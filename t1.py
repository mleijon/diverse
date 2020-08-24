with open('evales.txt') as fi:
    temp_lst = fi.read().split('Expect = e-')[1:]
numbers = [int(x.split('\n')[0]) for x in temp_lst]
print(min(numbers))
