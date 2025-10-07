from app.models import Area, Region

def run():
    area = "HexRealm"
    area_obj = Area.objects.get(name=area)
    regions = area_obj.regions.all()
    for r in regions:
        print(r.name)