d={}

for line in open("res.txt"):  
    if 'Expired' in line:
        name=line.split(', ')[0].split('\'')[1]
        count=line.split(', ')[2].split(']')[0]
        d[name]=int(count)
d_s=sorted(d.items(),key= lambda item:item[1],reverse=True)

