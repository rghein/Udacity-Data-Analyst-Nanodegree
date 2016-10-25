import pickle

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    
    
features = ['salary', 'to_messages', 'deferral_payments', 'total_payments', 
            'exercised_stock_options', 'bonus', 'restricted_stock', 
            'shared_receipt_with_poi', 'restricted_stock_deferred', 
            'total_stock_value', 'expenses', 'loan_advances', 'from_messages', 
            'other', 'from_this_person_to_poi', 'poi', 'director_fees', 
            'deferred_income', 'long_term_incentive', 'email_address', 
            'from_poi_to_this_person']


print 'Number of Data Points:', len(data_dict), '\n' 

#    Result:  146

num_poi, non_poi = 0, 0
for person in data_dict:
    if data_dict[person]['poi']:
        num_poi = num_poi + 1
    else:
        non_poi = non_poi + 1
        
print 'Number of POI:', num_poi
print 'Number of Non POI:', non_poi, '\n' 

#    Result:
#    Number of POI: 18
#    Number of Non POI: 128  

print 'Number of features:', len(features), '\n' 


#    Result: 21
 
print 'Feature | Percentage Missing Values' 
print '-----------------------------------'       
for feature in features:
    total, not_nan, nan = 0, 0, 0
    for person in data_dict:
        total = total + 1
        if data_dict[person][feature] == 'NaN':
            nan = nan + 1
        else:
            not_nan = not_nan + 1
    print feature, ' | ', "{0:.2f}".format(100.0 * nan / total) 


#    Result:
#
#    Feature | Percentage Missing Values 
#    
#    ----------------------------------- 
#    
#    salary  |  34.93
#    to_messages  |  41.10
#    deferral_payments  |  73.29
#    total_payments  |  14.38
#    exercised_stock_options  |  30.14
#    bonus  |  43.84
#    restricted_stock  |  24.66
#    shared_receipt_with_poi  |  41.10
#    restricted_stock_deferred  |  87.67
#    total_stock_value  |  13.70
#    expenses  |  34.93
#    loan_advances  |  97.26
#    from_messages  |  41.10
#    other  |  36.30
#    from_this_person_to_poi  |  41.10
#    poi  |  0.00
#    director_fees  |  88.36
#    deferred_income  |  66.44
#    long_term_incentive  |  54.79
#    email_address  |  23.97
#    from_poi_to_this_person  |  41.10



    
