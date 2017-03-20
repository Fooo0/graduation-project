# -*- coding:utf-8 -*-
'''
Created on 2017.3.7

@author: Jiafei Song
'''

class AppInfo:
    def __init__(self):
        self.update = []     # list of Info£¬what's new
        self.review = []     # list of Info£¬user review
        
    def setName(self, name):
        self.name = name
        
    def appendUpdate(self, info):
        self.update.append(info)
        
    def appendReview(self, info):
        self.review.append(info)
        
class Info:
    def __init__(self, time, info):
        self.time = time
        self.info = info    # token list, what's new or review   