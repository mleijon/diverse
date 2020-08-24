data_lst = []
with open('test2.txt') as fi1:
    input_text1 = fi1.read()
with open('order.txt') as fi2:
    input_test2 = fi2.read()
order_lst = input_test2.split('\n')
elements = input_text1.split('unicycler-run2\\')
for item in elements[1:]:
    data_lst.append([item.split('\n')[0],
                     item.split('\n')[5].strip().split(' ')[-2]])
with open('size.txt', 'w') as fi3:
    for strain in order_lst:
        for item in data_lst:
            if item[0] == strain:
                fi3.write(item[1] + '\n')
                continue
