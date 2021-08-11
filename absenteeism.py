# import packages
import pandas as pd

# Load absenteeism_at_work.csv as a DataFrame: absence
absence = pd.read_csv('Absenteeism_at_work.csv')

# Drop columns not of interest
to_drop = ['Seasons','Pet']
absence.drop(to_drop, inplace=True, axis=1)
print (absence.shape)

# Change column names
# Load simpler_column_names.csv as a DataFrame: new_col_names
new_col_names = pd.read_csv('Simpler column names.csv')

#Create a list of new column labels: new_labels
new_labels = list(new_col_names['DataFrame Col Label'])
z = zip(absence.columns, new_labels)
new_names_dict = dict(z)

# Change Column Names in absence DataFrame
absence.rename(columns = new_names_dict, inplace=True)

# check datatypes of absence Dataframe
print (absence.dtypes)
# All Columns are of type integer

# Sort absence Dataframe by ID Number descending order
absence.sort_values("ID", inplace=True)

# Replace 'reason_for_absence' disease codes with short description
# generate a list of codes representing 'reason_for_absence' values:
disease_classification_code = [num for num in range(1,29)]
# Load 'Key for causes of absence' dataframe
new_names_for_causes = pd.read_csv('Key for causes of absence.csv', header=0)
# Extract descriptive names for disease classification codes
new_names = list(new_names_for_causes['cause_of_absence'])
z = zip(disease_classification_code, new_names)
cause_codes_to_desc_dict = dict(z)

# absence uses a disease classification code to describe clinical cause of absence
# for readability we will replace the codes with short descriptive names
# Replace disease classification codes for descriptive names using dictionary of {codes:names}
absence['reason_for_absence'].replace(cause_codes_to_desc_dict, value=None, inplace=True)

# Convert categorical columns into datatype category
absence['reason_for_absence'] = absence['reason_for_absence'].astype('category')
absence['day'] = absence['day'].astype('category')
absence['month'] = absence['month'].astype('category')
absence['disciplinary_failure'] = absence['disciplinary_failure'].astype('category')
absence['education_level'] = absence['education_level'].astype('category')
absence['drink'] = absence['drink'].astype('category')
absence['smoke'] = absence['smoke'].astype('category')

#check datatypes for each column
print (absence.dtypes)

# check ranges for category columns
print (absence['month'].unique())
print (absence[absence['month'] == 0])
# only 3 rows, we can drop these rows (as absenteeism = 0 and cause = 0)
absence = absence[absence['month'] != 0]

print (absence['day'].unique())
print (absence['disciplinary_failure'].unique())
print (absence['education_level'].unique())
print (absence['drink'].unique())
print (absence['smoke'].unique())
# All good

print (absence['reason_for_absence'].unique())
# 28 categories, all good

print (absence[absence['reason_for_absence'] == 0])
# 40 rows have 'reason for absence' incorrectly set to value 0
# All of these rows have 'absenteeism_time_hours of zero
# Let's drop all rows with absenteeism_time of zero
print (absence[absence['absenteeism_time_hours'] == 0])
absence = absence[absence['absenteeism_time_hours'] > 0]

print (absence.shape)

# absence due to routine medical appointments have 7 defined category values
# these will be collapsed into a single categorical value for simplicity
# define which category values we want to collapse
absence_for_routine_medical_appts = ['health_factors_treatment', 'follow_up_consultation',\
                                     'medical_consultation', 'blood_donation', 'lab_exam' \
                                     'physiotherapy', 'dental_consultation']
# We want a single categorical value 'routine_medical_appt'
# create a mapping to map the 7 categories onto one:
list1 = ['routine_medical_appt']
mapping1 = { key:value for key in absence_for_routine_medical_appts for value in list1}
print (mapping1)
# replace the 7 categorical values with 1 catch-all value
absence['reason_for_absence'] = absence['reason_for_absence'].replace(mapping1)

# Summary of absence dataset cleaning so far:
# 696 observations over 18 columns
# All category columns have categorical values in correct range
# 3 columns not of interest were dropped
# rows with absenteeism_time_hours of zero were dropped
# Column names were replaced with clearer, more concise descriptors
# ICD codes for medical causes for absence were replaced with concise descriptors
# a single categorical value 'routine_medical_appt' replaced 7 category values
# All column datatypes correct

print (absence.columns)
# look at height and weight values
import matplotlib.pyplot as plt
plt.hist(absence['weight (kg)'])
plt.title('Weight_kg')
plt.show()
# it looks like Weight is in Kg
plt.hist(absence['height (cm)'])
plt.title('Height_cm')
plt.show()
# it looks like 'Height is in cm

# check bmi values
# With the metric system, the formula for BMI is weight in kilograms divided by height in meters squared.
# Since height is commonly measured in centimeters, an alternate calculation formula,
# dividing the weight in kilograms by the height in centimeters squared,
# and then multiplying the result by 10,000, can be used.
bmi = (absence['weight (kg)'] / absence['height (cm)'] ** 2) * 10000
# verify that bmi values in absence 'bmi' column are correct
bmi_delta = bmi - absence['bmi']
print (bmi_delta.max())
# close enough, the max difference is 0.7458
