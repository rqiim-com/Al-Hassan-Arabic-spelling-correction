# -*- coding: utf-8 -*-

import sys
import codecs
import multiprocessing
reload(sys)
sys.setdefaultencoding('utf8')
# lettersSet=['؛','؟','،',' ',"'"," ","|",">","&","<","}","A","b","p","t","v","j","H","x","d","*","r","z","s","$","S","D","T","Z","E","g","_","f","q","k","l","m","n","h","w","Y","y","`","{","P","J","V","G"]
# file=codecs.open('/home/razzaz/Desktop/Data/lmData/all/allTotrainLM.txt.clean.newBuck',"r",'utf-8')
# out=codecs.open('/home/razzaz/Desktop/Data/lmData/all/allTotrainLM.txt.clean.newBuck.arabiconly','w')
# outout=codecs.open('/home/razzaz/Desktop/Data/lmData/all/outchar','w',encoding='utf-8')


# for line in file:
#     result={}

#
#     splited = line.replace('\t',' ').replace('؟',' ؟ ').replace('،',' ، ').replace('؛',' ؛ ').replace('.',' . ').replace(",",' , ').replace('  ',' ').replace(',',' , ').split(' ')
#     for word in splited:
#         for char in word:
#             if char in lettersSet:
#                 out.write(char)
#             else:
#                 outout.write(char)
#                 outout.write('\n')
#         out.write(' ')
#         outout.write(' ')
#     out.write('\n')
#     outout.flush()
#     out.flush()
# out.close()
#
result = {}
lettersSet = [".","؟" ,"،" ,"؛" ,"“" ,'‘','؛', '؟', '،', ' ', "'", " ", "|", ">", "&", "<", "}", "A", "b", "p", "t", "v", "j", "H", "x", "d",
                      "*", "r", "z", "s", "$", "S", "D", "T", "Z", "E", "g", "_", "f", "q", "k", "l", "m", "n", "h", "w",
                      "Y", "y", "`", "{", "P", "J", "V", "G"]

def RemoveNonArabic(lines):

    for line in lines:
        line=str(line)
        outLine=''
        splited = line.replace('\t', ' ').replace('؟', ' ؟ ').replace('،', ' ، ').replace('؛', ' ؛ ').replace('.',' . ').replace(",", ' , ').replace('  ', ' ').replace(',', ' , ').split(' ')
        for word in splited:
            for char in word:
                if char in lettersSet:
                    outLine+=char
            outLine+=" "
        result[outLine]=True
    return result

def printNum(z,x):
    print str(z) + '\t'+str(x)

if __name__ == '__main__':
    # configurable options.  different values may work better.
    numthreads = 8
    numlines = 100000
    dataPath='/home/razzaz/Desktop/Data/FeaturedArticleFromRaqim/allRowText.txt.buck'
    out = codecs.open('/home/razzaz/Desktop/Data/FeaturedArticleFromRaqim/all.utf8.buck.arabiconly', 'w')
    lines = open(dataPath,'r').readlines()
    # create the process pool
    pool = multiprocessing.Pool(processes=numthreads)

    result_list = pool.imap(RemoveNonArabic, (lines[linenum:linenum + numlines] for linenum in xrange(0, len(lines), numlines)))
    pool.close()
    pool.join()

    print ('mapping was finished')
    map(result.update, result_list)
    print ('Finished')
    print (len(result))

for kline in result.keys():
    if(str(kline).strip().replace("​\n",'')==''):
        continue
    out.write(str(kline))
    out.write('\n')
out.flush()
out.close()
# file.close()