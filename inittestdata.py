from src import db, malb


db.drop_all()
db.create_all()
malb.synchronize_with_mal('quetzalcoatl384', 'cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', 4448103)
malb.upload_aa_data('./data/aaresults0.txt')