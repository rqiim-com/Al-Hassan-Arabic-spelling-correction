# # -*- coding: utf-8 -*-
f=open("/home/razzaz/Desktop/Data/diacs+nimlar.uniqs","r")
fout=open('/home/razzaz/Desktop/Data/diacs+nimlar.uniqs.preprocessed','w')

b=["ة","ه","ي","ى"]
c=["أ","ا","أ"]
for line in f:
    sp=line.split()
    check=1;
    if sp[0]=="الأحمقين":
        print sp
    if sp[0].startswith("ا"):
        if sp[0].startswith("ال"):
            if any(x == sp[0][2] for x in c):
                continue

        else:
            continue
    if any(z in line for z in c):
        if not line.startswith("ال") :
            continue
        else:
            xx=line.lstrip("ال")
            if any(l in xx for l in c):
                continue
    if any(sp[0].endswith(x) for x in b):
        continue
    fout.write(sp[0] + "\n")
fout.flush()
fout.close()
f.close()