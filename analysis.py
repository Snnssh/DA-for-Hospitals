import pandas as pd
import matplotlib.pyplot as plt


def gender_set(row):
    if str(row)[0] in ['f', 'F', 'w', 'W']:
        return 'f'
    elif str(row)[0] in ['m', 'M']:
        return 'm'


general = pd.read_csv('test/general.csv')
prenatal = pd.read_csv('test/prenatal.csv')
sports = pd.read_csv('test/sports.csv')

# changing the col. names
prenatal.columns, sports.columns = list(general), list(general)

# merging into df named hospitals
hospitals = pd.concat([general, prenatal, sports], ignore_index=True)
hospitals.drop(columns=['Unnamed: 0'], inplace=True)

# del all the empty rows
hospitals = hospitals.dropna(how='all')
# replace NaNs
hospitals.fillna({'gender': 'f'}, inplace=True)
hospitals.loc[hospitals['gender'] == 'prenatal'] = hospitals.loc[hospitals['gender'] == 'prenatal'].fillna('f')
hospitals.fillna(0, inplace=True)
# unifying gender col.
hospitals['gender'] = hospitals['gender'].apply(gender_set)

# ans. "Which hospital has the highest number of patients?":
popular_hosp = hospitals.hospital.value_counts(sort=True).index[0]

# ans. "What share of the patients in the general hospital suffers from stomach-related issues?"
gen_stomach_count = hospitals.loc[(hospitals['hospital'] == 'general') & (hospitals['diagnosis'] == 'stomach')].shape[0]
gen_stomach_share = round(gen_stomach_count / hospitals.loc[hospitals['hospital'] == 'general'].shape[0], 3)

# ans. "What share of the patients in the sports hospital suffers from dislocation-related issues?"
sports_disl_count = \
    hospitals.loc[(hospitals['hospital'] == 'sports') & (hospitals['diagnosis'] == 'dislocation')].shape[0]
sports_disl_share = round(sports_disl_count / hospitals.loc[hospitals['hospital'] == 'sports'].shape[0], 3)

# ans. "What is the difference in the median ages of the patients in the general and sports hospitals?"
gen_median_ages_pivot = hospitals.pivot_table(index='hospital', values='age', aggfunc='median')
gen_sports_dif = int((gen_median_ages_pivot.loc['general'][0] - gen_median_ages_pivot.loc['sports'][0]))

# ans. "In which hospital the blood test was taken the most often?"
blood_taken = hospitals.loc[hospitals['blood_test'] == 't']
blood_test_pivot = blood_taken.pivot_table(index='hospital', values='blood_test', aggfunc='count').sort_values(
    by='blood_test', ascending=False)
blood_lead = blood_test_pivot.index[0]
how_many = blood_test_pivot.loc[blood_lead][0]

# print(f'The answer to the 1st question is {popular_hosp}'
# print(f'The answer to the 2nd question is {gen_stomach_share}'
# print(f'The answer to the 3rd question is {sports_disl_share}'
# print(f'The answer to the 4th question is {gen_sports_dif}'
# print(f'The answer to the 5th question is {blood_lead}, {how_many} blood tests')

plot1 = hospitals.plot(y='age', kind='hist', bins=10)
plt.show()

plot2 = hospitals['diagnosis'].value_counts().plot(kind='pie')
plt.show()

data = hospitals['height']
fig, axes = plt.subplots()
plt.violinplot(data)

plt.show()

print('The answer to the 1st question: 15-35')
print('The answer to the 2nd question: pregnancy')
print(
    "The answer to the 3rd question: It's because of a mismatch between the measurement system: metric and imperial "
    "systems.")
