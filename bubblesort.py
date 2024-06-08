n=[13,42,11,90,65,8,3,1]
for i in range(len(n)):
    swap=False
    for j in range(0,len(n)-i-1):
        if n[j]>n[j+1]:
            n[j],n[j+1]=n[j+1],n[j]
            swap=True
    if(swap==False):
        break

print(n)