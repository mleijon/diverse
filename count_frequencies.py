import matplotlib.pyplot as plt
data_lst = []
with open('amp_length.txt') as fi:
    for item in fi:
        data_lst.append(int(item.strip()))
plt.style.use('ggplot')
plt.hist(data_lst, bins=100, range=(400, 500))
plt.show()