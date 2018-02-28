# -*- coding: utf-8 -*-
import  ReadData
import multiprocessing
import time
import sys
from datetime import datetime
import codecs
import os
ii=0
similarityDic={}

def __init__(self,wordlist):
    self.dic=wordlist

def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    if abs(lenstr1-lenstr2)>1:
        return float("inf")
    for i in xrange(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in xrange(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            transpositionCost=1
            if s1[i] == s2[j]:
                cost = 0
            elif isSimilar(s1[i],s2[j]):
                cost=1
            else:
                cost = 2
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )


            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + transpositionCost)  # transposition

    return d[lenstr1 - 1, lenstr2 - 1]

def cluster(dic):
    indexLog=0
    D=list(dic)

    C={}
    while  len(D)!=0 :
        print indexLog
        t=len(D)
        G=list(D)
        i=0

        M=[]
        for j in range(0,t):
            if levenshtein(G[i],D[j])==1:
                M.append(D[j])
        D.remove(G[i])
        indexLog+=1
        if len(M) != 0:

            for word in M:
                D.remove(word)
                indexLog+=1
        try:

            C[G[i]]=M
            i+=1
        except IndexError:
            print 'error'
    return C
def levenshtein(word1, word2):

    columns = len(word1) + 1
    rows = len(word2) + 1
    if abs(columns-rows)>1:
        return 10
    # build first row
    currentRow = [0]
    for column in xrange(1, columns):
        currentRow.append(currentRow[column - 1] + 1)

    for row in xrange(1, rows):
        previousRow = currentRow
        currentRow = [previousRow[0] + 1]

        for column in xrange(1, columns):

            insertCost = currentRow[column - 1] + 1
            deleteCost = previousRow[column] + 1

            if word1[column - 1] != word2[row - 1]:
                cost=2
                if isSimilar(word1[column - 1],word2[row - 1]):
                    cost=1
                replaceCost = previousRow[column - 1] + cost
            else:
                replaceCost = previousRow[column - 1]

            currentRow.append(min(insertCost, deleteCost, replaceCost))

    return currentRow[-1]
def search(TARGET,words, maxCost):
    results = []
    for word in words:
        cost = levenshtein(TARGET, word)

        if cost <= maxCost:
            results.append((word, cost))

    return results

def newClustering(wordsUniq):
    C = {}
    MAX_COST = 1
    i=0
    for word in wordsUniq:
        print i
        TARGET =word
        results = search(TARGET,wordsUniq, MAX_COST)
        C[word]=results
        i+=1
    return C

def WordsNighbors(words):
        C={}
        for word in words:
            M=[]
            for uWord in uniqWordsset:
                dist=levenshtein(word,uWord)
                if dist==1:
                    M.append(uWord)

            C[word]=M
        return C



def writeClustredDic(dic,path):
    dict(dic)
    outFile=open(path,'w')
    for centeriod in dic:
        outFile.write(centeriod)
        for word in dic[centeriod]:
            outFile.write(" "+word)
        outFile.write('\n')
        outFile.flush()
    outFile.close()

def loadSimilarityTable(path):
    f=codecs.open(path, 'r', encoding="utf-8")
    for line in f:
        letters=line.strip('\n').strip().split(" ")
        similarityDic[letters[0]]=letters[1:]

def isSimilar(c1,c2):
    charlist=similarityDic.get(c1)
    if charlist==None:
        return False
    charlist=list(charlist)
    if c2 in charlist:
        return True
    else:return False

if __name__ == '__main__':
    dataPath="/home/razzaz/PycharmProjects/ArabicSpellchecker/diffrence"
    a =datetime.now()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    loadSimilarityTable(dir_path + os.sep + 'SmilarityTable')
    uniqWordsset, uniqWordsMap=ReadData.readData(dataPath)
    c=cluster(uniqWordsset)
    writeClustredDic(c,dataPath+'.dic')
    b =datetime.now()
    diffrence = b - a
    print diffrence
    exit()

    a =datetime.now()

    numthreads = 8
    numOfWords = 100

    # create the process pool
    pool = multiprocessing.Pool(processes=numthreads)

    result_list = pool.map(WordsNighbors, (uniqWordsset[wordIndex:wordIndex + numOfWords] for wordIndex in xrange(0, len(uniqWordsset))), numOfWords)
    pool.close()
    pool.join()
    result = {}
    print ('mapping was finished')
    map(result.update, result_list)
    print ('Finished')
    print (len(result))
    outPath=dataPath+".ClustredDic"
    writeClustredDic(result,outPath)
    b =datetime.now()
    diffrence = b - a
    print diffrence