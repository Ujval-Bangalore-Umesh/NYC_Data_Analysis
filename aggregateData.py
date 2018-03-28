import pandas as pd
from matplotlib import pyplot as plt

member_df = pd.read_csv('/home/daram008/Minnemudac/member_information.csv')
lab_df = pd.read_csv('/home/daram008/Minnemudac/Training/labresults_training.csv')
medical_df = pd.read_csv('/home/daram008/Minnemudac/Training/medical_training.csv',low_memory = False)
rx_df = pd.read_csv('/home/daram008/Minnemudac/Training/rx_training.csv',low_memory = False)
confinement_df = pd.read_csv('/home/daram008/Minnemudac/Training/confinement_training.csv',low_memory = False)

lab_df_with_m  = pd.merge(member_df, lab_df, how='inner', on=list(lab_df.columns & member_df.columns),sort=True,\
         copy=True, indicator=False)

medical_df_with_m = pd.merge(member_df, medical_df, how='inner', on=list(member_df.columns & medical_df.columns),sort=True,\
         copy=True, indicator=False)

rx_df_with_m = pd.merge(member_df, rx_df, how='inner', on=list(member_df.columns & rx_df.columns),sort=True,\
         copy=True, indicator=False)

confinement_df_with_m = pd.merge(member_df, confinement_df, how='inner', on=list(member_df.columns & confinement_df.columns),sort=True,\
         copy=True, indicator=False)
         
del lab_df,medical_df,rx_df,confinement_df
#del lab_df_with_m,medical_df_with_m,rx_df_with_m,confinement_df_with_m

medical_df_with_m.year_of_birth = medical_df_with_m.year_of_birth.apply(lambda x: 2017-x)

med_costs_gender = medical_df_with_m.groupby(by = [u'gender'])[[u'STD_COST']].mean()

plt.figure()
plt.scatter(range(len(list(medical_df_with_m.gender.unique()))),med_costs_gender)
plt.show()

a = list(medical_df_with_m.year_of_birth.unique())
a.sort()

med_cost_age = medical_df_with_m.groupby(['year_of_birth'])[[u'STD_COST']].mean()


plt.figure()
plt.scatter(a,med_cost_age)
plt.show()


rx_df_with_m.year_of_birth = rx_df_with_m.year_of_birth.apply(lambda x: 2017-x)

rx_df_with_m.STD_COST = rx_df_with_m.STD_COST.apply(lambda x: 0 if (x == 'None') else x)
rx_df_with_m.STD_COST = rx_df_with_m.STD_COST.apply(lambda x: float(x))

rx_costs_gender = rx_df_with_m.groupby(by = [u'gender'])[[u'STD_COST']].mean()
plt.scatter(range(len(list(rx_df_with_m.gender.unique()))),rx_costs_gender)
plt.show()

rx_costs_age = rx_df_with_m.groupby(by = [u'year_of_birth'])[[u'STD_COST']].mean()

b = list(rx_df_with_m.year_of_birth.unique())
b.sort()
plt.scatter(b,rx_costs_age)
