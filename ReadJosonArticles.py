import json
from pprint import pprint
import requests
import sys


reload(sys)
sys.setdefaultencoding('utf8')
path="/home/razzaz/Desktop/Data/FeaturedArticleFromRaqim/"
outfile=open(path+'articles.txt','w')
IDSfile=open(path+'IDS.txt','r')
prevIDS=IDSfile.readlines()

for i in range(0,13):
    featuredArticlesIDS=requests.get(url="https://rqiim.com/api/post/featured?sort=created&direction=desc&page="+str(i)+"&limit=20")
    # data = json.load(open('/home/razzaz/Desktop/Raqim/jasonFeaturedArticles/FeatureArticles.josn'))
    x=featuredArticlesIDS.json()
    for record in x:
        _id2= str((record['_id2']))
        if(_id2+'\n' in prevIDS):
            continue
        else:
            prevIDS.append(_id2)
        featuredArticlesData=requests.get(url="https://rqiim.com/api/post/"+_id2)

        article=featuredArticlesData.json()
        body=article["body"]
        outfile.write(body)
        outfile.write('\n')
    outfile.flush()

outfile.close()
IDSfile=open(path+'IDS.txt','w')
for id in prevIDS:
    IDSfile.write(id.strip('\n'))
    IDSfile.write('\n')
IDSfile.flush()
IDSfile.close()

# pprint(x)