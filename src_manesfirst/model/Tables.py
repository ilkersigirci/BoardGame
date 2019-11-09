import peewee

myDB = peewee.SqliteDatabase("ceng445")


class Paper(peewee.Model):
    title = peewee.CharField()
    content = peewee.BlobField()
    author = peewee.TextField()
    metaData = peewee.CharField()
    id = peewee.PrimaryKeyField(primary_key=True)


    class Meta:
        database = myDB


class Word(peewee.Model):
    word = peewee.CharField()

    class Meta:
        database = myDB



class InverseIndex(peewee.Model):
    paper = peewee.ForeignKeyField(Paper)
    word = peewee.ForeignKeyField(Word)

    class Meta:
        database = myDB

class paperIdGenerator(peewee.Model):
    currentId = peewee.BigIntegerField()
    class Meta:
        database = myDB


def createTables():
    try:
        Paper.create_table(Paper)
        Word.create_table(Word)
        InverseIndex.create_table(InverseIndex)
        if(not paperIdGenerator.table_exists()):
            paperIdGenerator.create_table(paperIdGenerator)
            id = paperIdGenerator()
            id.currentId = 1
            id.save()

    except peewee.OperationalError as e:
        print(e)






