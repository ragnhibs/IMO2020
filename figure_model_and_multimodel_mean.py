import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point


plt.rcParams['hatch.linewidth'] = 0.5

plt.rcParams['figure.dpi'] = 300

plt.rcParams['font.size'] = 8
plt.rcParams.update({'mathtext.default':  'regular' })

cmap = plt.get_cmap('bwr')
levels = np.arange(-0.8,0.8+0.1,0.1)

model_list = ['cesm','noresm','osloctm3','giss_oma','giss_matrix']

antmod = float(len(model_list))
print(antmod)


var_list = {'cesm':'ensmean',
            'noresm':'ensmean',
            'giss_oma':'ensmean',
            'giss_matrix':'ensmean',
            'osloctm3':'RFtot'}


model_list_dict = {'cesm': 'CESM2',
                   'noresm':'NorESM2',
                   'osloctm3':'OsloCTM3',
                   'giss_oma':'ModelE OMA',
                   'giss_matrix':'ModelE MATRIX'}


letter_list = ['a','b','c','d','e']
               

fig, axd = plt.subplot_mosaic(
    """
    abc
    de.
    ff.
    ff.
    """, figsize=(6,5), subplot_kw={'projection': ccrs.PlateCarree()}
)

    

    
for modnr,model in enumerate(model_list):
    print(model)
    data = xr.open_dataset('netcdf_files/ERF_modelmean_'+model+'.nc')
    data_regridded= xr.open_dataset('netcdf_files/regridded/ERF_modelmean_'+model+'.nc')
    var = var_list[model]
    #print(data_regridded)
    ax = axd[letter_list[modnr]]
    #ax = axs[0,modnr]
    ax.set_global()
    ax.coastlines()
    data[var].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(),add_colorbar=False)
    ax.set_title(letter_list[modnr] + ') '+model_list_dict[model],loc='left')

    #ax = axs[1,modnr]
    #ax.set_global()
    #ax.coastlines()
    #data_regridded[var].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree())

    data_regridded['sign'] = xr.where(data_regridded[var]<=0,data_regridded[var], 1)
    data_regridded['sign'] = xr.where(data_regridded[var]>0,data_regridded['sign'], 0)
    #ax = axs[2,modnr]
    #ax.set_global()
    #ax.coastlines()
    #data_regridded['sign'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree())
    
    #print(data_regridded['sign'])
    #exit()
    


    if modnr == 0:
        data_modelmean = data_regridded[var].squeeze()
        sign_modelmean = data_regridded['sign'].squeeze()
    else:
        data_modelmean = data_modelmean + data_regridded[var].squeeze()#.values
        sign_modelmean = sign_modelmean + data_regridded['sign'].squeeze()

print(sign_modelmean)



data_modelmean = data_modelmean/antmod
data_modelmean.name = 'multimodelmean'
print(data_modelmean)

axs  = axd['f']
axs.set_global()
axs.coastlines()
#data_modelmean.plot(ax=axs,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(),
#                    cbar_kwargs={'label': '[W m$^{-2}$]'})
cbar_ax = fig.add_axes([0.74,0.14,0.03,0.5])  #x0,y0,dx,dy #HER KAN DU SETTE POS OG STR FOR COLORBAREN
data_modelmean.plot(ax=axs,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(),
                    cbar_kwargs={'label': '[W m$^{-2}$]',"cax":cbar_ax})

#Bruke denne:
sign_lon = sign_modelmean.lon.values
sign_lat = sign_modelmean.lat.values

sign_data = sign_modelmean.values
sign_data, sign_lon = add_cyclic_point(sign_data, coord=sign_lon)
#axs.contourf(sign_lon,sign_lat,sign_data,levels=[0,1,4,5],colors='none',hatches=[None,'////',None],transform=ccrs.PlateCarree())

#Brukt i submission : axs.contourf(sign_lon,sign_lat,sign_data,levels=[0,1,4,5],colors='none',hatches=['...',None,'...'],transform=ccrs.PlateCarree())

#axs.contourf(sign_lon,sign_lat,sign_data,levels=[0,1,4,5],colors='none',hatches=['.....',None,'.....'],transform=ccrs.PlateCarree())

axs.contourf(sign_lon,sign_lat,sign_data,levels=[0,1,4,5],colors='none',hatches=['xxxx',None,'xxxx'],transform=ccrs.PlateCarree())

#axs.contourf(sign_lon,sign_lat,sign_data,levels=[0,1,4,5],colors='none',hatches=['////',None,'////'],transform=ccrs.PlateCarree())


#axs.contourf(sign_lon,sign_lat,sign_data,levels=[0,1,4,5],colors='none',hatches=[None,'////',None],transform=ccrs.PlateCarree())


"""

sign_modelmean.plot.contourf(ax=axs,levels=[0,1,4,5],colors='none',hatches=[None,'////',None],transform=ccrs.PlateCarree())
"""
print('Maxvalue')
print(data_modelmean.max())

[mlat,mlon] = data_modelmean.argmax(dim=["lat","lon"])
print(mlat)
print(mlon)
axs.set_title(' ')
axs.set_title('f) Multi model mean',loc='left')

#plt.tight_layout()
plt.savefig('figure_multimodel_mean_and_ens_mean.png')
#plt.show()
