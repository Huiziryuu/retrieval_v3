import multiprocessing

__author__ = 'liuhui'

'''
The coding is not totally original work.

Part of the data structure, algorithm is referred from the online tutorial
 <Problem Solving with Algorithms and Data Structures>
 http://interactivepython.org/runestone/static/pythonds/index.html

 Very good material, highly recommend it.
'''

import os
import sys
from multiprocessing import Process, Manager

import timeit

class RetrievalHash:

    # to compose a dictionary from word list
    def __init__(self):
        # to store the search result
        self.lexical_dic = {}

    def isEmptyDic(self):
        if self.lexical_dic:
            return False
        else:
            return True

    ''' read frequency list into memory
    '''
    def composeDic(self, filePath):
        # check file existence - exist
        if os.path.exists(filePath):

            f = open(filePath,'r', encoding="latin1")
            for i in f:
                word, freq = i.split()
                self.lexical_dic[word] = (word, freq)
            f.close()
        # check file existence - doesn't exist
        else:
            print('File', filePath, 'does not exist!')
            sys.exit(1)

    def searchDic(self, items):
        # print('step0')
        managerlist = Manager()
        # print('step1')
        list_existed = managerlist.list()
        list_notExisted = managerlist.list()
        # print('step2')
        procs = []

        for i in range(len(items)):
            p = multiprocessing.Process(target=self.searchDicInner,args=(items[i],list_existed,list_notExisted))
            procs.append(p)
            p.start()

        # wait for all work process to finish
        for p in procs:
            p.join()

        self.__quickSort(list_existed)

        # print(list_existed)
        # print(list_notExisted)
        rtn = {}
        rtn['existed'] = list_existed[0:]
        rtn['notExisted'] = list_notExisted[0:]
        return rtn

    ''' search items from the dictionary
    '''
    def searchDicInner(self, item, list_existed, list_notExisted):
        # rtn = {}
        # list_existed = []
        # list_notExisted = []
        # for item in items:
        try:
            lexi = self.lexical_dic[item]
            list_existed.append((lexi[0], int(lexi[1])))
        except KeyError:
            list_notExisted.append(item)

        # self.__quickSort(list_existed)
        #
        # rtn['existed'] = list_existed
        # rtn['notExisted'] = list_notExisted
        # return rtn

    ''' sort search result according to the word frquency
    '''
    def __quickSort(self, alist):
        self.__quickSortHelper(alist,0,len(alist)-1)

    ''' sort helper functoin, mainly for recursive call
    '''
    def __quickSortHelper(self, alist, first, last):
        if first < last:
            splitpoint = self.__partition(alist, first, last)

            self.__quickSortHelper(alist,first,splitpoint-1)
            self.__quickSortHelper(alist,splitpoint+1,last)

    ''' to find the partition point for each sort loop
    '''
    def __partition(self, alist, first, last):

        # get a median value as pivo point
        medianP = (first + last) // 2
        pivopoint = sorted([(first, alist[first][1]), (medianP, alist[medianP][1]), (last, alist[last][1])],\
                           key=lambda x:x[1])[1][0]
        alist[first], alist[pivopoint] = alist[pivopoint], alist[first]
        pivovalue = alist[first][1]

        leftmark = first
        rightmark = last

        done = False
        while not done:

            while leftmark <= rightmark and alist[leftmark][1] >= pivovalue:
                leftmark = leftmark + 1

            while rightmark >= leftmark and alist[rightmark][1] <= pivovalue:
                rightmark = rightmark - 1

            if rightmark < leftmark:
                done = True
            else:
                alist[leftmark], alist[rightmark] = alist[rightmark], alist[leftmark]

        # exchange
        alist[first],alist[rightmark] = alist[rightmark],alist[first]

        return rightmark

# class MyManager(BaseManager): pass
#
# def Manager():
#     m = MyManager()
#     m.start()
#     return m
#
# MyManager.register('RetrievalHash', RetrievalHash)

# ''' main control function
# '''
# def main():
#
#     # get necessary information through the prompt
#     prompt = "==> "
#     exitPrompt = ""
#
#     # get frequency lexicon file
#     while True:
#         print(">> Please indict the freqence file. eg. /tmp/freq_lexi_dic_file {} <<".format(exitPrompt))
#         filePath = input(prompt)
#         if filePath.upper() == 'NO':
#             exit(0)
#         elif os.path.exists(filePath):
#             break
#         else:
#             print(">> File doesn't exist, please verify <<")
#             exitPrompt = "Or input 'No' to terminate this programme"
#
#     # struct hash map
#     dic = leXicalDic()
#     composeDic(dic, filePath)
#
#     # retrieve
#     while True:
#         print(">> Please input the search key words separated in space. eg. exical_item1 lexical_item2 ... <<")
#         wordsList = input(prompt)
#         wordsList = wordsList.split()
#         start = timeit.default_timer()
#         print(wordsList)
#         searchDic(dic, wordsList)
#         stop = timeit.default_timer()
#         print("retrieval result - available words:", dic.list_existed)
#         print("retrieval result - words not in the lexicon:", dic.list_notExisted)
#         print('retrieval execution time is:',str((stop - start)*1000), 'milliseconds')
#
#         # next retrieve request
#         print(">> Do you want to continue retrieving? Yes or No <<")
#         rep = input(prompt)
#         if rep.upper() == "NO":
#             exit(0)
#
# if __name__ == '__main__':
#     main()


#####################################################
#
# for testing only
# hash map constructing time is 10 seconds around
# retrieve time is 0.06 milliseconds around
#
#####################################################

# def main():
#
#     # construct data
#     composeDic(dic, '/Users/liuhui/Documents/MasterStudy/2015/Programming_Project/source/ari/freq_eng')
#
#     # retrieve
#     start = timeit.default_timer()
#     searchDic(dic, ['algorithmiquement','aagoel', 'homathorizon', 'huiliu',\
#                     'enghls', 'french', 'ok', 'whaoo', 'what', 'finland', 'python'])
#     stop = timeit.default_timer()
#     print(dic.list_existed)
#     print(dic.list_notExisted)
#     print('search execution time is:',str((stop - start)*1000), 'milliseconds')
#
# if __name__ == '__main__':
#     dic = leXicalDic()
#     main()