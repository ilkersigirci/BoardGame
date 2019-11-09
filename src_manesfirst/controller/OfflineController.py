from main.src.model import Tables
from main.src.service import Paper,PController
import bibtexparser


def main():
    bibtexList = [
        """@article{lecun2015deep,
title={Deep learning},
author={LeCun, Yann and Bengio, Yoshua and Hinton, Geoffrey},
journal={Nature},
volume={521},
number={7553},
pages={436--444},
year={2015},
publisher={Nature Research}
}"""
        ,

        """@inproceedings{kumar2016ask,
title={Ask me anything: Dynamic memory networks for natural language processing},
author={Kumar, Ankit and Irsoy, Ozan and Ondruska, Peter and Iyyer, Mohit and Bradbury, James and Gulrajani, Ishaan and Zhong, Victor and Paulus, Romain and Socher, Richard},
booktitle={International Conference on Machine Learning},
pages={1378--1387},
year={2016}
}"""
        ,
        """@phdthesis{karpathy2016connecting,
title={Connecting Images and Natural Language},
author={Karpathy, Andrej},
year={2016},
school={Stanford University}
}"""
        ,
        """@inproceedings{sukhbaatar2015end,
title={End-to-end memory networks},
author={Sukhbaatar, Sainbayar and Weston, Jason and Fergus, Rob and others},
booktitle={Advances in neural information processing systems},
pages={2440--2448},
year={2015}
}"""
    ]


    # Tables.Paper.drop_table()
    # Tables.InverseIndex.drop_table()
    # Tables.Word.drop_table()
    # Tables.paperIdGenerator.drop_table()
    #
    # Tables.createTables()

    newPaper = Paper.Paper()
    newPController = PController.Pcontroller()
    returnBibtexes = newPController.searchScholar("Albert Einstein","",3)
    for bibtex in returnBibtexes:
        print(bibtex)
    # newPaper = Paper.Paper()
    # newPaper.setMetaByBibtex(testBibtex3)
    # paper = open("documents/test2.pdf","rb")
    # paperContent = paper.read()
    # newPaper.setContent(paperContent)
    # print(len(newPaper.wordContent))
    # print(newPaper.getMeta())
    # print(newPaper.getId())
    # newPaper.upload(paperContent)

    # pcontroller = pc.Pcontroller()
    # p = pcontroller.searchbyContent("word result Skipgram")
    # for m in p:
    #     print(m.id)

    # controller = pc.Pcontroller()
    # controller.watchPaper("NEW",'',None)
    #
    # time.sleep(10)

    # newPaper = Paper.Paper()
    # newPaper.setMetaByBibtex(testBibtex4)
    # paper = open("documents/test3.pdf","rb")
    # paperContent = paper.read()
    # newPaper.setContent(paperContent)
    # print(len(newPaper.wordContent))
    # print(newPaper.getMeta())
    # print(newPaper.getId())
    # newPaper.upload(paperContent)


if(__name__ == "__main__"):
    Tables.createTables()
    main()