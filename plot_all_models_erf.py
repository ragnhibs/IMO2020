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
import sys
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
sys.path.append('/div/qbo/users/ragnhibs/Python/')
print(sys.path)
import area_calcs_irregular

#
plt.rcParams['font.size'] = 6
plt.rcParams.update({'mathtext.default':  'regular' })

cmap = plt.get_cmap('bwr')
levels = np.arange(-1,1+0.2,0.2)

netcdf_output = 'netcdf_files/ERF_modelmean_'

def read_giss_oma():
    path_giss = '/div/nac/projects/shipping/GISS_output/cmap/'
    giss_oma_ens1 = 'E6omaF40c2000_SHP0p2_minus_CTL_1996_2045.nc'
    giss_oma_ens2 = 'E6omaF40c2010_SHP0p2_minus_CTL_1996_2045.nc'

    data_giss_oma_ens1 = xr.open_dataset(path_giss+giss_oma_ens1)
    data_giss_oma_ens2 = xr.open_dataset(path_giss+giss_oma_ens2)

    giss_oma_ens1 = data_giss_oma_ens1['FNT']
    giss_oma_ens2 = data_giss_oma_ens2['FNT']

    giss_oma_ens1.name = 'ens1'
    giss_oma_ens2.name = 'ens2'
    
    giss_oma_erf = xr.merge([giss_oma_ens1,giss_oma_ens2])
    

    return(giss_oma_erf)

def read_giss_matrix():
    path_giss = '/div/nac/projects/shipping/GISS_output/cmap/'
    giss_matrix_ens1 = 'E6matF40c2000_SHP0p2_minus_CTL_gnu_1996_2045.nc'
    giss_matrix_ens2 = 'E6matF40c2010_SHP0p2_minus_CTL_1996_2045.nc'

    data_giss_matrix_ens1 = xr.open_dataset(path_giss+giss_matrix_ens1)
    data_giss_matrix_ens2 = xr.open_dataset(path_giss+giss_matrix_ens2)

    giss_matrix_ens1 = data_giss_matrix_ens1['FNT']
    giss_matrix_ens2 = data_giss_matrix_ens2['FNT']

    giss_matrix_ens1.name = 'ens1'
    giss_matrix_ens2.name = 'ens2'
    
    giss_matrix_erf = xr.merge([giss_matrix_ens1,giss_matrix_ens2])
    

    return(giss_matrix_erf)

def read_noresm():
    path_noresm = '/div/no-backup-nac/users/raby/SHIPPING/'
    noresm_ens1 = 'NF2000climo_f19_AER2019_shpx0p2_96x144.nc'
    noresm_ens2 = 'NF2000climo_2010sst_f19_AER2019_shpx0p2_96x144.nc'
    
    data_noresm_ens1 = xr.open_dataset(path_noresm+noresm_ens1)
    data_noresm_ens2 = xr.open_dataset(path_noresm+noresm_ens2)

    #data_noresm_toa_net_erf = data_noresm_ens1['TOA_NET_ERF'].copy()
    noresm_ens1 = data_noresm_ens1['TOA_NET_ERF']
    noresm_ens2 = data_noresm_ens2['TOA_NET_ERF']

    noresm_ens1.name = 'ens1'
    noresm_ens2.name = 'ens2'
    
    noresm_erf = xr.merge([noresm_ens1,noresm_ens2])
    

    return(noresm_erf) #data_noresm_ens1['TOA_NET_ERF'],data_noresm_ens2['TOA_NET_ERF'])


def read_cesm():
    print('CESM')
    cesm_cataloge = {'BASE1':'F2000climof19_AER2019',
                     'SHIP1':'F2000climof19_AER2019_shpx0p2',
                     'BASE2':'F2000climo2010sstf19_AER2019b', 
                     'SHIP2':'F2000climo2010sstf19_AER2019_shpx0p2b'}

    timeperiod = {'BASE1':'200501-210412',
                  'SHIP1':'200501-210412',
                  'BASE2':'201001-210912', 
                  'SHIP2':'201001-210912'} 

    scen = 'BASE1'
    path_cesm = '/div/qbo/users/oivinho/CESM/output/'+cesm_cataloge[scen]+'/conv/'
    file_flnt = 'FLNT_Amon_F2000climof19_AER2019_CESM2_gn_'+timeperiod[scen]+'_timeavg.nc'
    file_fsnt = 'FSNT_Amon_F2000climof19_AER2019_CESM2_gn_'+timeperiod[scen]+'_timeavg.nc'

    data_flnt = xr.open_dataset(path_cesm+file_flnt)
    data_fsnt = xr.open_dataset(path_cesm+file_fsnt)
    
    
    data_net_base = data_fsnt['FSNT'] - data_flnt['FLNT']
    data_net_base.name='NET'

    scen = 'SHIP1'
    path_cesm = '/div/qbo/users/oivinho/CESM/output/'+cesm_cataloge[scen]+'/conv/'
    file_flnt = 'FLNT_Amon_F2000climof19_AER2019_shpx0p2_CESM2_gn_'+timeperiod[scen]+'_timeavg.nc'
    file_fsnt = 'FSNT_Amon_F2000climof19_AER2019_shpx0p2_CESM2_gn_'+timeperiod[scen]+'_timeavg.nc'

    data_flnt = xr.open_dataset(path_cesm+file_flnt)
    data_fsnt = xr.open_dataset(path_cesm+file_fsnt)

    data_net_ship = data_fsnt['FSNT'] - data_flnt['FLNT']
    data_net_ship.name='NET'

    cesm_ens1 = data_net_ship - data_net_base
    cesm_ens1.name = 'ens1'
    print(cesm_ens1)


    scen = 'BASE2'
    path_cesm = '/div/qbo/users/oivinho/CESM/output/'+cesm_cataloge[scen]+'/conv/'
    file_flnt = 'FLNT_Amon_F2000climo2010sstf19_AER2019b_CESM2_gn_'+timeperiod[scen]+'_timeavg.nc'
    file_fsnt = 'FSNT_Amon_F2000climo2010sstf19_AER2019b_CESM2_gn_'+timeperiod[scen]+'_timeavg.nc'

    data_flnt = xr.open_dataset(path_cesm+file_flnt)
    data_fsnt = xr.open_dataset(path_cesm+file_fsnt)

    data_net_base = data_fsnt['FSNT'] - data_flnt['FLNT']
    data_net_base.name='NET'

    scen = 'SHIP2'
    path_cesm = '/div/qbo/users/oivinho/CESM/output/'+cesm_cataloge[scen]+'/conv/'
    file_flnt = 'FLNT_Amon_F2000climo2010sstf19_AER2019_shpx0p2b_CESM2_gn_'+timeperiod[scen]+'_timeavg.nc'
    file_fsnt = 'FSNT_Amon_F2000climo2010sstf19_AER2019_shpx0p2b_CESM2_gn_'+timeperiod[scen]+'_timeavg.nc'

    data_flnt = xr.open_dataset(path_cesm+file_flnt)
    data_fsnt = xr.open_dataset(path_cesm+file_fsnt)

    data_net_ship = data_fsnt['FSNT'] - data_flnt['FLNT']
    data_net_ship.name='NET'

    cesm_ens2 = data_net_ship - data_net_base
    cesm_ens2.name = 'ens2'
    print(cesm_ens2)
    cesm_ens2 = cesm_ens2.drop("time")
    cesm_ens1 = cesm_ens1.drop("time")
    print(cesm_ens2)
    cesm_erf = xr.merge([cesm_ens1,cesm_ens2])
    print(cesm_erf)
    
    return(cesm_erf)


def read_osloctm3():
    print('OsloCTM3')
    path_osloctm3 = '/div/qbo/utrics/IMO/OsloCTM3_RF/'

    file_aod =  'OsloCTM3.imo.AOD.2010.nc'
    file_RFari = 'OsloCTM3.imo.dir.2010.nc'
    file_RFaci = 'OsloCTM3.imo.indir.2010.nc'
    data_RFari = xr.open_dataset(path_osloctm3+file_RFari)
    data_RFaci = xr.open_dataset(path_osloctm3+file_RFaci)
    print(data_RFari)
    print(data_RFaci)

    data_RFtot = data_RFaci.copy()
    data_RFtot['RFtot'] = data_RFaci['RF'] + data_RFari['RF'] 
    print(data_RFtot)

    if(False):
        fig, axs = plt.subplots(1, 3,squeeze=True,figsize=(19,5),
                                subplot_kw={'projection': ccrs.PlateCarree()})

        levels = np.arange(0,0.55,0.05)
        complist = ['RFtot','RFari','RFaci']
        print(levels)
        

        for ix,comp in enumerate(complist):
            ax = axs[ix]
            ax.set_global()
            ax.coastlines()
        
            
            if comp=='RFtot':
                im = data_RFtot['RFtot'].plot(ax=ax,vmin=levels[0],vmax=levels[-1],cmap=cmap,transform=ccrs.PlateCarree())
            elif comp=='RFaci':
                im = data_RFaci['RF'].plot(ax=ax,vmin=levels[0],vmax=levels[-1],cmap=cmap,transform=ccrs.PlateCarree())
            elif comp == 'RFari':
                im = data_RFari['RF'].plot(ax=ax,vmin=levels[0],vmax=levels[-1],cmap=cmap,transform=ccrs.PlateCarree())
            ax.set_title(comp)
            #cax = fig.add_axes([0.92, 0.1, 0.01, 0.75])
            #cbar = fig.colorbar(im, cax=cax, format='%.3f',shrink=0.6) #cbar_kwargs={
            #cbar.set_label('W m-2', labelpad=-60, y=1.05, rotation=0)
        
        #plt.show()

    return(data_RFtot['RFtot'])
    

#Start read and plot model results:

erf_cesm = read_cesm()
erf_cesm['ensmean'] = 0.5 * (erf_cesm['ens1'] + erf_cesm['ens2'])
print(erf_cesm['ensmean'])
erf_cesm['ensmean'].to_netcdf(netcdf_output+'cesm.nc')
#erf_cesm.to_netcdf(netcdf_output+'cesm.nc')

erf_noresm = read_noresm()
print(erf_noresm)

erf_noresm['ensmean'] = 0.5 *(erf_noresm['ens1'] + erf_noresm['ens2'])
print(erf_noresm) #['ensmean'])
outfelt = erf_noresm['ensmean']
print(outfelt)
outfelt.to_netcdf(netcdf_output+'noresm.nc')
erf_noresm.to_netcdf(netcdf_output+'noresm.nc')


erf_giss_oma = read_giss_oma()
erf_giss_oma['ensmean'] = 0.5 *(erf_giss_oma['ens1'] + erf_giss_oma['ens2'])
erf_giss_oma['ensmean'].to_netcdf(netcdf_output+'giss_oma.nc')

erf_giss_matrix = read_giss_matrix()
erf_giss_matrix['ensmean'] = 0.5 *(erf_giss_matrix['ens1'] + erf_giss_matrix['ens2'])
erf_giss_matrix['ensmean'].to_netcdf(netcdf_output+'giss_matrix.nc')

rftot_osloctm3 = read_osloctm3()
print(rftot_osloctm3)
rftot_osloctm3.to_netcdf(netcdf_output+'osloctm3.nc')

ens = ['ens1','ens2','ensmean']
fig, axs = plt.subplots(5, 3,squeeze=True,figsize=(8,5),
                                subplot_kw={'projection': ccrs.PlateCarree()})
modnr = 0
model='CESM2'
ensnr = 0
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_cesm['ens1'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model+ ' ' + ens[ensnr])

ensnr = 1
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_cesm['ens2'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model+ ' ' + ens[ensnr])

ensnr = 2
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_cesm['ensmean'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model+ ' ' + ens[ensnr])

modnr = 1
model='ModelE_MATRIX'
ensnr = 0
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_giss_matrix['ens1'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model+ ' ' + ens[ensnr])

ensnr = 1
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_giss_matrix['ens2'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model + ' ' + ens[ensnr])

ensnr =2
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_giss_matrix['ensmean'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model+ ' ' + ens[ensnr])

modnr = 2
model='ModelE_OMA'
ensnr = 0
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_giss_oma['ens1'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model+ ' ' + ens[ensnr])

ensnr = 1
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_giss_oma['ens2'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model + ' ' + ens[ensnr])

ensnr =2
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_giss_oma['ensmean'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model+ ' ' + ens[ensnr])


modnr = 3
model='NorESM2'
ensnr = 0
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_noresm['ens1'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model+ ' ' + ens[ensnr])

ensnr = 1
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_noresm['ens2'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model + ' ' + ens[ensnr])

ensnr =2
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = erf_noresm['ensmean'].plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model+ ' ' + ens[ensnr])


modnr = 4
model='OsloCTM3'
axs[modnr,0].axis('off')
axs[modnr,1].axis('off')
ensnr = 2
ax = axs[modnr,ensnr]
ax.set_global()
ax.coastlines()
im = rftot_osloctm3.plot(ax=ax,cmap=cmap,levels=levels,transform=ccrs.PlateCarree(), cbar_kwargs={'label': None})
ax.set_title(model)





plt.tight_layout()
plt.show()
exit()
