# Titanic Data Visualization

***

**_Udacity Data Analyst Nanodegree Data Visualization Project - Greg Hein_**


## Summary 

***

This project looks at a database that contains a number of the demographic characteristics for each of the passengers on the [Titanic](https://en.wikipedia.org/wiki/RMS_Titanic). It is an investigation with the intention of finding which specific types of those passenger characterstics had higher rates of survival, and to demonstrate those findings with data visualization.  Three charts are shown looking at the passenger characterstics of:  Passenger Class, Sex, and Age with respect to passenger survival.  The visualization shows that Upper Classes (1 > 2 > 3), Females, and Children all had higher survival rates.


## Design 

***

The project description called for creating: "a visualization that shows the demographics or passenger information between those passengers who survived and those who died".  After looking at the titanic data file, 3 categories for each passenger looked like they would possibly show differences with regard to survival of the passengers, so they were chosen for the visualization.  As mentioned in the summary, the categories of Passenger Class, Sex, and Age were used for the visualization for comparison with respect to survival. The goal of the project and visualization was finding which type of each had higher survival rates.    

Because the visualizations would show comparisons between categories of data, bar charts were chosen as the chart type.  

The project also indicated that it was required to solicit feedback from at least three persons, and to improve the visualization if possible from the suggestions.  

The dimple.js library for web based charting which uses D3.js/JavaScript was utilized to make bar charts of the number of survivors from all the different categories listed above.  The initial bar charts were kept simple, with minimal refinement, in an effort to encourage feedback and criticism from the reviewers.  

After review, a number of changes were made to the charts:

1. The first reviewer made two points about the charts.  First that althought the number of survivors was shown in the chart, what would be helpful was a comparison of the number of survivors vs. non-survivors in each category. For this reason, the charts were changed to vertical grouped bar charts showing the number of passengers in each category, split by color, with survivors next to non-survivors. The second point was that the age chart really did a poor job of communicating any worthwhile information about the data.   For this reason, it was decided to group persons into age groups.  Three groups of age were chosen: Children (younger than 18); Adults (18 and older); and Age Unknown.  The last category was used due to the fact that many passengers did not have an age listed in the data.  This was done for completeness, so that the number of passengers was consistent in all 3 charts.  The reason for separating children vs. adults was somewhat arbitrary, but chosen in reference to the often quoted "[women and children first](https://en.wikipedia.org/wiki/Women_and_children_first)".  This grouping was done by creating a modified version of the initial titanic_data.csv file and adding an additional category of "Age Category".  That category was then used for the age chart.  This was done with a short python script. (included with submission). 

2. The second reviewer made comments about the labels of the charts and what was seen on scroll over of the charts, that they were confusing.  The colors for each chart were labeled 0/1, as they were in the original csv file to represent Non-Survivor/Survivor.  In addition, to someone who was unfamiliar with the original data file, an axis label such as "Pclass" did not make it obvious what was being charted.  For this reason, two things were done.  The dimple code was updated with changes to the titles of the x and y axes where necessary.  This did not however influence the 0/1 problem, and there was still a problem on scroll over.  For this reason, the python script mentioned above was used to further modify the data, and change the 0 and 1 in the "Survived" field to "Non-Survivor" and "Survivor".  In creating the dimple code, the category "Name" was being used for the y axes (any non numeric catogory would show the number of data points in a dimple bar chart).  The csv file was simply manually modified to change the title of the "Name" category to "Number of Passengers".  This solved the problem with scroll over information regarding the number of passengers (went from for example, "Name: 372" to "Number of Passengers: 372").  Similarly, "Pclass" was changed to "Passenger Class".   

3. The third reviewer had two suggestions.  It was suggested to add some minimal text information to add descriptions of the charts and their findings to help the chart viewer understand what was being presented.  Also, it was suggested to spruce up the charts with a little color.  In response to those suggestions, text was added to the index.html file, and the dimple code was updated and all three charts were given different colors.  Also a very minimal amount of css styling was added to the index.html file to possibly improve the chart viewing experience.  

4. Other modifications were made from the initial charts after the three soliciations for feedback.  The dimple code was changed to make the charts smaller.  This was done to make them look more compact, as they were only comparing a small number of categories, and to possibly make them easier to view with different screen/brower sizes.  Also, a decision was made to change the y-axis from the number of passengers to the percentage survived in each type and to only include percentage survived (not non-survivors), so as to concentrate on the goal of the project to determine which of the types of each characteristic had a higher rate of survival.  


## Feedback

***

#### There were 3 different solicitations for feedback, below is a summation of their comments: 

#### First Feedback  
*In some way show the relative numbers of survivors vs. non-survivors so the different categories can be better compared.  Also, either remove the age chart, as it conveys no information regarding relative survival, or possibly group the ages to see if that may convey some information.*

#### Second Feedback
*Improve the labels on the chart axes and the scroll over data to make it easier for the person viewing the chart to interpret what the chart is showing.*  

#### Third Feedback
*One can see from looking at the visualizations that relatively speaking, Children were more likely to survive than Adults, Females more likely to survive than males, and upper class passengers more likely to survive than lower class passengers.  A suggestion to possibly add a heading for each chart describing what it is looking at.  Also, it might aesthetically improve the charts if it were a little dressed up with more color.* 


## Resources

***

**Sources consulted to create visualization:**

[Udacity Intro to HTML and CSS Class](https://www.udacity.com/course/intro-to-html-and-css--ud304) 

[Udacity Intro to JavaScript Course](https://www.udacity.com/course/intro-to-html-and-css--ud304) 

[Udacity Data Visualization and D3.js Course](https://www.udacity.com/course/data-visualization-and-d3js--ud507) 

[Link to Specific Titanic Data Used](https://www.google.com/url?q=https://www.udacity.com/api/nodes/5420148578/supplemental_media/titanic-datacsv/download&sa=D&ust=1475090699719000&usg=AFQjCNF5F5mKo92XbpeSRrwL8hpB4-Y4FA) 

[More Detailed Information Regarding the Titanic Data](https://www.kaggle.com/c/titanic/data) 

[dimple Documentation](https://github.com/PMSI-AlignAlytics/dimple/wiki) 

[dimple Examples from dimple Documentation](http://dimplejs.org/examples_index.html) 

[Flowchart to help choose which chart to use](https://apandre.files.wordpress.com/2011/02/chartchooserincolor.jpg) 

