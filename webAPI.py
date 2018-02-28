# -*- coding: utf-8 -*-
import flask
from flask import Flask
from flask import abort
import kenlm
import codecs
import os
import time
from flask import request
import json
import  main

# similarityDic={}
#
#
# def SentenceWordsInDictionart(UniqWordsSet,sentence):
#     sentence=str(sentence)
#     UniqWordsSet=set(UniqWordsSet)
#     result={}
#     for word in sentence:
#         if word in UniqWordsSet:
#             result[word]=True
#         else:
#             result[word]=False
#     return result
#
# def loadUniqWords(path):
#     uniqWordsSet=set()
#     uniqWordsfile=codecs.open(path, 'r', 'utf-8`')
#     for line in uniqWordsfile:
#         line=line.strip('\n').strip()
#         uniqWordsSet.add(line)
#     uniqWordsfile.close()
#     return uniqWordsSet
#
# def isSimilar(c1,c2):
#     charlist=similarityDic.get(c1)
#     if charlist==None:
#         return False
#     charlist=list(charlist)
#     if c2 in charlist:
#         return True
#     else:return False
#
# def loadClusterDic(path):
#     clusters={}
#     clsuterDicFile=codecs.open(path,'r','utf-8')
#     for line in clsuterDicFile:
#         line=line.strip('\n').strip()
#         words=line.split(" ")
#         clusters[(words[0])] = words[1:]
#     return clusters
#
# def damerau_leven_dist_Similarit(s1, s2):
#
#     d = {}
#     lenstr1 = len(s1)
#     lenstr2 = len(s2)
#     for i in xrange(-1, lenstr1 + 1):
#         d[(i, -1)] = i + 1
#     for j in xrange(-1, lenstr2 + 1):
#         d[(-1, j)] = j + 1
#
#     for i in xrange(lenstr1):
#         for j in xrange(lenstr2):
#             if s1[i] == s2[j]:
#                 cost = 0
#             elif isSimilar(s1[i],s2[j]):
#                 cost=1
#             else:
#                 cost = 2
#             d[(i, j)] = min(
#                 d[(i - 1, j)] + 1,  # deletion
#                 d[(i, j - 1)] + 1,  # insertion
#                 d[(i - 1, j - 1)] + cost,  # substitution
#             )
#             if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
#                 d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition
#
#     return d[lenstr1 - 1, lenstr2 - 1]
# def levenshtein(word1, word2):
#
#     columns = len(word1) + 1
#     rows = len(word2) + 1
#     if abs(columns-rows)>=4:
#         return float("inf")
#     # build first row
#     currentRow = [0]
#     for column in xrange(1, columns):
#         currentRow.append(currentRow[column - 1] + 1)
#
#     for row in xrange(1, rows):
#         previousRow = currentRow
#         currentRow = [previousRow[0] + 1]
#
#         for column in xrange(1, columns):
#
#             insertCost = currentRow[column - 1] + 1
#             deleteCost = previousRow[column] + 1
#
#             if word1[column - 1] != word2[row - 1]:
#                 cost=1
#                 if(isSimilar(word1[column - 1] , word2[row - 1])):
#                     cost=0.5
#                 replaceCost = previousRow[column - 1] + cost
#             else:
#                 replaceCost = previousRow[column - 1]
#
#             currentRow.append(min(insertCost, deleteCost, replaceCost))
#
#     return currentRow[-1]
#
# def candidate_retrival(word,ClusterDic):
#
#     temp=[]
#     candidtes=[]
#     # ClusterDic=dict(ClusterDic)
#     t=len(ClusterDic)
#     minimum=3
#     for center in ClusterDic.keys():
#         if center==u"محمد":
#             print "stop"
#         dist=levenshtein(word, center)
#         if(dist==minimum or dist==minimum+1):
#             temp.append(center)
#             temp+=ClusterDic[center]
#
#         elif(dist<minimum):
#             temp.append(center)
#             temp=temp+ClusterDic[center]
#             minimum = dist
#
#     for item in temp:
#
#         dist=levenshtein(item,word)
#         if (dist<minimum):
#             # candidtes=[]
#             candidtes.append(item)
#         elif (dist==minimum):
#             candidtes.append(item)
#     return candidtes
#
# def spellCheck(sentence,clustresDic,uniqWords,langModel,n):
#
#     splited=sentence.split(" ")
#     res={}
#     for word in splited:
#         res[word] = None
#         if not word in uniqWords:
#             candidates=candidate_retrival(word,clustresDic)
#             if len(candidates)<1:
#                 res[word]="no match"
#                 continue
#             candidatesScores = {}
#             for candidate in candidates:
#                 new=sentence.replace(word,candidate)
#                 s=langModel.score(new)
#                 if s in candidatesScores.keys():
#                     candidatesScores[s]=(candidatesScores[s]).append(candidate)
#                 else:
#                     listofCand=[]
#                     listofCand.append(candidate)
#                     candidatesScores[s]=listofCand
#             scoresSorted=candidatesScores.keys()
#             scoresSorted=sorted(scoresSorted,reverse=True)
#
#             sentence=sentence.replace(word,candidatesScores[scoresSorted[0]][0])
#             numofsuges=min(n,len(scoresSorted))
#
#             for i in range(numofsuges):
#                 nScore=scoresSorted[i]
#                 nCandidates=candidatesScores[nScore]
#                 if(word in res.keys()):
#                     if not res[word]==None:
#                         ls=res[word]
#                         ls=ls+nCandidates
#                         res[word]=ls
#                     else:
#                         ls=[]
#                         ls=ls+nCandidates
#                         res[word] = ls

    # return res
# def preprocessing(sen):
#     exit()
# def loadSimilarityTable(path):
#     f=codecs.open(path, 'r', encoding="utf-8")
#     for line in f:
#         letters=line.strip('\n').strip().split(" ")
#         similarityDic[letters[0]]=letters[1:]

app = Flask(__name__)

@app.route('/spells/<string:sentence>', methods=['GET'])
def spellCheckGet(sentence):
    a = time.time()
    checkResut = main.spellCheck(sentence, uniqWords, langModel, numberOfSugesstion)
    b = time.time()
    print "time to finish is " + str(b - a)
    result=json.dumps(checkResut)
    return result
@app.route('/spell/',  methods=['POST'])
def spellCheckPost():
    sentence=flask.request.json["sentence"]
    a = time.time()
    checkResut = main.spellCheck(sentence, uniqWords, langModel, numberOfSugesstion)
    b = time.time()
    print "time to finish is " + str(b - a)
    result=json.dumps(checkResut)
    return result



if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    main.loadSimilarityTable(dir_path + os.sep + 'SmilarityTable')
    print main.similarityDic
    uniqWordsPath = dir_path + os.sep + "Nim+feat+diacs+Qalb.uniq"
    clustersDicPath = dir_path + os.sep + "UniqWordsQalb.dic"

    main.clustresDic=main.loadClusterDic(clustersDicPath)
    uniqWords = main.loadUniqWords(uniqWordsPath)
    langModelPath = dir_path + os.sep + "languageModel3.arpa"
    langModel = kenlm.LanguageModel(langModelPath)
    numberOfSugesstion = 5
    app.run(host= '0.0.0.0',debug=True)