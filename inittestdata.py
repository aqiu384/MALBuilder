from src import db, malb
from unittests.BaseMalbTester import init_test_mal

db.drop_all()
db.create_all()
init_test_mal()
malb.synchronize_with_mal('quetzalcoatl384', 'cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', 4448103)
malb.upload_aa_data('./data/aaresults0.txt')