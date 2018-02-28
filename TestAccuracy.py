# -*- coding: utf-8 -*-
import codecs
import random
import main
def RandomWordChange(word):
    uniqs=main.loadUniqWords("/home/razzaz/PycharmProjects/ArabicSpellchecker/uniqWords")
    letters=[u"أ",u"ب",u'ت',u'ث',u'ج',u'ح',u'خ',u'د',u'ذ',u'ر',u'ز',u'س',u'ش',u'ص',u'ض',u'ط',u'ظ',u'ع',u'غ',u'ف',u'ق',u'ك',u'ل',u'م',u'ن',u'ه',u'ي',"ا"]
    temp1=word
    while True:
        word=temp1
        if word.startswith(u"ا"):
            word= word.replace(u"ا",u"أ")
        if word.startswith(u"أ"):
            word= word.replace(u"أ",u"ا")
        x=random.randrange(0,len(word))
        z=random.randrange(0,2)
        y=random.randrange(0,len(letters))
        print x,y,z
        if z==0:
            word=word.remove(word[x])
        elif z==1:
            word=word.replace(word[x],letters[y])
        elif z==2:
            word.insert(x,letters[y])
        else:
            temp=word[x]
            word=word.replace(word[x],word[x+1])
            word=word.replace(word[x+1],temp)
        if not word in uniqs:
            return word
def createRandomScientence():
    print 1


orginalDataFile=codecs.open("/home/razzaz/Desktop/test","r",'utf-8')
falseDataFile=codecs.open("/home/razzaz/Desktop/test1","w",'utf-8')
for line in orginalDataFile:
    splited=line.strip().split()
    x=random.randrange(0, len(splited))
    falseWord=RandomWordChange(splited[x])
    del splited[x]
    splited.insert(x,falseWord)
    s="".join(z+" " for z in splited)
    falseDataFile.write(s+"\n")
