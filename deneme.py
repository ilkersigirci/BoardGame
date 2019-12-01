import json


stateChange = {"player":"ilker",
				"actions":[]
				}

stateChange.update( {'before' : 23} )
stateChange["actions"].append({"skip": 5})
stateChange["actions"].append({"hello": 6})
#stateChange.append()
	
stateChange.update([ ('where', 4) , ('who', 5) , ('why', 6)] )
dict2 = {'dict2_1' : 4 ,'dict2_2' : 5}
stateChange.update(dict2)

print(json.dumps(stateChange, indent = 2))