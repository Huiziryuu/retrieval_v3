__author__ = 'liuhui'

import RunClientManager
import os
import timeit

def main():

    manager = RunClientManager.make_client_manger()
    dic = manager.get_lex_dic()

    # get necessary information through the prompt
    prompt = "==> "
    exitPrompt = ""

    if (dic.isEmptyDic()):
        # get frequency lexicon file
        while True:
            print(">> Please indict the freqence file. eg. /tmp/freq_lexi_dic_file {} <<".format(exitPrompt))
            filePath = input(prompt)
            if filePath.upper() == 'NO':
                exit(0)
            elif os.path.exists(filePath):
                break
            else:
                print(">> File doesn't exist, please verify <<")
                exitPrompt = "Or input 'No' to terminate this programme"

        dic.composeDic(filePath)


    # retrieve
    while True:
        print(">> Please input the search key words separated in space. eg. exical_item1 lexical_item2 ... <<")
        wordsList = input(prompt)
        wordsList = wordsList.split()
        start = timeit.default_timer()
        result = dic.searchDic(wordsList)
        stop = timeit.default_timer()
        print("retrieval result - available words:", result['existed'])
        print("retrieval result - words not in the lexicon:", result['notExisted'])
        print('retrieval execution time is:',str((stop - start)*1000), 'milliseconds')

        # next retrieve request
        print(">> Do you want to continue retrieving? Yes or No <<")
        rep = input(prompt)
        if rep.upper() == "NO":
            exit(0)

if __name__ == '__main__':
    main()