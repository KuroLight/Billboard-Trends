# Billboard-Trends

## To Run
only edit this two lines:

    START_YEAR = 2009  # inclusive

    END_YEAR = 2010  # exclusive


## N parts are planned to do:

1. A powerful Spider-man gets lyrics.json, including artists, titles, lyrics, genres, etc.
2. A smart Iron-man does the data analysis job.
3. A muscular Captain-America shows the beautiful charts.
4. Last but not the least, a magical Dr. Strange contributes the magic. 


## Videos in year 2016: 

1. https://www.youtube.com/watch?v=vdji9fLqyB8
2. https://www.youtube.com/watch?v=IabHTp06BLs
3. https://www.youtube.com/watch?v=t5-a5WqbFnE


## Tutorials:
1. https://www.kaggle.com/rahulvks/nlp-billboard-nb-1
2. https://www.datacamp.com/community/tutorials/R-nlp-machine-learning
3. https://www.kaggle.com/devisangeetha/sing-a-song-lyrics-is-here/notebook
4. https://github.com/rasbt/musicmood
5. http://brandonrose.org/clustering#K-means-clustering 
6. https://pudding.cool/2017/05/song-repetition/
7. https://www.kaggle.com/rcushen/a-basic-implementation-of-sentiment-analysis


## Team work:
0. data collection
    1. shiyao: 00-09, 90-00
    2. boyu:   80-90, 70-80
    3. yongfa: 60-70, 50-60

1. shiyao:
1) data preprocessing

artist, clean lyrics, drop stopwords, stemming, pos_tag

2) vocabulary 改变
    1. graph 1: vocabulary, adj, noun count 变化
    2. graph 2: artists: vocabulary, adj, noun count 变化
    3. graph 3: vocabulary -> wordcloud
    4. graph 4: top 10, top 50, top 100  vocabulary 占比分析，歌词长度 distribution 的长度分析
    5. graph 5: 不同年代的：歌词数量，高频word, 高 tf-idf 统计对比
    6. graph 7: case study: prince or micheal jackson
3) TBD 
2. boyu: sentiment analysis
NRC Lexicon: 参考 https://www.kaggle.com/devisangeetha/sing-a-song-lyrics-is-here/notebook

3. yongfa: 
    pipeline:
    1. load jsons
    2. remove stopwords, stem, and tokenize
    3. tf-idf and calculate cosine similarity
    4. k-means clustering
    5. 

    clustering, Kmeans:
    1) artist
    2) song
    3) through year

## token
create environmrnt variable 'GENIUS_TOKEN':

    please ask yongfatS
