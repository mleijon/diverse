import subprocess
import os
rgi = '/home/micke/miniconda3/bin/rgi'
selected_dir = '/home/micke/unicycler-run2/assemblies_renamed/'
content = os.listdir(selected_dir)
print(content)
for item in content:
    infile = selected_dir + item
    outfile = selected_dir + item.split('.')[0]
    print(infile)
    print(outfile)
    subprocess.run(rgi + ' main' + ' -i ' + infile + ' -o ' + outfile, shell=True)
    exit()
