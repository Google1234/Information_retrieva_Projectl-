
a=[5,5,6,6,6,6,6,7,7,7]
j1=j2=0
while j2<len(a):
    while j2<len(a) and a[j1]==a[j2]:
        j2+=1
    print  (a[j1],j2-j1)
    j1=j2