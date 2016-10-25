"""This program takes in data from a file containing
   information concerning passengers on the Titanic.
   It modifies the data for each passenger and writes 
   them to a new file.  For use in Udacity Data Analysis 
   Nanodegree project for Data Visualization"""

# Create a new file:
file = open("new_titanic_data.csv", "w")

# Open given data file and split lines:
text = open("titanic_data.csv").read().splitlines()

# Add one category title to the categories in new file:
text[0] = text[0] + ',Age Category'
file.write(text[0] + '\n')

# Iterate through lines of data,
# modify them and write each line
# to the new file:
for i in range(1, len(text)):
    t = text[i].split(',')
    
    # Add data to new category "Age Category":
    if t[6] != '':
        age = float(t[6])
        if age < 18.0:
            t.append('Child')
        else:
            t.append('Adult')
    else:
        t.append('Age Unknown')
        
    # Change data in the "Survived" category:
    if t[1] == '0':
        t[1] = 'Non-Survivor'
    else:
        t[1] = 'Survivor'
        
    # Write new individual passenger data to new file:
    if i != len(text):     
        file.write(','.join(t) + '\n')
    else:
        file.write(','.join(t))

# Close file:
file.close()
    
    
