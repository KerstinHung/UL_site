from app.models import Area, Region
import csv

def initAdd():
    # 開啟 CSV 檔案
    with open('/Users/hungciyi/UL_site/crawl/csv_data/regions.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for r, a in reader:
            area = Area.objects.get(name=a)
            Region.objects.create(
                name = r,
                area = area
            )

def updateAreaObj():
    with open('/Users/hungciyi/UL_site/crawl/csv_data/regions.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for r, a in reader:
            region_obj = Region.objects.get(name=r)
            area_obj = Area.objects.get(name=a)
            region_obj.area = area_obj
            region_obj.save()

def run():
    updateAreaObj()

    print(Region.objects.all())
    """
    # 刪除所有 region
    regions = Region.objects.all()
    regions.delete()
    print(Region.objects.all())
    """