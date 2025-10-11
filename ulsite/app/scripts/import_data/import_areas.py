from app.models import Area
import csv

def initAdd():
    with open('../crawl/csv_data/areas.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for a, b in reader:
            obj, created = Area.objects.get_or_create(name=a)
            if not obj:
                Area.objects.create(
                    name = a
                )

def run():
    initAdd()

    print(Area.objects.all())