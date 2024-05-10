import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point


plt.rcParams['figure.dpi'] = 300

plt.rcParams['font.size'] = 8
plt.rcParams.update({'mathtext.default':  'regular' })

cmap = plt.get_cmap('bwr')
levels = np.arange(-0.8,0.8+0.1,0.1)

#fig, axs = plt.subplots(3, 5,squeeze=True,figsize=(15,3),
#                               subplot_kw={'projection': ccrs.PlateCarree()})
model_list = ['cesm','noresm','osloctm3','giss_oma','giss_matrix']

antmod = float(len(model_list))
print(antmod)


var_list = {'cesm':'ensmean',
            'noresm':'ensmean',
            'giss_oma':'ensmean',
            'giss_matrix':'ensmean',
            'osloctm3':'RFtot'}

for modnr,model in enumerate(model_list):
    print(model)
    data = xr.open_dataset('netcdf_files/ERF_modelmean_'+model+'.nc')
    data_regridded= xr.open_dataset('netcdf_files/regridded/ERF_modelmean_'+model+'.nc')
    var = var_list[model]
    #print(data_regridded)
    
#    ax = axs[0,modnr]
#    ax.set_global()
#    ax.coastlines()
#    data[var].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree())
#    ax.set_title(model)

#    ax = axs[1,modnr]
#    ax.set_global()
#    ax.coastlines()
#    data_regridded[var].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree())

    data_regridded['sign'] = xr.where(data_regridded[var]<=0,data_regridded[var], 1)
    data_regridded['sign'] = xr.where(data_regridded[var]>0,data_regridded['sign'], 0)
#    ax = axs[2,modnr]
#    ax.set_global()
#    ax.coastlines()
#    data_regridded['sign'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree())
    
    #print(data_regridded['sign'])
    #exit()
    
#    ax.set_title(model)

    if modnr == 0:
        data_modelmean = data_regridded[var].squeeze()
        sign_modelmean = data_regridded['sign'].squeeze()
    else:
        data_modelmean = data_modelmean + data_regridded[var].squeeze()#.values
        sign_modelmean = sign_modelmean + data_regridded['sign'].squeeze()

print(sign_modelmean)

#plt.savefig('figure_models_erf_sign.png')

data_modelmean = data_modelmean/antmod
data_modelmean.name = 'multimodelmean'
print(data_modelmean)
fig, axs = plt.subplots(1, 1,squeeze=True,figsize=(8,3),
                                subplot_kw={'projection': ccrs.PlateCarree()})
axs.set_global()
axs.coastlines()
data_modelmean.plot(ax=axs,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(),
                    cbar_kwargs={'label': 'Multimodel mean [W m$^{-2}$]'})


sign_lon = sign_modelmean.lon.values
sign_lat = sign_modelmean.lat.values

sign_data = sign_modelmean.values
sign_data, sign_lon = add_cyclic_point(sign_data, coord=sign_lon)

axs.contourf(sign_lon,sign_lat,sign_data,levels=[0,1,4,5],colors='none',hatches=['...',None,'...'],transform=ccrs.PlateCarree())


print('Maxvalue')
print(data_modelmean.max())

[mlat,mlon] = data_modelmean.argmax(dim=["lat","lon"])
print(mlat)
print(mlon)
axs.set_title('')

plt.savefig('figure_multimodel_mean.png')
#plt.show()
