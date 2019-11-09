import threading

import bibtexparser
from main.src.repository import PeeweeRepository
import requests
import scholarly

import main.src.model.Tables as Tables


class Pcontroller():

    def __init__(self):
        self.watchers = []

    def getPaper(self,id):
        return PeeweeRepository.getPaperById(id)

    def searchbyTitle(self,title):
        return PeeweeRepository.getPaperByTitle(title)

    def searchbyAuthor(self,author):
        return PeeweeRepository.getPaperByAuthor(author)

    def searchbyContent(self,word):
        words = word.lower()
        words = words.split(' ')
        if(len(words) == 1):
            return PeeweeRepository.getPapersBySingleWord(word)
        else:
            return PeeweeRepository.getPapersByMultipleWords(words)

    def searchScholar(self,author='',title='',num=10):
        return self._searchScholar(author,title,num)

    def deletePaper(self,id):
        PeeweeRepository.deletePaperById(id)

    def watchPaper(self,type,str,callback):
        newWatcher = Watcher(type,str,callback)
        newWatcher.start()
        self.watchers.append(newWatcher)

    def _searchScholar(self,author, title, num):
        if((title == '' and author != '') or (title != '' and author != '')):
            resultList = []
            responseForSearchAuthor = scholarly.search_author(author)
            for response in responseForSearchAuthor:
                response.fill()
                for publication in response.publications:
                    if (title in publication.bib['title']):
                        publication.fill()
                        publicationDict = self._searchTitle(publication.bib["title"])
                        if len(resultList) < num:
                            resultList.append(publicationDict)
                        else:
                            return resultList
            return resultList
        elif(author == '' and title != ''):
            return [self._searchTitle(title)]
        else:
            return []


    def _searchTitle(self,title):
        publicationObject = next(scholarly.search_pubs_query(title))
        publicationObject.fill()
        publicationBibtex = requests.get(publicationObject.url_scholarbib,headers=scholarly._HEADERS, cookies=scholarly._COOKIES)

        publicationDict = bibtexparser.loads(publicationBibtex.text).entries[0]

        return publicationDict

class Watcher:
    def __init__(self,type,watchString,callbackFunction):
        self.type = type
        self.watchString = watchString
        self.callbackFunction = callbackFunction
        self.watcher = None


    def start(self):
        if(self.type == "NEW"):
            self.currentPaperCount = Tables.Paper.select().count()
            self.watchNew()


    def watchNew(self):
        currentPaperCount = Tables.Paper.select().count()
        if(currentPaperCount > self.currentPaperCount):
            self.currentPaperCount = currentPaperCount
            self.callbackFunction()
            return
        threading.Timer(1, self.watchNew).start()
        self.currentPaperCount = currentPaperCount


