#Plot annual mean surface concentration
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.cm as cm
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)



#
plt.rcParams['font.size'] = 8
plt.rcParams.update({'mathtext.default':  'regular' })


######################
def read_gridarea():
    #OsloCTM3 gridarea
    filearea = '/div/qbo/hydrogen/OsloCTM3/HYDROGEN_output/areacell_Amon_OsloCTM3_hydrogen-c1_r1_gn_201001-201012.nc'
    area_data = xr.open_dataset(filearea)
    print(area_data['areacell'].sum())
    return area_data

def read_osloctm_annual(file,filepath,comp):
    data = xr.open_dataset(filepath+file)
    print(data)

    month_length = data.time.dt.days_in_month
    print(month_length)

    weighted_data= data.weighted(month_length)


    #Annual mean:
    annual_data= weighted_data.mean(dim='time')
    
    #Convert unit #kg-> micro: 
    factor = 1e9 #convert from kg to mikrogram
    annual_data = annual_data*factor

    return annual_data


def plot_osloctm_abs():
    titletext = letter + ' ' + str(startyr) + ' vs. ' + str(endyear)
    
    file_pert = comp+'_Amon_OsloCTM3_'+project+'-'+str(endyear)+'_r1_gn_201001-201012.nc'
    annual_data_pert = read_osloctm_annual(file=file_pert, filepath=filepath, comp=comp)
    
    file_cntr = comp+'_Amon_OsloCTM3_'+project+'-'+str(startyr)+'_r1_gn_201001-201012.nc'
    annual_data_cntr = read_osloctm_annual(file=file_cntr, filepath=filepath, comp=comp)
    
    plottfelt = annual_data_pert[comp].isel(lev=lev_niv)-annual_data_cntr[comp].isel(lev=lev_niv)

    #Per Year:
    plottfelt = plottfelt/float(endyear-startyr)
   
    plottfelt.plot(ax=ax,levels=levels,cmap=cmap,transform=ccrs.PlateCarree(),cbar_kwargs={'label': labeltext})
    ax.coastlines()
    ax.set_title(titletext)
    ax.set_global()
"""
def plot_osloctm_varmet_abs():
    titletext = str(startyr) + ' vs. ' + str(endyear)
    
    file_pert = 'OsloCTM3.v1.01b.'+str(endyear)+'_CMIP6.'+comp+'.modellevel.monthly.nc'
    annual_data_pert = read_osloctm_annual(file=file_pert, filepath=filepath,comp=comp)
    
    file_cntr = 'OsloCTM3.v1.01b.'+str(startyr)+'_CMIP6.'+comp+'.modellevel.monthly.nc'
    annual_data_cntr = read_osloctm_annual(file=file_cntr, filepath=filepath,comp=comp)
    
    plottfelt = annual_data_cntr[comp].isel(lev=lev_niv)-annual_data_pert[comp].isel(lev=lev_niv)

    #Per Year:
    plottfelt = plottfelt/float(startyr-endyear)
    plottfelt.plot(ax=ax,levels=levels,cmap=cmap,transform=ccrs.PlateCarree())
    ax.coastlines()
    ax.set_title(titletext)
    #ax.set_title(comp + ' abs. diff. ' + titletext)
    ax.set_global()
"""
    
#####################

comp = 'mmrso4'
labeltext = comp + ' yr$^{-1}$'
crange = [-30,0]

levels = np.arange(-0.1,0.11,0.01)
#Surfconc
lev_niv = 0

area_data = read_gridarea()


#Start plotting:
cmap = plt.get_cmap('BrBG')
fig, axs = plt.subplots(2,4,squeeze=True,figsize=(20,6),
                                subplot_kw={'projection': ccrs.PlateCarree()})

project='hist_fixed'
filepath = '/div/pdo/histO3/OUTPUT/'
ax = axs[0,0]
letter = 'a)'
startyr = 1990
endyear = 2000
plot_osloctm_abs()


project='hist_met2010_ceds21'
filepath = '/div/qbo/utrics/OsloCTM3/CTM3results/histO3/OUTPUT/'

ax = axs[0,1]
letter = 'b)'
startyr = 2000
endyear = 2007
plot_osloctm_abs()

letter = 'c)'
ax = axs[0,2]
startyr = 2007
endyear = 2014
plot_osloctm_abs()

letter = 'd)'
ax = axs[0,3]
startyr = 2014
endyear = 2019
plot_osloctm_abs()

letter = 'e)'
ax = axs[1,0]
project = 'imo_vertship'
filepath = '/div/qbo/utrics/OsloCTM3/CTM3results/IMO/OUTPUT/'

titletext = 'IMO 2020 vs. 2019'

file_pert =  comp+'_Amon_OsloCTM3_'+project+'-20perc_r1_gn_201001-201012.nc'

annual_data_pert = read_osloctm_annual(file=file_pert, filepath=filepath,comp=comp)

file_cntr = comp+'_Amon_OsloCTM3_'+project+'-cntr_r1_gn_201001-201012.nc'
annual_data_cntr = read_osloctm_annual(file=file_cntr, filepath=filepath,comp=comp)

plottfelt = annual_data_pert[comp].isel(lev=lev_niv)-annual_data_cntr[comp].isel(lev=lev_niv)
plottfelt.plot(ax=ax,levels=levels,cmap=cmap,transform=ccrs.PlateCarree(), cbar_kwargs={'label': labeltext})
ax.coastlines()
ax.set_title(letter + ' ' + titletext)
ax.set_global()



letter = 'f)'
ax = axs[1,1]
startyr = 1990
endyear = 2019
titletext = letter + ' ' + str(startyr) + ' vs. ' + str(endyear)

project='hist_met2010_ceds21'
filepath = '/div/qbo/utrics/OsloCTM3/CTM3results/histO3/OUTPUT/'
file_pert = comp+'_Amon_OsloCTM3_'+project+'-'+str(endyear)+'_r1_gn_201001-201012.nc'
annual_data_pert = read_osloctm_annual(file=file_pert, filepath=filepath, comp=comp)

project='hist_fixed'
filepath = '/div/pdo/histO3/OUTPUT/'
file_cntr = comp+'_Amon_OsloCTM3_'+project+'-'+str(startyr)+'_r1_gn_201001-201012.nc'
annual_data_cntr = read_osloctm_annual(file=file_cntr, filepath=filepath, comp=comp)

plottfelt = annual_data_pert[comp].isel(lev=lev_niv)-annual_data_cntr[comp].isel(lev=lev_niv)

#Per Year:
plottfelt = plottfelt

plottfelt.plot(ax=ax,levels=levels,cmap=cmap,transform=ccrs.PlateCarree(),cbar_kwargs={'label': comp})
ax.coastlines()
ax.set_title(titletext)
ax.set_global()


letter = 'g)'
ax = axs[1,2]
startyr = 2000
endyear = 2019
titletext = letter + ' ' + str(startyr) + ' vs. ' + str(endyear)

project='hist_met2010_ceds21'
filepath = '/div/qbo/utrics/OsloCTM3/CTM3results/histO3/OUTPUT/'
file_pert = comp+'_Amon_OsloCTM3_'+project+'-'+str(endyear)+'_r1_gn_201001-201012.nc'
annual_data_pert = read_osloctm_annual(file=file_pert, filepath=filepath, comp=comp)

file_cntr = comp+'_Amon_OsloCTM3_'+project+'-'+str(startyr)+'_r1_gn_201001-201012.nc'
annual_data_cntr = read_osloctm_annual(file=file_cntr, filepath=filepath, comp=comp)

plottfelt = annual_data_pert[comp].isel(lev=lev_niv)-annual_data_cntr[comp].isel(lev=lev_niv)

#Per Year:
plottfelt = plottfelt

plottfelt.plot(ax=ax,levels=levels,cmap=cmap,transform=ccrs.PlateCarree(),cbar_kwargs={'label': comp})
ax.coastlines()
ax.set_title(titletext)
ax.set_global()


letter = 'h)'
ax = axs[1,3]
startyr = 2007
endyear = 2019
titletext = letter + ' ' + str(startyr) + ' vs. ' + str(endyear)

project='hist_met2010_ceds21'
filepath = '/div/qbo/utrics/OsloCTM3/CTM3results/histO3/OUTPUT/'
file_pert = comp+'_Amon_OsloCTM3_'+project+'-'+str(endyear)+'_r1_gn_201001-201012.nc'
annual_data_pert = read_osloctm_annual(file=file_pert, filepath=filepath, comp=comp)

file_cntr = comp+'_Amon_OsloCTM3_'+project+'-'+str(startyr)+'_r1_gn_201001-201012.nc'
annual_data_cntr = read_osloctm_annual(file=file_cntr, filepath=filepath, comp=comp)

plottfelt = annual_data_pert[comp].isel(lev=lev_niv)-annual_data_cntr[comp].isel(lev=lev_niv)

#Per Year:
plottfelt = plottfelt

plottfelt.plot(ax=ax,levels=levels,cmap=cmap,transform=ccrs.PlateCarree(),cbar_kwargs={'label': comp})
ax.coastlines()
ax.set_title(titletext)
ax.set_global()

#axs[1,2].axis('off')
#axs[1,3].axis('off') 


plt.show()
exit()


