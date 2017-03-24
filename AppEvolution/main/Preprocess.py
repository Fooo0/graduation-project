# encoding: utf-8
'''
Data preprocess focused on NLP

@author:     Jiafei Song
'''

import os
import nltk
import re
import datetime

def getRevFiles(dirPath):    # get all files contain review data
    for root, _,files in os.walk(dirPath):
        for fileName in files:
            prepReview(root, fileName)
    return

def NLPProcess(text):    # NLP preprocessing
    global englishStopWords
    global wn
    sentences = nltk.sent_tokenize(    # benefit sentence tokenizing
                    text.lower())    # lowercase
    wholeText = []
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        wordTags = nltk.pos_tag(words)
        wordsNVAdj = [wordTag[0] for wordTag in wordTags if wordTag[1] in    # filter (adj./n./v.)words
                      ["JJ","JJR","JJS",    # adj.
                       "NN","NNS","VB",    # n.
                       "VBD","VBG","VBN","VBP","VBZ"]]    # v.
        if wordsNVAdj:
            wholeText.extend(wordsNVAdj)
    textPrep = [wn.morphy(word)    # stemming
                    for word in wholeText if not word in englishStopWords and wn.morphy(word)]    # remove stopwords
    return textPrep

def prepReview(root, fileName):    # Preprocess review data
    global dayRef
    aFile = open(os.path.join(root, fileName), 'r')
    forReview = open("D:/Users/Mo/workspace/AppEvolution/main/Review/review/" + fileName,"a")#open(os.path.join("D:\Users\Mo\workspace\AppEvolution\data\preprocessed\review", fileName), "a")
    forMark = open("D:/Users/Mo/workspace/AppEvolution/main/Review/mark/" + fileName,"a")#open(os.path.join("D:\Users\Mo\workspace\AppEvolution\data\preprocessed\mark", fileName), "a")
    lines = aFile.readlines()    # content
    lineNum = len(lines)    # length
    dateLine = 0
    reviewLine = 1
    markLine = 2
    while markLine < lineNum:
        date = datetime.datetime.strptime(lines[dateLine].replace('DATE:',''),"%B %d, %Y\n")
        days = (date - dayRef).days
        review = lines[reviewLine].replace('REVB:','')
        mark = lines[markLine].replace('MARK:','')
        forMark.write("%d %s" % (days,mark))
        if int(mark,10) < 4:
            reviewPrep = NLPProcess(review)
            if len(reviewPrep) > 1:    # no or one word(e.g. good love boring) are both non-inf
                forReview.write("%d\n%s\n" % (days," ".join(reviewPrep)))
        dateLine += 7
        reviewLine += 7
        markLine += 7
    aFile.close()
    forReview.close()
    forMark.close()
    return

def writeFile(daysLast, match, aFile):    # write preprocessed what's new data to file
    daysNow = match.group('days')    # time delta
    if daysLast != daysNow:
        if(aFile.tell() != 0):
            aFile.write('\n')
        aFile.write("%s\n" % daysNow)
        daysLast = daysNow
    textPrep = NLPProcess(match.group('text'))
    aFile.write("%s " % " ".join(textPrep))
    return daysLast
 
def prepWhatsNew(path):    # Preprocess what's new data
    # RE for id of App
    patName = re.compile(r'^[a-z]+(\.[a-z]+\d*(_[a-z]+\d*)*)*',re.I)
    # RE for normal what's new description, maybe non-inf,e.g.1 111 In this update:
    norDes = re.compile(r'^\d+\s(?P<days>\d+)\s(?P<text>[a-z]+.*)',re.I)
    # RE for special what's new description with serial number, inf,e.g.4 242 1. New App Manager
    spDesNum = re.compile(r'^\d+\s(?P<days>\d+)\s\d+[\.,)]\s*(?P<text>.*)',re.I)
    # RE for special what's new description with marks, inf,e.g.4 272 -Fixed the key sound bug
    spDesMar = re.compile(r'^\d+\s(?P<days>\d+)\s\W+\s*(?P<text>.*)',re.I)
    # RE for other normal what's new description, but inf, e.g.1 106 3D Stickers
    norDesO = re.compile(r'^\d+\s(?P<days>\d+)\s(?P<text>.+)',re.I)
    patterns = [patName, norDes, spDesNum, spDesMar, norDesO]
    
    aFile = open(path, 'r')    # read resource file
    lines = aFile.readlines()    # content
    aFilePrep = None    # file for preprocessed data
    daysLast = ' '
    for i, line in enumerate(lines):
        matches = [pattern.match(line) for pattern in patterns]    # match all the patterns
        if matches[0] != None:    # match id for App
            name = 'D:\Users\Mo\workspace\AppEvolution\main\WhatsNew\\'+matches[0].group().replace('.', '_')+'.txt'
            if aFilePrep:
                aFilePrep.close()    # close old file
            aFilePrep = open(name, "a")    # open a new file for new App
        elif matches[1] != None:    # What's new may be non-inf
            m1 = patterns[2].match(lines[i + 1])
            m2 = patterns[3].match(lines[i + 1])
            if m1 != None or m2 != None:
                m = m1 if m1 != None else m2
                if matches[1].group('days') == m.group('days'):    # must be non-inf
                    continue
                else:    # inf
                    daysLast = writeFile(daysLast, matches[1], aFilePrep)
            else:    # inf
                daysLast = writeFile(daysLast, matches[1], aFilePrep)
        elif matches[2] != None:    # inf
            daysLast = writeFile(daysLast, matches[2], aFilePrep)
        elif matches[3] != None:    # inf
            daysLast = writeFile(daysLast, matches[3], aFilePrep)
        elif matches[4] != None:    # inf
            daysLast = writeFile(daysLast, matches[4], aFilePrep)
    return

global englishStopWords
global wn
global dayRef
#-------- TO BE CONTINUE --------#
# (IF POSSIBLE)ADD OR DELETE STOPWORDS IN NLTK
#  ADD: good lova cool excite boring game please fix
englishStopWords = nltk.corpus.stopwords.words("english")
wn = nltk.corpus.wordnet
dayRef = datetime.datetime(2016,1,1)
getRevFiles("D:\Users\Mo\workspace\AppEvolution\data\googleplay_data_save")
prepWhatsNew("D:\Users\Mo\workspace\AppEvolution\data\AllWhatsNew.txt")