#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[3]:


#count number of schools 
Unique_Schools = school_data_complete['school_name'].unique()
count_schools = len(Unique_Schools)
count_schools


# In[38]:


# count number of total students
unique_IDs = school_data_complete['Student ID'].unique() 
count_students = len(unique_IDs) 
count_students


# In[39]:


# Calculate Total Budget  
total_budget = school_data_complete['budget'].sum() 
total_budget


# In[40]:


student_data.head()


# In[41]:


# calculate the average math score 
avg_math_score = school_data_complete['math_score'].mean()
avg_math_score


# In[8]:


# calculate average reading score 
avg_read_score = school_data_complete['reading_score'].mean()
avg_read_score


# In[9]:


#calculate overall passing rate  
total_pass = avg_read_score + avg_math_score
overall_pass_rate = total_pass/2
overall_pass_rate 


# In[10]:


# calculate % students with a passing math score 
Num_pass_math = school_data_complete.loc[student_data['math_score'] >= 70]['math_score'].count()
perc_pass_math = Num_pass_math/count_students
perc_pass_math.round(2)


# In[11]:


# calculate % students with a passing reading score 
Num_pass_read = school_data_complete.loc[student_data['reading_score'] >= 70]['math_score'].count()
perc_pass_read = Num_pass_read/count_students
perc_pass_read.round(2)


# In[12]:


#create new dataframe to display findings for entire school district
dist_sum = pd.DataFrame({
    "Total Schools": [count_schools],
    "Total Students": [count_students],
    "Total Budget": [total_budget],
    "Average Math Score": [avg_math_score],
    "Average Reading Score": [avg_read_score],
    "% Passing Math": [perc_pass_math],
    "% Passing Reading":[perc_pass_read],
    "Overall Passing Rate": [overall_pass_rate]})

#write df to csv
dist_sum.to_csv('dataframes/DistrictSummaryDF.csv', index = None, header=True)
dist_sum 


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# In[13]:


# group by school name 
grouped_school = school_data_complete.groupby(['school_name'])


# In[14]:


# display School type 
school_type = grouped_school['type'].first()
school_type


# In[15]:


# Calculate the total student for each school
total_student = grouped_school.size() 
total_student


# In[16]:


# calculate total school budget
total_budget = grouped_school['budget'].first()
total_budget


# In[17]:


bud_per_stu = total_budget/total_student 
bud_per_stu


# In[18]:


avg_math_score = grouped_school['math_score'].mean()
avg_math_score


# In[19]:


avg_read_score = grouped_school['reading_score'].mean()
avg_read_score


# In[20]:


grouped_passing_math = school_data_complete[school_data_complete['math_score']>=70].groupby(['school_name']).size()
percent_passing_math = (grouped_passing_math/total_student)*100
percent_passing_math



# In[21]:


grouped_passing_reading = school_data_complete[school_data_complete['reading_score']>=70].groupby(['school_name']).size()
percent_passing_reading = (grouped_passing_reading/total_student)*100 

percent_passing_reading


# In[22]:


percent_overall_passing = (percent_passing_math + percent_passing_reading)/2
percent_overall_passing


# In[24]:


school={
    'School Type': school_type,
    'Total Students':total_student,
    'Total School Budget': total_budget,
    'Per Student Budget': bud_per_stu,
    'Average Math Score': avg_math_score,
    'Average Reading Score': avg_read_score,
    '% Passing Math': percent_passing_math,
    '% Passing Reading': percent_passing_reading,
    '% Overall Passing Rate': percent_overall_passing,}
school_summary = pd.DataFrame(school)
school_summary

#write df to csv
school_summary.to_csv('dataframes/SchoolSummaryDF.csv', index = None, header=True)


# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[25]:


top_5 = school_summary.sort_values("% Overall Passing Rate", ascending = False)
top_5.to_csv('dataframes/Top5PassDF.csv', index = None, header=True)
top_5.head()


# In[ ]:





# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[26]:


bottom_5 = school_summary.sort_values("% Overall Passing Rate", ascending = True)
#write csv
bottom_5.to_csv('dataframes/Bottom5PassDF.csv', index = None, header=True)
bottom_5.head()


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[28]:


ninth_math = school_data_complete.loc[school_data_complete['grade'] == '9th'].groupby('school_name')["math_score"].mean()
tenth_math = school_data_complete.loc[school_data_complete['grade'] == '10th'].groupby('school_name')["math_score"].mean()
eleventh_math = school_data_complete.loc[school_data_complete['grade'] == '11th'].groupby('school_name')["math_score"].mean()
twelfth_math = school_data_complete.loc[school_data_complete['grade'] == '12th'].groupby('school_name')["math_score"].mean()

math_scores = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
math_scores = math_scores[['9th', '10th', '11th', '12th']]

#format table and show
math_scores.style.format({'9th': '{:.2f}', 
                          "10th": '{:.2f}', 
                          "11th": "{:.2f}", 
                          "12th": "{:.2f}"})

#write csv
math_scores.to_csv('dataframes/MathScoresDF.csv', index = None, header=True)
## Come back and use matplotlib to  create a line chart for school compariosn between grades


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[29]:


ninth_read = school_data_complete.loc[school_data_complete['grade'] == '9th'].groupby('school_name')["reading_score"].mean()
tenth_read = school_data_complete.loc[school_data_complete['grade'] == '10th'].groupby('school_name')["reading_score"].mean()
eleventh_read = school_data_complete.loc[school_data_complete['grade'] == '11th'].groupby('school_name')["reading_score"].mean()
twelfth_read = school_data_complete.loc[school_data_complete['grade'] == '9th'].groupby('school_name')["reading_score"].mean()

reading_scores = pd.DataFrame({
    "9th": ninth_read, 
    "10th": tenth_read, 
    "11th": eleventh_read, 
    "12th": twelfth_read
})
reading_scores = reading_scores[['9th','10th','11th','12th']]

#format table and show
reading_scores.style.format({'9th': '{:.2f}', 
                             "10th": '{:.2f}', 
                             "11th": "{:.2f}", 
                             "12th": "{:.2f}"})
#write csv
reading_scores.to_csv('dataframes/ReadingScoresDF.csv', index = None, header=True)


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[30]:


# Create Bins
bins = [0, 585, 615, 645, 675]
group_name = ["<$585", "$585-615", "$615-645", "$645-675"] 
school_data_complete['spending_bins'] = pd.cut(school_data_complete['budget']/school_data_complete['size'], bins, labels = group_name)



# In[31]:


#group schools by spending 
school_spend_group = school_data_complete.groupby('spending_bins')

#calculations
avg_math = school_spend_group['math_score'].mean()
avg_read = school_spend_group['reading_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('spending_bins')['Student ID'].count()/school_spend_group['Student ID'].count()
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('spending_bins')['Student ID'].count()/school_spend_group['Student ID'].count()
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('spending_bins')['Student ID'].count()/school_spend_group['Student ID'].count()

#build dataframe  
spending_table = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
            
}) 

#reorder columns
spending_table = spending_table[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]

spending_table.index.name = "Per Student Budget"
spending_table = spending_table.reindex(group_name)  
spending_table 

#formating 
spending_table.style.format({'Average Math Score': '{:.2f}', 
                              'Average Reading Score': '{:.2f}', 
                              '% Passing Math': '{:.2%}', 
                              '% Passing Reading':'{:.2%}', 
                              'Overall Passing Rate': '{:.2%}'})
#write csv
spending_table.to_csv('dataframes/SpendingTableDF.csv', index = None, header=True)


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[33]:


# Create Bins
bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"] 
school_data_complete['size_bins'] = pd.cut(school_data_complete['size'], bins, labels = group_names)


# In[36]:


#group by size 
school_size_grouped = school_data_complete.groupby('size_bins')

#calculations 
avg_math = school_size_grouped['math_score'].mean()
avg_read = school_size_grouped['reading_score'].mean() 
math_pass = school_data_complete[school_data_complete['math_score']>=70].groupby('size_bins')['Student ID'].count()/school_size_grouped['Student ID'].count()
read_pass = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('size_bins')['Student ID'].count()/school_size_grouped['Student ID'].count() 
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('size_bins')['Student ID'].count()/school_size_grouped['Student ID'].count()
 
#build dataframe 
scores_by_size = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': math_pass,
    '% Passing Reading': read_pass,
    "Overall Passing Rate": overall
            
}) 

#reorder columns
scores_by_size = scores_by_size[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]

scores_by_size.index.name = "Score Per School Size"
scores_by_size = scores_by_size.reset_index()  

scores_by_size.style.format({'Average Math Score': '{:.2f}',
    'Average Reading Score': '{:.2f}',
    '% Passing Math': '{:.2%}',
    '% Passing Reading': '{:.2%}',
    "Overall Passing Rate": '{:.2%}'
    
})

#write csv
scores_by_size.to_csv('dataframes/SizeTableDF.csv', index = None, header=True)


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[37]:


# Create a new data frame with our desired columns
scores_type = school_summary[['School Type','Average Math Score',
                                  'Average Reading Score','% Passing Math',
                                  '% Passing Reading','% Overall Passing Rate',]]
# Create a group based off of the school type
scores_type = scores_type.groupby('School Type').mean()

#formatting 
scores_type.style.format({'Average Math Score': '{:.1f}', 
                              'Average Reading Score': '{:.1f}', 
                              '% Passing Math': '{:.1f}', 
                              '% Passing Reading':'{:.1f}', 
                              '% Overall Passing Rate': '{:.1f}'})

#write csv 
scores_type.to_csv('dataframes/ScoresTypeDF.csv', index = None, header=True)


# In[ ]:




