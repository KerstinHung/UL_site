import csv
from app.models import Skill

def _to_bool(x):
    if x: return True
    else: return False

def _to_int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None

def import_non_img_data(csv_path: str):
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        peek = next(reader, None)
        if peek is None:
            print("CSV 是空的")
            return
        rows = []
        if peek and (peek[1].strip().isdigit()):
            rows.append(peek)
        rows.extend(reader)

        created_cnt = 0
        skipped_cnt = 0
        updated_cnt = 0

        for row in rows:
            if not row or len(row) < 9:
                continue
            name,ex,phase,near,mid,far,card,effect1,effect2,effect3,effect4,effect5,base_skill = row

            ex_b = _to_bool(_to_int(ex))
            near_b = _to_bool(_to_int(near))
            mid_b = _to_bool(_to_int(mid))
            far_b   = _to_bool(_to_int(far))
            if (not near_b) and (not mid_b) and (not far_b):
                near_b = True
                mid_b = True
                far_b = True

            base_obj = Skill.objects.filter(name=base_skill).first() if base_skill else None

            defaults = dict(
                name = name,
                ex = ex_b,
                near = near_b,
                mid = mid_b,
                far = far_b,
                base_skill = base_obj,
            )
            obj, created = Skill.objects.get_or_create(name=name, defaults=defaults)

            if created:
                created_cnt += 1
            else:
                Skill.objects.filter(pk=obj.pk).update(**defaults)
                updated_cnt += 1

        print(f"Skills created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total skills now: {Skill.objects.count()}")

def run():
    csv_path = '../crawl/csv_data/skills.csv'
    import_non_img_data(csv_path)