import pynecone as pc

class Foods(pc.Model,table=True):
	food_name:str
	price:int
	stock:int