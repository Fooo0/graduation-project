#!/usr/bin/env python
# encoding: utf-8
'''
Data preprocess focused on NLP

@author:     Jiafei Song

@copyright:  2017 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import os
import nltk
import string
from ClassDef import Info

def getFiles(dirPath):
    for root, _,files in os.walk(dirPath):
        for fileName in files:
            NLProcess(root, fileName)
    
def NLProcess(root, fileName):
    global englishStopWords
    global lan
    aFile = open(os.path.join(root, fileName), 'r')
    '''
    forReview = open("D:/Users/Mo/workspace/AppEvolution/data/preprocessed/review/" + fileName,"a")#open(os.path.join("D:\Users\Mo\workspace\AppEvolution\data\preprocessed\review", fileName), "a")
    forMark = open("D:/Users/Mo/workspace/AppEvolution/data/preprocessed/mark/" + fileName,"a")#open(os.path.join("D:\Users\Mo\workspace\AppEvolution\data\preprocessed\mark", fileName), "a")
    '''
    lines = aFile.readlines()    # content
    lineNum = len(lines)    # length
    dateLine = 0
    reviewLine = 1
    markLine = 2
    testPrep = open(fileName,"a")
    while markLine < lineNum:
        date = lines[dateLine].replace('DATE:','')
        review = lines[reviewLine].replace('REVB:','')
        mark = lines[markLine].replace('MARK:','')
        #forMark.write("%s%s" % (date,mark))
        if int(mark,10) < 4:    
            #-------- TO BE CONTINUE --------#
            # (IF POSSIBLE)ADD OR DELETE STOPWORDS IN NLTK

            sentences = nltk.sent_tokenize(    # benefit sentence tokenizing
                            review.lower())    # lowercase    # remove punctuations
            oneReview = []
            for sentence in sentences:
                words = nltk.word_tokenize(sentence)
                wordTags = nltk.pos_tag(words)
                wordsNVAdj = [wordTag[0] for wordTag in wordTags if wordTag[1] in    # filter (adj./n./v.)words
                              ["JJ","JJR","JJS",    # adj.
                               "NN","NNS","VB",    # n.
                               "VBD","VBG","VBN","VBP","VBZ"]]    # v.
                oneReview.extend(wordsNVAdj)
            reviewPrep = [lan.stem(word)    # stemming
                            for word in oneReview if not word in englishStopWords]    # remove stopwords
            
            testPrep.write("%s%s%s\n" % (date,mark,reviewPrep))
            '''
            forReview.write("%s%s" % (date,[word for word in nltk.word_tokenize(    # tokenize
                                        review.lower().translate(None,string.punctuation))    # lowercase and remove punctuations
                                        if not word in englishStopWords]    # remove stopwords
                                      ))
            '''
        dateLine += 7
        reviewLine += 7
        markLine += 7
    aFile.close()
    '''
    forReview.close()
    forMark.close()
    '''
    testPrep.close()
    return


global englishStopWords
global lan
englishStopWords = nltk.corpus.stopwords.words("english")
lan = nltk.stem.lancaster.LancasterStemmer()
getFiles("D:\Users\Mo\workspace\AppEvolution\data\googleplay_data_save")