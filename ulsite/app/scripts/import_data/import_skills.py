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
    # 開啟 CSV 檔案
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        # 如果第一列是標頭，就跳過
        peek = next(reader, None)
        if peek is None:
            print("CSV 是空的")
            return
        # 判斷第一欄的ex欄位是不是數字 0或1，不是就當標頭；是就當第一筆資料
        rows = []
        if peek and (peek[1].strip().isdigit()):
            rows.append(peek)  # 第一列就是資料
        # 把剩下的列加進來
        rows.extend(reader)

        created_cnt = 0
        skipped_cnt = 0
        updated_cnt = 0

        for row in rows:
            if not row or len(row) < 9:
                continue
            name,ex,phase,near,mid,far,card,effect1,effect2,effect3,effect4,effect5,base_skill = row

            # 轉型
            ex_b = _to_bool(_to_int(ex))
            near_b = _to_bool(_to_int(near))
            mid_b = _to_bool(_to_int(mid))
            far_b   = _to_bool(_to_int(far))
            if (not near_b) and (not mid_b) and (not far_b):
                near_b = True
                mid_b = True
                far_b = True

            # 外鍵（可為 None）
            base_obj = Skill.objects.filter(name=base_skill).first() if base_skill else None

            # 以 name 去判定是否已存在
            # 若你希望以 id 為唯一鍵，可改成 pk=_to_int(xxx)
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
                # 已存在就更新（如果你不想更新，用 continue 即可）
                Skill.objects.filter(pk=obj.pk).update(**defaults)
                updated_cnt += 1
                # 如果你想跳過而不更新，改成：
                # skipped_cnt += 1
                # continue

        print(f"Skills created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total skills now: {Skill.objects.count()}")

def run():
    base_dir = "/Users/hungciyi/UL_site"
    csv_path = f'{base_dir}/crawl/csv_data/skills.csv'
    #img_dir = f'{base_dir}/images/monsters'
    import_non_img_data(csv_path)
    #import_img(img_dir)