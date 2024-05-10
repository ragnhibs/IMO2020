import subprocess
import glob

print('Start!')

files = '*.nc'
len_path= len(files)
mylist = [f for f in glob.glob(files)]
print(mylist)


for i in range(len(mylist)):
    infile = mylist[i]
    print(infile)
    outfile =  'regridded/'+infile
    print(outfile)

    cmdl = 'cdo remapbil,ERF_modelmean_cesm.nc ' + infile +' ' + outfile
    print(cmdl)
    print(subprocess.run(cmdl, capture_output=True, shell=True))
