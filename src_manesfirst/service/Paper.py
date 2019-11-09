import os

import bibtexparser
import textract
import re

from main.src.repository import PeeweeRepository
from django.db import models


# def extractWords():
#     filename = 'asd' + '.pdf'
#     text = textract.process(filename)
#     decodedContent = (text.decode())
#     content = decodedContent.replace('\n', " ")
#     content = content.split(' ')
#     print(content)


class Paper:

    def __init__(self,metaData=None,byteContent=None,wordContent=None,id=None):
        self.metaData = metaData
        self.byteContent = byteContent
        self.wordContent = wordContent
        self.id = PeeweeRepository.getNextPaperId()





    def upload(self,pdfFile):
        if(self.metaData == None):
            print("Please set a meta data for this paper.")
            return
        else:
            self.setContent(pdfFile)
            PeeweeRepository.uploadPaper(self.metaData, self.id, self.reducedWordContent, self.byteContent)

    def getId(self):
        return self.id

    def setId(self,id):
        self.id = id

    def getMeta(self):
        return self.metaData

    def setMeta(self,metaData):
        self.metaData = metaData


    def setMetaByBibtex(self,metaData):
        self.metaData = bibtexparser.loads(metaData).entries[0]


    def getContent(self):
        return ' '.join(self.wordContent)

    def setContent(self,pdfFileByteContent):
        textractPdfFile = open("textractTempPDF.pdf","wb")
        textractPdfFile.write(pdfFileByteContent)
        textractPdfFile.close()

        self.wordContent = textract.process("textractTempPDF.pdf",encoding="utf-8")\
            .decode("utf-8")\
            .replace("\n","")\
            .split(" ")
        alhenumericalTestRE = re.compile(r'^\w+$')
        self.reducedWordContent =list(filter(alhenumericalTestRE.search,self.wordContent))
        self.reducedWordContent = list(map(lambda x:x.lower(),self.reducedWordContent))
        self.reducedWordContent = list(set(self.reducedWordContent))
        # self.wordContent.replace("the","")
        # self.wordContent.replace("a","")
        # self.wordContent.replace("an","")
        os.remove("textractTempPDF.pdf")
        self.byteContent = pdfFileByteContent





