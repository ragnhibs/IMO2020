import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.cm as cm
import sys
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

sys.path.append('/div/qbo/users/ragnhibs/Python/')
print(sys.path)
import area_calcs_irregular

plt.rcParams['figure.dpi'] = 300

default_size = 10
plt.rc('font', size=default_size)


#def read_gridarea():
#    #OsloCTM3 gridarea
#    filearea = '/div/qbo/hydrogen/OsloCTM3/HYDROGEN_output/areacell_Amon_OsloCTM3_hydrogen-c1_r1_gn_201001-201012.nc'
#    area_data = xr.open_dataset(filearea)
#    print(area_data['areacell'].sum())
#    return area_data

def read_osloctm3():
    print('OsloCTM3')
    path_osloctm3 = '/div/qbo/utrics/IMO/OsloCTM3_RF/'

    #file_aod =  'OsloCTM3.imo.AOD.2010.nc'
    file_RFari = 'OsloCTM3.imo.dir.2010.nc'
    file_RFaci = 'OsloCTM3.imo.indir.2010.nc'
    data_RFari = xr.open_dataset(path_osloctm3+file_RFari)
    data_RFaci = xr.open_dataset(path_osloctm3+file_RFaci)
    print(data_RFari)
    print(data_RFaci)

    data_RFtot = data_RFaci.copy()
    data_RFtot['RFtot'] = data_RFaci['RF'] + data_RFari['RF'] 
    print(data_RFtot)

    areaxy_data = area_calcs_irregular.get_area(data_RFtot.lat,data_RFtot.lon)
    print(areaxy_data)
    areaxy  = xr.DataArray(areaxy_data,coords=dict(lat=data_RFtot.lat, lon=data_RFtot.lon), dims=("lat", "lon"))
    print(areaxy)

    
    if(True):
        fig, axs = plt.subplots(1, 2,squeeze=True,figsize=(12,3),
                                subplot_kw={'projection': ccrs.PlateCarree()})

        
        complist = ['RFari','RFaci']
                

        for ix,comp in enumerate(complist):
            ax = axs[ix]
            ax.set_global()
            ax.coastlines()
        
            if comp=='RFaci':
                levels = np.arange(0,0.40,0.05)
                im = data_RFaci['RF'].plot(ax=ax,vmin=levels[0],vmax=levels[-1],
                                           cmap=cmap,transform=ccrs.PlateCarree(),cbar_kwargs={'label': 'RF [W m$^{-2}$]'})
                weighted_rf = data_RFaci['RF'].weighted(areaxy)
                globalmean = weighted_rf.mean()
                print(globalmean)
                ax.set_title('b) ' + comp + ' [' + "{:.3f}".format(globalmean) + ' W m$^{-2}$]',loc='left')
            elif comp == 'RFari':
                levels = np.arange(0,0.12,0.05)
                im = data_RFari['RF'].plot(ax=ax,vmin=levels[0],vmax=levels[-1],
                                           cmap=cmap,transform=ccrs.PlateCarree(),cbar_kwargs={'label': 'RF [W m$^{-2}$]'})
                weighted_rf = data_RFari['RF'].weighted(areaxy)
                globalmean = weighted_rf.mean()
                print(globalmean)
                ax.set_title('a) ' + comp + ' [' + "{:.3f}".format(globalmean)+ ' W m$^{-2}$]', loc='left')

cmap = plt.get_cmap('OrRd')
read_osloctm3()

plt.tight_layout()

plt.savefig('figure_rf_osloctm.png') 


exit()
