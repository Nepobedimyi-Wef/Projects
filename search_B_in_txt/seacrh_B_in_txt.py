file_read=open('ex1.txt').read().replace('A','').replace('C','').rfind('B',0)
if file_read > 0:
    print(file_read+1)
else:
    print('0')
