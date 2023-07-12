#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Automatic package import
get_ipython().system('pip install pyforest')


# In[5]:


# package to visualize missing values
get_ipython().system('pip install missingno')


# In[7]:


# PAckage for in-depth EDA report
get_ipython().system('pip install sweetviz')


# In[9]:


# calling pyforest/ no need to write imports
from pyforest import *


# In[14]:


#data description
df = pd.read_csv('../GIS 4.1/GEOSTATS/R Practicals/Kaggle_DATA/climate_change_data.csv')


# In[16]:


#visualize the data frame
df.head()


# In[19]:


# visualize missing values
import missingno as msno
msno.matrix(df)


# In[93]:


# Current EDA report
import sweetviz as sv

report = sv.analyze(df)
report.show_html()


# In[26]:


# numerical columns
num_cols = []
for col in df.columns:
    if df[col].dtypes != 'o':
        num_cols.append(col)
    


# In[ ]:


# visualize the numerical columns to detect outliers
plt.figure(figsize = (20, 30))
for i, col in enumerate(num_cols):
    ax = plt.subplot(3, 2, i + 1)
    sns.histplot(df[col], kde = True)
    ax.set_title(col + "Histogram")


# In[ ]:


plt.show_html()


# In[30]:


###----- Trimming the outliers using z-score ----###
# Z-score method can only be applied on columns with normal or almost normal distribution. 
# Here, If a certain value falls outside of 3 standard deviations we can say it an outlier.
mean = df['Temperature'].mean()
std = df['Temperature'].std()
upper_limit = mean + 3 * std
lower_limit = mean - 3 * std


# In[32]:


df.shape


# In[40]:


len(df[(df['Temperature'] >= lower_limit) & (df['Temperature'] <= upper_limit)])


# In[42]:


# Show the detected outliers indices
len(df[(df['Temperature'] < lower_limit) | (df['Temperature'] > upper_limit)])


# In[44]:


# removal of the outliers
df1 = df[(df['Temperature'] >= lower_limit) & (df['Temperature'] <= upper_limit)]


# In[57]:


# show the remaining indices
df1.shape


# In[58]:


# Capping to set the value to upper & lower limit
df2 = df.copy()


# In[59]:


df2['Temperature'] = np.where(df['Temperature'] > upper_limit, 
                              upper_limit, 
                              np.where(df['Temperature'] < lower_limit,
                                       lower_limit,
                                       df['Temperature']
                                     )
                             )


# In[60]:


df1.head()


# In[91]:


# in-depth report after Z-score method, removal of outlier

import sweetviz as sv1

report1 = sv1.analyze(df1)
report1.show_html()


# In[64]:


## ---- Percentile Method ----##
# Percentile - describes how a compare to other scores from the same set. 
# If a value is in kth percentile, it is greater than k percent of the total values. 
# In percentile method, if a value is greater than 99/95 percentile(depends upon the problem statement) or less than 1/5 percentile than it is consider an outlier.

# creating a df for pm
df02 = df.copy()


# In[66]:


# visualize the df02
df02.head()


# In[68]:


# Plot the df02 to detect outliers
sns.displot(df02['Temperature'], kde = True)


# In[70]:


# The value with 99th percentile 
upper_limit = df02['Temperature'].quantile(0.99) 
upper_limit


# In[72]:


#The value with 1th percentile 
lower_limit = df02['Temperature'].quantile(0.01)
lower_limit


# In[74]:


# Trim the outliers
df02.shape


# In[77]:


# the outliers indices
len(df02[(df2['Temperature'] > upper_limit) | (df2['Temperature'] < lower_limit)])


# In[79]:


# remaining values
new_df02_1 = df02[(df2['Temperature'] <= upper_limit) & (df2['Temperature'] >= lower_limit)]


# In[81]:


new_df02_1.shape


# In[85]:


##---- Capping/winsorization using percentile method -----##
new_df02_2 = df02.copy()


# In[87]:


new_df02_2['Temperature'] = np.where(df02['Temperature'] > upper_limit,
                                     upper_limit,
                                     np.where(df02['Temperature'] < lower_limit,
                                             lower_limit,
                                             df02['Temperature']
                                             )
                                    )


# In[94]:


# describe the new data
new_df02_2.head()


# In[96]:


# Current EDA report after Percentile Method

report = sv.analyze(new_df02_2)
report.show_html()


# In[99]:


## -----IQR Method ----##
###############################################
########  IQR - Inter Quartile Range ##########
######## Q1 - 25th percentile #################
######## Q2 - 50th percentile (Median) ########
########## Q3 - 75th percentile ###############

# Used for skewed data. 
# In this method, we calculate the minimum and maximum value. 
# If any value is less than minimum value or greater than maximum value, then it is considered as an outlier. 
# IQR = Q3 - Q1 
# Minimum = Q1 - 1.5 * IQR 
# Maximum = Q3 + 1.5 * IQR

df03 = pd.read_csv('../GIS 4.1/GEOSTATS/R Practicals/Kaggle_DATA/train.csv')


# In[101]:


df03.head()


# In[103]:


# we have positively skewed data
sns.histplot(df03['Fare'], kde = True)


# In[105]:


# visualize with a boxplot
sns.boxplot(x = df03['Fare'])


# In[107]:


# summary of the change
q1 = df03['Fare'].quantile(0.25)
q3 = df03['Fare'].quantile(0.75) 
iqr = q3 - q1


# In[110]:


# creating mean val and max value 
min_val = q1 - (1.5 * iqr) 
max_val = q3 + (1.5 * iqr)


# In[111]:


len(df03[(df03['Fare'] > max_val) | (df03['Fare'] < min_val)])


# In[119]:


#### -----Trimming -----####

df03.shape


# In[115]:


new_df03_1 = df03[(df03['Fare'] < max_val) & (df03['Fare'] > min_val)]


# In[117]:


new_df03_1.shape


# In[120]:


#Visualize the new data
sns.histplot(new_df03_1['Fare'], kde = True)


# In[122]:


# Use Boxplot to detect new outliers
sns.boxplot(x = new_df03_1['Fare'])


# In[124]:


#### ------ Capping ----#####
new_df03_2 = df03.copy()


# In[126]:


new_df03_2['Fare'] = np.where(df03['Fare'] > max_val,
                             max_val,
                             np.where(df03['Fare'] < min_val,
                                     min_val,
                                     df03['Fare']
                                     )
                             )


# In[128]:


new_df03_2.sample(5)


# In[129]:


# report on the data

report = sv.analyze(new_df03_2)
report.show_html()

