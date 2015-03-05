from app import db, malb
import os.path

db.drop_all()
db.create_all()
malb.synchronize_with_mal('quetzalcoatl384', 'cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk')

i = 0
filename = "./data/aaresults"
while(os.path.isfile(filename+str(i)+".txt")):
	print("Processing datafile: "+str(i))
	malb.upload_aa_data(filename+str(i)+".txt")
	i += 1
