########################################################################################
##
##    Udacity Data Analysis Nanodegree Wrangle OpenStreetMaps Project
##    https://www.udacity.com/course/data-analyst-nanodegree--nd002
##
##    The map data is taken from MapZen: https://mapzen.com/data/metro-extracts
##    The data chosen to investigate is the OSM XML data for Milwaukee, Wisconsin
##    avaliable here:
##    https://s3.amazonaws.com/metro-extracts.mapzen.com/milwaukee_wisconsin.osm.bz2


########################################################################################
##
##    Imports

from pymongo import MongoClient
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


########################################################################################
##
##    count_tags determines the number of each of the tags in the data

def count_tags(filename):
        tags = {}

        for event, elem in ET.iterparse(filename, events = ('start',)):
            if elem.tag not in tags:
                tags[elem.tag] = 1
            else:
                tags[elem.tag] = tags[elem.tag] + 1

        return tags

##    tags = count_tags('mke.osm')
##    pprint.pprint(tags)
##
##    tags = {'bounds': 1,
##            'member': 6579,
##            'nd': 859194,
##            'node': 697806,
##            'osm': 1,
##            'relation': 540,
##            'tag': 443856,
##            'way': 78494}


#######################################################################################
##
##    The code below processes and parses the xml file and creates a list of dictionaries
##    that will later be converted to JSON.  A smaller version is also created
##    that only contains elements that have address information


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    address = {}

    if element.tag == "node" or element.tag == "way" :
        attributes = element.attrib
        node['type'] = element.tag

        for attribute in attributes:
            if attribute not in CREATED:
                if attribute != 'lat' and attribute != 'lon':
                    node[attribute] = attributes[attribute]
                else:
                    if 'pos' not in node:
                        node['pos'] = [0.0, 0.0]
                    if attribute == 'lat':
                        node['pos'][0] = float(attributes[attribute])
                    if attribute == 'lon':
                        node['pos'][1] = float(attributes[attribute])
            else:
                if 'created' not in node:
                    node['created'] = {attribute: attributes[attribute]}
                else:
                    node['created'][attribute] = attributes[attribute]

        for nd in element.iter('nd'):
            if 'node_refs' in node:
                node['node_refs'].append(nd.attrib['ref'])
            else:
                node['node_refs'] = [nd.attrib['ref']]

        for tag in element.iter('tag'):
            k = tag.attrib['k']
            v = tag.attrib['v']

            if problemchars.search(k):
                continue
            elif k[:5] == 'addr:':
                if ':' in k[5:]:
                    continue
                else:
                    address[k[5:]] = v
            else:
                node[k] = v

        if address != {}:
            node['address'] = address

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    data = []
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:
            data.append(el)
    return data

def process_map_address_nodes_only(file_in, pretty = False):
    data = []
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:
            if 'address' in el:
                data.append(el)
    return data


mke = process_map('mke.osm')
mke_address_only = process_map_address_nodes_only('mke.osm')


########################################################################################
##
##    The data was then audited using AuditStreetName.py and
##    the mapping below is a reflection of the fields needed to update.
##    The clean_data function will clean the street information in the data.
##    Specifically, abbreviations of the street type are converted to their full name.
##    Also, a cleaning process is done to change qualifiers such
##    as N, No., No to the full word (eg. North)

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Rd": "Road",
            "Ave.": "Avenue",
            "Ave": "Avenue",
            "Dr.": "Drive",
            "Dr": "Drive",
            "Cir": "Circle",
            "Ct": "Court",
            "Ln": "Lane",
            "PL": "Place",
            "Pl.": "Place",
            "Pkwy": "Parkway",
            "Blvd": "Boulevard"}

compass_mapping = {'No.':'North',
                   'NO.':'North',
                   'No':'North',
                   'NO':'North',
                   'N':'North',
                   'N.':'North',
                   'So.':'South',
                   'SO.':'South',
                   'So':'South',
                   'SO':'South',
                   'S':'South',
                   'S.':'South',
                   'E':'East',
                   'E.':'East',
                   'W':'West',
                   'W.':'West',
                   'NORTH':'North',
                   'SOUTH':'South',
                   'EAST':'East',
                   'WEST':'West'}

def update_name(name, mapping):
    for key in mapping:
        if re.search(key + '$', name):
            name = name[:-len(key)] + mapping[key]

    return name

def clean_data(input_list):
    for node in input_list:
        if 'address' in node:
            if 'street' in node['address']:
                node['address']['street'] = update_name(node['address']['street'], mapping)
                words = node['address']['street'].split(' ')
                if words[0] in compass_mapping:
                    words[0] = compass_mapping[words[0]]
                    node['address']['street'] = ' '.join(words)
    return

clean_data(mke)
clean_data(mke_address_only)

#######################################################################################\
##
##    The function create_json_file takes the list of dictionaries as input
##    and converts it to a json file

def create_json_file(file_in, json_filename, pretty = False):
    file_out = "{0}.json".format(json_filename)
    with codecs.open(file_out, "w") as fo:
         for el in file_in:
            if pretty:
                fo.write(json.dumps(el, indent=2)+"\n")
            else:
                fo.write(json.dumps(el) + "\n")
    return

create_json_file(mke, 'mke')
create_json_file(mke_address_only, 'mke_small')

#######################################################################################
##
##    The rest of the code loads the file into a MongoDB database
##    and the database is analyzed by running queries.
##
##    The code here uses pymongo to load the files into MongoDB,
##    but it can also be done from the command line with the shell command:
##    mongoimport --db streetmap --collection mke --file mke.json

##    Load file into MongoDB database:

client = MongoClient('localhost:27017')
db = client.streetmap
for node in mke:
    db.mke.insert(node)

##    Run Queries:

print "Number of data entries in database:", db.mke.count()
print "Number of unique users:", len(db.mke.distinct("created.user"))
print "Number of nodes:", db.mke.find({'type':'node'}).count()
print "Number of ways:", db.mke.find({'type':'way'}).count()
print "Number of data entries with position info:", db.mke.find({'pos': {'$exists': True}}).count()
print "Number of data entries with address info:", db.mke.find({'address': {'$exists': True}}).count()
print "Number of data entries with street info:", db.mke.find({'address.street': {'$exists': True}}).count()
print "Number of data entries with amenity info:", db.mke.find({'amenity': {'$exists': True}}).count()
print "Number of data entries with building info:", db.mke.find({'building': {'$exists': True}}).count()

##    Number of data points: 776300
##    Number of nodes: 697799
##    Number of ways: 78486
##    Number of data points with address info: 2804
##    Number of data points with street info: 2317

##    Aggregation queries:

def aggregate(db, pipeline):
    return [doc for doc in db.mke.aggregate(pipeline)]

print '\nNumber of users with only one contribution:'
pipeline1 = [{"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
             {"$group": {"_id": "$count", "num_users": {"$sum": 1}}},
             {"$sort": {"_id": 1}},
             {"$limit": 1}]
result1 = aggregate(db, pipeline1)
pprint.pprint(result1)

##    [{u'_id': 1, u'num_users': 122}]

print '\nTop 5 contiributing users:'
pipeline2 = [{"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
              {"$sort": {"count": -1}},
              {"$limit": 5}]
result2 = aggregate(db, pipeline2)
pprint.pprint(result2)

##    [{u'_id': u'woodpeck_fixbot', u'count': 181244},
##     {u'_id': u'ItalianMustache', u'count': 69763},
##     {u'_id': u'reschultzed', u'count': 45951},
##     {u'_id': u'Gary Cox', u'count': 32553},
##     {u'_id': u'bbauter', u'count': 31861}]

print '\nTop 5 types of restaurant cuisine categories:'
pipeline3 = [{"$match": {"amenity": {"$exists": 1}, "cuisine": {"$exists": 1}, "amenity": "restaurant"}},
             {"$group": {"_id": "$cuisine",  "count": {"$sum": 1}}},
             {"$sort": {"count": -1}},
             {"$limit": 5}]
result3 = aggregate(db, pipeline3)
pprint.pprint(result3)

##    [{u'_id': u'american', u'count': 29},
##     {u'_id': u'pizza', u'count': 28},
##     {u'_id': u'italian', u'count': 23},
##     {u'_id': u'chinese', u'count': 15},
##     {u'_id': u'mexican', u'count': 14}]

print '\nTop 5 types of buildings:'
pipeline4 = [{'$match': {'building': {'$exists': 1}}},
             {'$group': {'_id': '$building', 'count': {'$sum': 1}}},
             {'$sort': {'count': -1}},
             {'$limit': 5}]
result4 = aggregate(db, pipeline4)
pprint.pprint(result4)

##    [{u'_id': u'yes', u'count': 5963},
##     {u'_id': u'house', u'count': 755},
##     {u'_id': u'apartments', u'count': 592},
##     {u'_id': u'commercial', u'count': 458},
##     {u'_id': u'garage', u'count': 356}]

print '\nTop 5 types of amenities:'
pipeline5 = [{'$match': {'amenity': {'$exists': 1}}},
             {'$group': {'_id': '$amenity', 'count': {'$sum': 1}}},
             {'$sort': {'count': -1}},
             {'$limit': 5}]
result5 = aggregate(db, pipeline5)
pprint.pprint(result5)

##    [{u'_id': u'parking', u'count': 1800},
##     {u'_id': u'school', u'count': 905},
##     {u'_id': u'restaurant', u'count': 385},
##     {u'_id': u'fast_food', u'count': 202},
##     {u'_id': u'fuel', u'count': 164}]

