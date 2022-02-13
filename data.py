import jieba as jb


class Data:
    __data=[]
    __dataName=""
    __dataPath=""
    __dataTokenize=[]
    __counts={}

    def __init__(self,data,dataName,dataPath):
        self.__data=data
        self.__dataName=dataName
        self.__dataPath=dataPath

    def __tokenize(self):
        print("Tokenize in ......\n")
        words=[]
        for sentence in self.__data:
            words+=jb.lcut(sentence,cut_all=False)
        self.__dataTokenize=words
        print("Tokenize is finished.\n",self.__dataTokenize)
    
    def __statics(self):
        print("Statistic in ......\n")
        for word in self.__dataTokenize:
            if len(word)<=1 or word.isnumeric():
                print(word)
            else:
                if word in self.__counts.keys():
                    self.__counts[word]=self.__counts[word]+1
                else :
                    self.__counts[word]=1
        print("Staticing words is finished.\n")

    def processing(self):
        self.__tokenize()
        self.__statics()

    def getStatics(self):
        return self.__counts

    def getDataPath(self):
        return self.__dataPath

    def getData(self):
        return self.__data

    def getDataName(self):
        return self.__dataName

    def getTokenizeString(self):
        str=""
        for word  in self.__dataTokenize:
            str+=word+" "
        return str