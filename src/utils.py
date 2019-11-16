def Singleton(cls):
	'''generic python decorator to make any class
	singleton.'''
	_instances = {}	  # keep classname vs. instance
	def getinstance():
		'''if cls is not in _instances create it
		and store. return the stored instance'''
		if cls not in _instances:
			_instances[cls] = cls()
		return _instances[cls]
	return getinstance


@Singleton
class Config:
    def __init__(self):
        self.vals = {}
    def __setitem__(self,k,v):
        self.vals[k]=v
    def __getitem__(self,k):
        return self.vals[k]
    
    
a=Config()
a['username']='onur'
b=Config()
b['username'] = 'ilker'
print(b['username'])
Config()['filename']='445.txt'
Config()['database']='mysql://localhost/ceng445'
print(Config().vals)