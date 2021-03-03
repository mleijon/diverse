import os
selected_dir = '/home/micke/unicycler-run2/'
content = os.listdir(selected_dir)
content_dir = []
for item in content:
    if os.path.isdir(selected_dir + item):
        content_dir.append(item)
    else:
        with open(selected_dir + item) as f:
            valid_samples = f.read().split()
for item in content_dir:
    if 'assembly.fasta' in os.listdir(selected_dir + item) and item in \
            valid_samples:
        new_name = selected_dir + 'assemblies_renamed/' + item + '.fasta'
        os.rename(selected_dir + item + '/assembly.fasta', new_name)

