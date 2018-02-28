# -*- coding: utf-8 -*-

import codecs
import re
import string
import sys

# dataFile=open('/home/razzaz/Desktop/AlgorythmaWork/Data/diacritization/test/aljazeera.txt.clean.Train.arabic.tashkeelRemoved','r')
reload(sys)
sys.setdefaultencoding('utf8')

table = string.maketrans("", "")


def test_trans(s):
    return s.translate(table, string.punctuation)

def Multisplit(txt, seps):
    default_sep = seps[0]

    # we skip seps[0] because that's the default seperator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]

def readData(path):
    dataFile=open(path,'r')
    uniqWordsMap={}
    uniqWordsset=set()
    for line in dataFile:
        splited=line.strip('\n').strip().split(" ")
        for word in splited:
            if word in uniqWordsMap:
                x=uniqWordsMap.get(word)
                x+=1
                uniqWordsMap[word]=x
            else:
                uniqWordsMap[word]=1
    for key in uniqWordsMap.keys():
        # if uniqWordsMap.get(key)>=0:
            uniqWordsset.add(key)
    print len(uniqWordsset)
    uniqWordsset=list(uniqWordsset)
    return uniqWordsset,uniqWordsMap
    # clustredDic=ClusteringTheDictionary.cluster(uniqWordsset)
    # outPath=dataPath+".ClustredIdc"
    # ClusteringTheDictionary.writeClustredDic(clustredDic,outPath)
    ClusterUtls=ClusteringTheDictionary.ClusteringUtlts(uniqWordsset)

def cleanFile(filePath):
    allData = open(filePath, 'r')
    outFile = codecs.open(filePath + '.clean', 'w', 'utf-8')
    count = 0
    allLines = allData.readlines()

    cleanLines = []
    for orginalLine in allLines:
        orginalLine=orginalLine.strip().strip(".")
        # remove english punctuations
        orginalLine = test_trans(orginalLine).strip()
        lines = Multisplit(orginalLine, list(string.punctuation))
        for line in lines:
            # remove arabic puctuations
            line = line.replace('’', '').replace("\”", '')
            line = re.sub(ur'[\u0600-\u0620]', ' ', line).strip()
            # remove Arabic strange letters
            line = re.sub(ur'[\u0656-\u06FF]', ' ', line).strip()
            # remove english letters and numbers
            line = re.sub(ur'[\u0020-\u007F]', ' ', line)
            line = re.sub(r'\s+', ' ', line).strip()

            print (line)
            print ('\n')
            if (line.strip('\n').strip() != ""):
                cleanLines.append(line)
        count = 0
    for cline in cleanLines:
        count += 1
        cline = cline.encode('utf-8')
        outFile.write(cline + '\n')
        outFile.flush()

    outFile.close()
# readData("/home/razzaz/Desktop/Data/NMWRC7AR/DATA/all.clean.Arabic.clean")
# cleanFile("/home/razzaz/Desktop/Data/NMWRC7AR/DATA/all.clean.Arabic")

            #
    # X = np.arange(len(uniqWordsset)).reshape(-1, 1)
    # # cls=DBSCAN( metric=lev_metric, eps=5, min_samples=2).fit_predict(X)
    # # cls=k_means(X,metric=lev_metric)
    # # db = DBSCAN(metric=lev_metric).fit(X)
    # # core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    # # core_samples_mask[db.core_sample_indices_] = True
    # # labels = db.labels_
    #
    # # Number of clusters in labels, ignoring noise if present.
    #
    #
    # words = uniqWordsset
    # words = np.asarray(words) #So that indexing with a list will work
    # lev_similarity = -1*np.array([[damerau_levenshtein_distance(w1,w2) for w1 in words] for w2 in words])
    # affprop = AffinityPropagation(affinity="precomputed", damping=0.5)
    # affprop.fit(lev_similarity)
    # centroids=affprop.cluster_centers_indices_
    # resultFile=open(dataPath+'.Clustringresult','w')
    #
    # for cluster_id in np.unique(affprop.labels_):
    #     exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
    #     cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
    #     cluster_str = ", ".join(cluster)
    #     print(" - *%s:* %s" % (exemplar, cluster_str))
    #     resultFile.write(" - *"+exemplar+":*"+cluster_str)
    #     resultFile.write('\n')
    #
    # resultFile.flush()
    # index=0
    # for word in uniqWordsset:
    #     resultFile.write(word+' '+str(affprop.labels_[index]) )
    #     resultFile.write('\n')
    #     index+=1
    #
    # resultFile.flush()
    # resultFile.close()
    # dataFile.close()
    #
    # centriodsFile=open(dataPath+'.centers','w')
    # for center in centroids:
    #     centriodsFile.write(uniqWordsset[center])
    #     centriodsFile.write('\n')
    # centriodsFile.flush()
    # centriodsFile.close()
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# print("Adjusted Rand Index: %0.3f"
#       % metrics.adjusted_rand_score(labels_true, labels))
# print("Adjusted Mutual Information: %0.3f"
#       % metrics.adjusted_mutual_info_score(labels_true, labels))
# print("Silhouette Coefficient: %0.3f"
#       % metrics.silhouette_score(X, labels))

