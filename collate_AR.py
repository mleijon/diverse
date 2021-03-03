import os
cc133 = ['133']
cc705 = ['705', '3140', '504', '151']
cc97 = ['97', '71', '697', '352']
selected_dir = '/home/micke/unicycler-run2/assemblies_renamed/rgi_results/txt/'
outfile1 = selected_dir.split('txt', 1)[0] + 'collated.txt'
outfile2 = selected_dir.split('txt', 1)[0] + 'mutations.txt'
st_file = selected_dir.split('txt', 1)[0] + 'sample_STs.csv'
content = os.listdir(selected_dir)
sample2st = dict()
sample2cc = dict()
with open(st_file) as f:
    for item in f.readlines():
        sample2st[item.split()[0]] = item.split()[1]
        if item.split()[1] in cc133:
            sample2cc[item.split()[0]] = '133'
        elif item.split()[1] in cc705:
            sample2cc[item.split()[0]] = '705'
        elif item.split()[1] in cc97:
            sample2cc[item.split()[0]] = '97'
        else:
            sample2cc[item.split()[0]] = 'other'
with open(outfile1, 'w') as out_f1, open(outfile2, 'w') as out_f2:
    for sample in content:
        sample_name = sample.split('.txt')[0]
        sample_st = sample2st[sample_name]
        sample_cc = sample2cc[sample_name]
        out_f1.write('{}\t{}\t{}\t'.format(sample_name, sample_st, sample_cc))
        out_f2.write('{}\t{}\t{}\t'.format(sample_name, sample_st, sample_cc))
        sample_file = selected_dir + sample
        with open(sample_file) as f:
            rgi_result = f.readlines()[1:]
            for gene in rgi_result:
                out_f1.write('{}\t'.format(gene.split('\t')[8]))
                if 'mutation' in gene.split('\t')[8]:
                    out_f2.write('{}\t'.format(gene.split('\t')[8]))
                    out_f2.write('{}\t'.format(gene.split('\t')[12]))
            out_f1.write('\n')
            out_f2.write('\n')

