# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:22:13 2020

@author: Aline Barbosa Alves

Technical test - Intelie - Support Data Analyst
"""

"""Import packages"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, datetime

"""Import Data"""
# Save filepath to variable for easier access
path = '/home/aline/Documentos/Ubiqum/Interview/Intelie/data/HRDataset_v13.csv'

# Read the data and store data in DataFrame
data = pd.read_csv(path)

"""Get to know the data"""
# Print a summary of the data
data.describe()

# Columns
data.columns

# Types
data.dtypes

# First 50 data points
data.head(50)

# Shape
data.shape

# Missing data
data.isnull().sum()

# Delete nan values for sex
data['Sex'].unique()
data.dropna(subset=['Sex'],inplace=True)

# Define function to calculate age
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < 
                                     (born.month, born.day))

# Set Date of Birth as date
data['DOB'] = datetime.strptime(data['DOB'], '%m/%d/%y')

# Fix the year
c = 0
for i in data['DOB']:
    if i > datetime.now():
        data['DOB'][c] = data['DOB'][c].replace(year=data['DOB'][c].year-100)
    c = c + 1

# Create an age column
data['Age'] = data.apply(lambda row : calculate_age(row['DOB']), axis = 1)
 
# Replace yes / no on HispanicLatino column
data['HispanicLatino'] = data['HispanicLatino'].replace(('yes','no'),
                                                        ('Yes','No'))
data['HispanicLatino'].unique()

"""Plots"""
# Set the size
plt.rcParams["figure.figsize"] = (16,9)

# Sex
data['Sex'].value_counts().plot(kind='bar')

# Sex / Department
chart = sns.countplot(x=data['Department'],hue=data['Sex'])
chart.set_xticklabels(chart.get_xticklabels(), rotation=45)

# Diversity / Sex
sns.countplot(x=data['Sex'],hue=data['FromDiversityJobFairID'])

# Diversity / Department
chart = sns.countplot(x=data['Department'],hue=data['FromDiversityJobFairID'])
chart.set_xticklabels(chart.get_xticklabels(), rotation=45)

# Race
data['RaceDesc'].value_counts().plot(kind='bar')

# Citizen
data['CitizenDesc'].value_counts().plot(kind='pie')

# Position
data['Position'].value_counts().plot(kind='bar')

# Pay rate / Position
position = data['Position'].replace(('Data Analyst ','IT Manager - DB',
               'IT Manager - Infra','IT Manager - Support'),
               ('Data Analyst', 'IT Manager','IT Manager','IT Manager'))
position = ['Accountant I', 'Administrative Assistant', 'Area Sales Manager',
       'BI Developer', 'BI Director', 'CIO', 'Data Architect',
       'Database Administrator', 'Data Analyst', 'Director of Operations',
       'Director of Sales', 'IT Director', 'IT Manager', 'IT Support',
       'Network Engineer', 'President & CEO', 'Production Manager', 
       'Production Manager', 'Production Technician I', 
       'Production Technician II', 'Sales Manager', 'Senior BI Developer', 
       'Shared Services Manager',
       'Software Engineer', 'Software Engineering Manager',
       'Sr. Accountant', 'Sr. DBA', 'Enterprise Architect',
       'Principal Data Architect', 'Sr. Network Engineer']

plt.figure(figsize=(32,18))
chart = data.plot(x='PositionID',y='PayRate',kind='scatter')
plt.xticks(np.sort(data['PositionID'].unique()), position)
chart.set_xlabel('Position')
chart.set_xticklabels(chart.get_xticklabels(), rotation=90)

# Pay rate sum by Position
data.groupby('Position')['PayRate'].sum().plot(kind='bar')

# Pay rate / Department
chart = data.plot(x='DeptID',y='PayRate',kind='scatter')
plt.xticks(data['DeptID'].unique(), data['Department'].unique())
chart.set_xlabel('Department')

# Pay rate sum by department
data.groupby('Department')['PayRate'].sum().plot(kind='bar')

# Manager / Performance
sns.countplot(y=data['ManagerName'], hue=data['PerformanceScore'])

# Manager / Satisfaction
sns.countplot(y=data['ManagerName'], hue=data['EmpSatisfaction'])

# Manager / Special Projects
sns.countplot(y=data['ManagerName'], hue=data['SpecialProjectsCount'])

# Age
data['Age'].hist(bins=25)

# Hispanic Latino / Pay rate
sns.violinplot('HispanicLatino', 'PayRate', data = data)

# Hispanic Latino
data['HispanicLatino'].value_counts().plot(kind='bar')

# Marital
data['MaritalDesc'].value_counts().plot(kind='pie')

# Marital / Status
sns.countplot(x=data['EmploymentStatus'],hue=data['MaritalDesc'])

# Citizen / Pay rate
sns.violinplot('CitizenDesc', 'PayRate', data = data)

# Recruitment
data['RecruitmentSource'].value_counts().plot(kind='bar')

# Recruitment / Status
sns.countplot(y=data['RecruitmentSource'],hue=data['EmploymentStatus'])

# Pay rate sum by recruitment
data.groupby('RecruitmentSource')['PayRate'].sum().plot(kind='bar')

# Pay rate mean by recruitment
data.groupby('RecruitmentSource')['PayRate'].mean().plot(kind='bar')

# Recruitment / Performance
sns.countplot(y=data['RecruitmentSource'], hue=data['PerformanceScore'])

# Recruitment / Satisfaction
sns.countplot(y=data['RecruitmentSource'], hue=data['EmpSatisfaction'])