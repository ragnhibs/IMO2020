import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 300

default_size = 8
plt.rc('font', size=default_size)


#Just for OsloCTM3 results
df_erf = pd.read_csv('csv_files/erf_results.csv',sep=',',index_col=0)
print(df_erf['ERF'])



fig, axs = plt.subplots(nrows=1,ncols=1,figsize=(17/3,8/3))

plt.grid(axis='y', color='lightgray',zorder=0)



model_list = ['CESM2','ModelE_MATRIX','ModelE_OMA','NorESM2','OsloCTM3']
model_list_out = model_list

                  
print(model_list)
print(model_list_out)



label_mean = 'Mean'
label_95 = '95% CI'
label_90 = '90% CI'
label_66 = '66% CI'

df_model_mean = pd.DataFrame(data=[],index=['ens1','ens2'],columns=model_list)

for m, model in enumerate(model_list):
    if model=='OsloCTM3':
        axs.plot(m,df_erf['ERF'].loc[model],'o',color='Black',markersize=3)
        df_model_mean[model].iloc[0]=df_erf['ERF'].loc[model]
        continue
    
    df_erf_model = pd.read_csv('csv_files/'+model+'_results.csv',sep=';',index_col=0)
    print(df_erf_model)

    ens_shift=[-0.15,+0.15]
    for e,ens in enumerate(df_erf_model.columns):
        df_model_mean[model].iloc[e]=df_erf_model[ens].loc['Mean']
        axs.plot(m+ens_shift[e],df_erf_model[ens].loc['Mean'],'o',color='Black',
                 markersize=3,zorder=10,label=label_mean)
        label_mean = None
        
        axs.plot([m+ens_shift[e],m+ens_shift[e]],[df_erf_model[ens].loc['95low'],
                                                  df_erf_model[ens].loc['95upp']],
                 color='Black',linewidth=1,zorder=2,label=label_95)
        label_95 = None
        

        top =df_erf_model[ens].loc['90upp'] - df_erf_model[ens].loc['90low']
        bottom = df_erf_model[ens].loc['90low']
        axs.bar(m+ens_shift[e],top , 0.05, bottom=bottom, color='blue',linewidth=0,label=label_90,zorder=5)
        label_90 = None
        
        top =df_erf_model[ens].loc['66upp'] - df_erf_model[ens].loc['66low']
        bottom = df_erf_model[ens].loc['66low']
        axs.bar(m+ens_shift[e],top , 0.1, bottom=bottom, color='blue',tick_label=model,
                alpha=0.5,linewidth=0,zorder=2,label=label_66)
        label_66 = None
        
    


print('Max and min for all ensembles/model means')
df_model_mean.loc['ens_mean']= df_model_mean.mean()
print(df_model_mean)

print(df_model_mean.loc['ens_mean'].min())
print(df_model_mean.loc['ens_mean'].max())
print(df_model_mean.loc['ens_mean'].mean())

top = df_model_mean.loc['ens_mean'].max()-df_model_mean.loc['ens_mean'].min()
bottom = df_model_mean.loc['ens_mean'].min()
print(top)
print(bottom)
axs.bar(m+1,top,0.1,bottom=bottom, color='orange',
                alpha=0.5,linewidth=0,zorder=2,label='Model mean range')

axs.plot(m+1,df_model_mean.loc['ens_mean'].mean(),'d',color='Black',
                 markersize=3,zorder=-10,label='Multi-model mean')
print(model_list)


model_list_out.append('Multi-model')        

print(model_list_out)
plt.xticks(np.arange(len(model_list_out)),model_list_out, rotation=20)
axs.set_xlim([-1,6])
axs.set_ylim([-0.02,0.30])
axs.set_ylabel('ERF [W m$^{-2}$]')



handles, labels = plt.gca().get_legend_handles_labels()
#specify order of items in legend
order = [0,1,3,4,2,5]
#add legend to plot
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],frameon=True,ncol=3)


plt.tight_layout()



plt.savefig('figure_erf.png') #, transparent=True)
exit()
    
