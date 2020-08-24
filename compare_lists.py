with open('all-files.txt') as fi1:
    namelist_all = fi1.read().strip().split('\n')
with open('selected-files.txt') as fi2:
    namelist_sel = fi2.read().strip().split('\n\n')
namelist_all.sort()
namelist_sel.sort()
namelist_diff = list(set(namelist_all) - set(namelist_sel))
namelist_diff.sort()
with open('diff-files.txt', 'w') as out_file:
    for item in namelist_diff:
        out_file.write((item + '\n'))



