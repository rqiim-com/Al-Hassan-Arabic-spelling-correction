f=open("/home/razzaz/Desktop/Data/lmData/all/allTotrainLM.reTaskeel.clean.buck.arabiconly_buck","r")
f2=open('/home/razzaz/Desktop/Data/lmData/all/allTotrainLM.reTaskeel.clean.buck.arabiconly_buck.lm','w')
for line in f:
    line="<s> "+line.strip('\n').strip()+" <\s>\n"
    f2.write(line)
f2.flush()
f2.close()
f.close()