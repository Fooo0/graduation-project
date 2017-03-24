# encoding: utf-8
'''
Created on 2017.03.23

@author: Jiafei Song
'''

import os
import nltk

def traverseFolder(dirWh):
    for root, _,files in os.walk(dirWh):
        for fileName in files:    # all file of preprocessed what's new data
            findPrepData(root, fileName)
        
def extractFeature(flag, text, fileName):
    global rootRevEx
    global rootWhEx
    if flag == 0:
        aFile = open(os.path.join(rootWhEx, fileName), 'a')
    if flag == 1:
        aFile = open(os.path.join(rootRevEx, fileName), 'a')
    tokens = nltk.word_tokenize(text)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    featrCandi = nltk.collocations.BigramCollocationFinder.from_words(tokens)
    '''
    test and decide: 1)n-gram:n? 2).from_words(tokens, yy):yy? 3)featrCandi.nbest(bigram_measures.pmi, xx):xx?
    '''
    for fc in featrCandi.score_ngrams(bigram_measures.pmi):    # measure features using pointwise mutual information
        aFile.write("%s : %s\n" % (fc[0],fc[1]))
    aFile.close()
    return

def findPrepData(rootWh, fileName):
    global rootRev
    global rootRevEx
    global rootWhEx
    fileWh = open(os.path.join(rootWh, fileName), 'r')    # what's new file of an App
    fileRev = open(os.path.join(rootRev, fileName), 'r')    # review file of the same App as above
    linesWh = fileWh.readlines()    # content
    linesRev = fileRev.readlines()    # content
    lineNumWh = len(linesWh)    # length
    lineNumRev = len(linesRev)    # length
    daysLineWh = 0
    dLineRBegn = 0    # first day line, i.e.time of first review between two updates
    dLineREnd = 0    # final day line, i.e.time of final review between two updates
    txtLineWh = 1
    while txtLineWh < lineNumWh:
        counter = 0    # count number of reviews between updates
        daysWh = int(linesWh[daysLineWh].strip('\n'))    # remove \n
        daysREV = int(linesRev[dLineREnd].strip('\n'))    # remove \n
        dLineRBegn = dLineREnd    # next begin line is last final line, save time, don't have to go from 0 again
        while(daysREV < daysWh and dLineREnd < lineNumRev):    # Reviews before update
            daysREV = int(linesRev[dLineREnd].strip('\n'))
            counter += 1    # count
            dLineREnd += 2    # next line for days
        reviewLst = [linesRev[i] for i in range(dLineRBegn + 1, dLineREnd, 2)]    # list for all reviews
        reviewStr = ' '.join(reviewLst)    # join all the reviews into a string
        extractFeature(1, reviewStr, fileName)
        extractFeature(0, linesWh[txtLineWh], fileName)
        daysLineWh += 2    # a new update day
        txtLineWh += 2    # a new uppdate description at the day above
    return

global rootRev
global rootRevEx
global rootWhEx
rootRev = 'D:\Users\Mo\workspace\AppEvolution\main\Review\Review'
rootRevEx = 'D:\Users\Mo\workspace\AppEvolution\main\Extract\Review'
rootWhEx = 'D:\Users\Mo\workspace\AppEvolution\main\Extract\WhatsNew'
traverseFolder('D:\Users\Mo\workspace\AppEvolution\main\WhatsNew')
        
        
        