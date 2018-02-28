def removefreq():
    f=open('/home/razzaz/Desktop/Data/test/all.wfreq','r')
    f2=open('/home/razzaz/Desktop/Data/test/all.wfreq.uniq','w')
    for line in f:
        newl=line.split()[0]
        f2.write(newl+"\n")
    f2.flush()
    f2.close()
    f.close()
def diffrenceonly():
    f1=open("/home/razzaz/PycharmProjects/ArabicSpellchecker/Nim+feat+diacs+Qalb.uniq",'r')
    f2=open('/home/razzaz/PycharmProjects/ArabicSpellchecker/UniqWordsQalb','r')
    f3=open('/home/razzaz/PycharmProjects/ArabicSpellchecker/diffrence','w')
    f2lines=f2.readlines()
    for line in f1:
        if not line in f2lines:
            f3.write(line)
    f3.flush()
    f1.close()
    f2.close()
    f3.close()

# diffrenceonly()
removefreq()