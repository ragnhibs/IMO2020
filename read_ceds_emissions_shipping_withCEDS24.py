import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#CEDS emissions can be found from https://github.com/JGCRI/CEDS/
def read_ceds_24():
    emfile = 'SO2_CEDS_global_emissions_by_sector_v2024_04_01.csv'
    filepath ='/div/pdo/emissions/CEDS0424/TOTALS/CEDS_v_2024_04_01_aggregate/'
    
    data_emis = pd.read_csv(filepath+emfile,delimiter=',',index_col=None,header=0,skiprows=0).T
    
    
    print(data_emis)
    data_emis.rename(columns=data_emis.loc['sector'], inplace = True)
    print(data_emis)

    data_emis = data_emis.drop(['em','sector','units'])
    data_emis.index.name = 'Year'
    index = data_emis.index.values
    for i,year in enumerate(index):
        year = year.split("X")
        index[i] = year[-1]
    
    data_emis.index = index.astype(int)
        
    print(data_emis.columns)


    # ktSO2 -> Tg SO2
    data_emis = data_emis.mul(1000*1000*1000*1e-12)

    return data_emis



emfile = 'SO2_global_CEDS_emissions_by_sector_2021_04_21.csv'
filepath ='/div/pdo/emissions/CEDS0521/TOTALS/'

data_emis = pd.read_csv(filepath+emfile,delimiter=',',index_col=None,header=0,skiprows=0).T

print(data_emis)
data_emis.rename(columns=data_emis.loc['sector'], inplace = True)
print(data_emis)

data_emis = data_emis.drop(['em','sector','units'])
data_emis.index.name = 'Year'
index = data_emis.index.values
for i,year in enumerate(index):
    year = year.split("X")
    index[i] = year[-1]
    
data_emis.index = index.astype(int)

print(data_emis.columns)


# ktSO2 -> Tg SO2
data_emis = data_emis.mul(1000*1000*1000*1e-12)

ceds_v2021_int_shipping = data_emis['1A3di_International-shipping']
ceds_v2021_dom_shipping = data_emis['1A3dii_Domestic-navigation']
ceds_v2021_tot = data_emis.sum(axis=1)

#ceds_v2021.to_csv(fileout)
data_emis_24 = read_ceds_24()
ceds_v2024_int_shipping = data_emis_24['1A3di_International-shipping']
ceds_v2024_dom_shipping = data_emis_24['1A3dii_Domestic-navigation']
ceds_v2024_tot = data_emis_24.sum(axis=1)


fig, axs = plt.subplots(nrows=1,ncols=3,figsize=(15,5))
ax = axs[0]
ax.plot(ceds_v2024_tot,color='darkgray')#,label='Total ant. emissions')
ax.plot(ceds_v2024_int_shipping,color='lightblue')#,label='International shipping')
ax.plot(ceds_v2021_tot,color='black',label='Total ant. emissions')
ax.plot(ceds_v2021_int_shipping,color='navy',label='International shipping')

ax.set_xlim(left=1850)
ax.set_title('a)',loc='left')
ax.legend(frameon=False, loc='upper left')
ax.set_ylabel('Emissions [Tg SO$_2$]')

ax = axs[1]
ax.plot(ceds_v2024_int_shipping,color='lightblue')#,label='International shipping')
ax.plot(ceds_v2021_int_shipping,color='navy',label='International shipping')
abs_80red = ceds_v2021_int_shipping.loc[2019]*0.2
print('Emission Int-ship 2019')
print(ceds_v2021_int_shipping.loc[2019])
print('Emission Int-ship 2020 with 80% reduction')
print(abs_80red)
print('Emission reduction')
print(ceds_v2021_int_shipping.loc[2019]-abs_80red)
print('Emission reduction relative to total emissions')
print((ceds_v2021_int_shipping.loc[2019]-abs_80red)/ceds_v2021_tot.loc[2019]*100.0)


print('Relative emission reduction CEDS24: 2020, 2022')
print((ceds_v2024_int_shipping.loc[2019]-ceds_v2024_int_shipping.loc[2020])/ceds_v2024_int_shipping.loc[2019]*100.0)
print((ceds_v2024_int_shipping.loc[2019]-ceds_v2024_int_shipping.loc[2022])/ceds_v2024_int_shipping.loc[2019]*100.0)



ax.plot(2020,abs_80red,'*',color='navy',label='80% reduction')

ax.set_xlim(left=1950)
ax.set_title('b)',loc='left')
ax.legend(frameon=False)
ax.set_ylabel('Emissions [Tg SO$_2$]')


ax = axs[2]
rel = ceds_v2021_int_shipping.div(ceds_v2021_tot)*100.0
rel24 = ceds_v2024_int_shipping.div(ceds_v2024_tot)*100.0
ax.plot(rel24,color='lightblue')
ax.plot(rel,color='navy',label='International shipping')
rel_80red = abs_80red/ceds_v2021_tot.loc[2019]*100.0
print('Relative emissions 2019')
print(rel.loc[2019])
print('Relative emissions 2020')
print(rel_80red)
ax.plot(2020,rel_80red,'*',color='navy',label='80% reduction')
ax.set_xlim(left=1950)
ax.set_title('c)',loc='left')
ax.legend(frameon=False)
ax.set_ylabel('Relative to total [%]')




plt.show()
