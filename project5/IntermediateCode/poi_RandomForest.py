# For Udacity Intro to Machine Learning Class Project
# This will use the Random Forest classifier to 
# Help identify persons of interest in the Enron email corpus

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 
                     'bonus', 'restricted_stock_deferred', 'deferred_income', 
                     'total_stock_value', 'expenses', 'exercised_stock_options', 
                     'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

email_features = ['to_messages', 'from_poi_to_this_person', 
                  'from_messages', 'from_this_person_to_poi', 
                  'shared_receipt_with_poi']
                  
all_features = ['poi'] + financial_features + email_features

features_list = ['poi','salary', 'shared_receipt_with_poi', 'deferred_income', 
                 'total_stock_value', 'exercised_stock_options', 'expenses',
                 'sum_fractions_to_and_from'] 


### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Task 2: Remove outliers

del data_dict['TOTAL'] 
del data_dict['THE TRAVEL AGENCY IN THE PARK']

### Task 3: Create new feature(s)

def computeFraction(poi_messages, all_messages):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
    """
   
    fraction = 0.

    if poi_messages != 'NaN' and all_messages != 'NaN':
        if all_messages != 0.0:
            fraction = float(poi_messages) / float(all_messages)
     
    return fraction


for name in data_dict:

    data_point = data_dict[name]
    
    from_poi_to_this_person = data_point["from_poi_to_this_person"]
    to_messages = data_point["to_messages"]
    fraction_from_poi = computeFraction( from_poi_to_this_person, to_messages )

    data_point["fraction_from_poi"] = fraction_from_poi

    from_this_person_to_poi = data_point["from_this_person_to_poi"]
    from_messages = data_point["from_messages"]
    fraction_to_poi = computeFraction( from_this_person_to_poi, from_messages )
    
    data_point["fraction_to_poi"] = fraction_to_poi
    
    data_point["sum_fractions_to_and_from"] = \
               fraction_from_poi + fraction_to_poi

    data_dict[name] = data_point
    
all_features = all_features + \
               ["fraction_from_poi", "fraction_to_poi", "sum_fractions_to_and_from"]   

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, all_features)

labels, features = targetFeatureSplit(data)

## Use PCA to minimize dimension and create new features:
#from sklearn.decomposition import PCA
#pca = PCA(n_components = 2)
#
## Use original features:
#from sklearn.feature_selection import SelectKBest
#selection = SelectKBest(k = 6)
#
#
## Combine new features with k-best original features:
#from sklearn.pipeline import FeatureUnion
#combined_features = FeatureUnion([('selection', selection), ('pca', pca)])
#
## Classifier used is Random Forest:
from sklearn.ensemble import RandomForestClassifier
#rf = RandomForestClassifier(min_samples_split = 3)
#
#from sklearn.pipeline import Pipeline
#pipeline = Pipeline([('features', combined_features), ('rf', rf)])

from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size = 0.3, random_state = 42)
    
#from sklearn.grid_search import GridSearchCV
#param_grid = dict(features__pca__n_components = range(2),
#                  features__selection = range(1, 10, 2),
#                  rf__min_samples_split = range(1, 3))
#grid_search = GridSearchCV(pipeline, param_grid = param_grid,
#                           scoring = 'recall')
#grid_search.fit(features_train, labels_train)
#print(grid_search.best_estimator_)
#                  
#clf = GridSearchCV(pipeline, param_grid = param_grid, verbose = 0)
#clf.fit(features_train, labels_train)
#
#bool_mask = selection.get_support()
#scores = selection.scores_
#p_values = selection.pvalues_
#f = all_features[1:]
#for i in range(len(f)):
#    if bool_mask[i]:
#        print f[i], scores[i], p_values[i]

clf = RandomForestClassifier(min_samples_split = 5, criterion = "entropy",
                             max_features = None)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)