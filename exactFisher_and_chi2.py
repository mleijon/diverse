#!/usr/bin/python

import scipy.stats as stats

oddsratio, pvalue = stats.fisher_exact([[1, 80], [4, 74]])
print(pvalue)
print('****')
ch2stat, ch2p = stats.chisquare([20, 22, 27, 7], f_exp=[15.1026, 28.7436, 23.3846, 8.7692], ddof=2)
print(ch2p)
