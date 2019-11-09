import peewee

from main.src.model.Tables import Paper,paperIdGenerator,Word,createTables,InverseIndex
from main.src.service import Paper as paper


def getNextPaperId():
    id = paperIdGenerator.get(paperIdGenerator.id == 1)
    nextId = id.currentId
    id.currentId += 1
    id.save()

    return nextId


def uploadPaper(metaData,id,wordContent,byteContent):
    try:
        existingPaper = getPaperByTitle(metaData["title"])
        print("Paper already exists!")
        return
    except peewee.DoesNotExist:
        newPaper = Paper()
        newPaper.title = metaData["title"]
        newPaper.metaData = str(metaData)
        newPaper.author = metaData["author"]
        newPaper.content = byteContent
        newPaper.id = id

        newPaper.save(force_insert=True)

        for words in wordContent:
            if(not Word.select().where(Word.word == words).exists()):
                currentWord = Word()
                currentWord.word = words
                currentWord.save()
            else:
                currentWord = Word.get(Word.word == words)

            if(not InverseIndex.select().where(InverseIndex.word_id == currentWord.id,
                                                      InverseIndex.paper_id == newPaper.id).exists()):
                newInverseIndex = InverseIndex()
                newInverseIndex.word = currentWord
                newInverseIndex.paper = newPaper
                newInverseIndex.save()




def getPaperByAuthor(author):
    databasePaper = Paper.get(Paper.author == author)

    return _databasePaperToActualPaper(databasePaper)

def getPaperByTitle(title):
    databasePaper = Paper.get(Paper.title == title)

    return _databasePaperToActualPaper(databasePaper)


def getPaperById(id):
    databasePaper = Paper.get(Paper.id == id)

    return _databasePaperToActualPaper(databasePaper)


def getPapersByMultipleWords(wordList):
    initialSet = set(getPapersBySingleWord(wordList[0]))
    for word in wordList[1:]:
        initialSet = initialSet.intersection(getPapersBySingleWord(word))
    return list(initialSet)


def getPapersBySingleWord(word):
    papers = (Paper.select()
              .join(InverseIndex)
              .join(Word)
              .where(word == Word.word))
    returnList = []
    for paper in papers:
        returnList.append(paper)

    return returnList
def deletePaperById(id):
    toBeDeletedPaper = Paper.get(Paper.id == id)

    toBeDeletedPaper.delete_instance()


def _databasePaperToActualPaper(databasePaper):
    actualPaper = paper.Paper()

    actualPaper.setMeta(eval(databasePaper.metaData))
    actualPaper.setId(databasePaper.id)
    actualPaper.setContent(databasePaper.content)

    return actualPaper

