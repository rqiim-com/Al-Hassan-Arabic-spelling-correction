# -*- coding: utf-8 -*-
import kenlm
import codecs
import os
import time
import multiprocessing
from multiprocessing import Manager
from functools import partial
clustresDic={}
similarityDic={}
def SentenceWordsInDictionart(UniqWordsSet,sentence):
    sentence=str(sentence)
    UniqWordsSet=set(UniqWordsSet)
    result={}
    for word in sentence:
        if word in UniqWordsSet:
            result[word]=True
        else:
            result[word]=False
    return result

def loadUniqWords(path):
    uniqWordsSet=set()
    uniqWordsfile=codecs.open(path, 'r', 'utf-8')
    for line in uniqWordsfile:
        line=line.strip('\n').strip()
        uniqWordsSet.add(line)
    uniqWordsfile.close()
    return uniqWordsSet

def isSimilar(c1,c2):
    charlist=similarityDic.get(c1)
    if charlist==None:
        return False
    charlist=list(charlist)
    if c2 in charlist:
        return True
    else:return False

def loadClusterDic(path):
    clusters={}
    clsuterDicFile=codecs.open(path,'r','utf-8')
    for line in clsuterDicFile:
        line=line.strip('\n').strip()
        words=line.split(" ")
        clusters[(words[0])] = words[1:]
    return clusters

def damerau_leven_dist_Similarity(s1, s2):

    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)

    if abs(lenstr1-lenstr2)>=3:
        return float("inf")
    for i in xrange(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in xrange(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
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
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + 1)  # transposition
    return d[lenstr1 - 1, lenstr2 - 1]



def levenshtein(word1, word2):
    columns = len(word1) + 1
    rows = len(word2) + 1
    if abs(columns-rows)>=3:
        return float("inf")
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
                cost=1
                # if(isSimilar(word1[column - 1] , word2[row - 1])):
                #     cost=1
                replaceCost = previousRow[column - 1] + cost
            else:
                replaceCost = previousRow[column - 1]
            currentRow.append(min(insertCost, deleteCost, replaceCost))

    return currentRow[-1]

def levenshteinWithSimilarity(word1, word2):
    columns = len(word1) + 1
    rows = len(word2) + 1
    if abs(columns-rows)>=3:
        return float("inf")
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
                if(isSimilar(word1[column - 1] , word2[row - 1])):
                    cost=1
                replaceCost = previousRow[column - 1] + cost
            else:
                replaceCost = previousRow[column - 1]
            currentRow.append(min(insertCost, deleteCost, replaceCost))

    return currentRow[-1]

def candidate_retrival(word,ClusterDic):

    temp=[]
    candidtes=[]
    # ClusterDic=dict(ClusterDic)
    t=len(ClusterDic)
    minimum=3
    for center in ClusterDic.keys():
        dist=levenshtein(word, center)
        if(dist==minimum or dist==minimum+1):
            temp.append(center)
            temp+=ClusterDic[center]

        elif(dist<minimum):
            temp=[]
            temp.append(center)
            temp=temp+ClusterDic[center]
            minimum = dist

    for item in temp:
        dist=levenshteinWithSimilarity(word,item)
        if (dist==minimum or dist==minimum+1):
            candidtes.append(item)
        elif (dist<minimum):
            candidtes=[]
            candidtes.append(item)

    return candidtes
def candidate_retrivalMultiProcessing(word,ClusterDicKeys,result):
    temp=[]
    # ClusterDic=dict(ClusterDic)
    global clustresDic
    minimum=4
    for center in ClusterDicKeys:
        dist=levenshtein(word, center)
        if(dist==minimum or dist==minimum+1):
            temp.append(center)
            temp+=clustresDic[center]
        elif(dist<minimum):
            if dist<minimum-1:
                temp=[]
                temp.append(center)
                temp=temp+clustresDic[center]
            else:
                temp.append(center)
                temp += clustresDic[center]
            minimum = dist
    candidtes={}
    for item in temp:
        dist=levenshteinWithSimilarity(word,item)
        if (dist == minimum  ):
            candidtes[item]=dist
        elif (dist < minimum):
            candidtes = {}
            candidtes[item]=dist
            minimum=dist

    result.update(candidtes)
    # print len(candidtes)
def multi(word):
    manager = Manager()
    result = manager.dict()
    jobs=[]
    global clustresDic
    subDicLength=int(len(clustresDic.keys())/4)
    for i in range(0,len(clustresDic),subDicLength):
        p = multiprocessing.Process(target=candidate_retrivalMultiProcessing, args=(word,clustresDic.keys()[i:i+subDicLength],result))
        p.start()
        jobs.append(p)
    for job in jobs:
        job.join()
    candidates=[]
    minimum = 4
    for key in result.keys():
        if result[key]==minimum :
            candidates.append(key)
        elif result[key] < minimum:
            minimum=result[key]
            candidates=[]
            candidates.append(key)
    return candidates

def spellCheck(sentence,uniqWords,langModel,n):

    splited=sentence.split()
    res={}
    for word in splited:
        word=word.strip()
        res[word] = None
        if not word in uniqWords:
            # candidates=candidate_retrival(word,clustresDic)
            candidates=multi(word)
            if len(candidates)<1:
                res[word]="no match"
                continue
            candidatesScores = {}
            for candidate in candidates:
                new=sentence.replace(word,candidate)
                s=langModel.score(new)
                if s in candidatesScores.keys():
                    ls=candidatesScores[s]
                    ls.append(candidate)
                    candidatesScores[s]=ls
                else:
                    listofCand=[]
                    listofCand.append(candidate)
                    candidatesScores[s]=listofCand
            scoresSorted=candidatesScores.keys()
            scoresSorted=sorted(scoresSorted,reverse=True)

            sentence=sentence.replace(word,candidatesScores[scoresSorted[0]][0])
            numofsuges=min(n,len(scoresSorted))

            for i in range(numofsuges):
                nScore=scoresSorted[i]
                nCandidates=candidatesScores[nScore]
                if(word in res.keys()):
                    if not res[word]==None:
                        ls=res[word]
                        ls=ls+nCandidates
                        res[word]=ls
                    else:
                        ls=[]
                        ls=ls+nCandidates
                        res[word] = ls

    return res
def preprocessing(words):
    words=words.replace(u"\uFE93",u"\u0629").replace(u"\uFE94",u"\u0629")
    words=words.replace(u"\uFEE9",u"\u0647").replace(u"\uFEEA",u"\u0647").replace(u"FEEC",u"\u0647").replace(u"\uFEEB",u"\u0647")
    return words
def loadSimilarityTable(path):
    f=codecs.open(path, 'r', encoding="utf-8")
    for line in f:
        letters=line.strip('\n').strip().split(" ")
        similarityDic[letters[0]]=letters[1:]

def main():
    global clustresDic
    dir_path = os.path.dirname(os.path.realpath(__file__))

    loadSimilarityTable(dir_path + os.sep + 'SmilarityTable')
    print similarityDic

    uniqWordsPath = dir_path + os.sep + "Nim+feat+diacs+Qalb.uniq"
    clustersDicPath = dir_path + os.sep + "UniqWordsQalb.dic"
    clustresDic = loadClusterDic(clustersDicPath)
    uniqWords = loadUniqWords(uniqWordsPath)
    langModelPath = dir_path + os.sep + "QALB3.arpa"
    langModel = kenlm.LanguageModel(langModelPath)
    numberOfSugesstion = 10

    while True:
        sentence = u'd d d'
        print "\n"
        text = raw_input("اكتب جملة \n")

        if (text == 'exit'):
            exit()
        sentence = str(text).decode("utf-8")
        a = time.time()
        checkResut = spellCheck(sentence, uniqWords, langModel, numberOfSugesstion)
        b = time.time()
        print "time to finish is " + str(b - a)

        for r in checkResut.keys():
            print "***********"

            print r.encode('utf-8')
            if checkResut[r] == None:
                print "coreect"
                continue
            for sug in checkResut[r]:
                print sug.encode('utf-8')

