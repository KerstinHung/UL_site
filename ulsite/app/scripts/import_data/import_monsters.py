import csv
import os
from django.core.files import File
from app.models import Monster

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
        # 判斷第一欄是不是數字 id，不是就當標頭；是就當第一筆資料
        rows = []
        if peek and (peek[0].strip().isdigit()):
            rows.append(peek)  # 第一列就是資料
        # 把剩下的列加進來
        rows.extend(reader)

        created_cnt = 0
        skipped_cnt = 0
        updated_cnt = 0

        for row in rows:
            if not row or len(row) < 9:
                continue
            id_str, name, eng_name, level, cost, HP, ATK, DEF, family_id = row

            # 轉型
            id_i = _to_int(id_str)
            level_i = _to_int(level)
            cost_i = _to_int(cost)
            hp_i   = _to_int(HP)
            atk_i  = _to_int(ATK)
            def_i  = _to_int(DEF)
            family_pk = _to_int(family_id)

            # 外鍵（可為 None）
            family_obj = Monster.objects.filter(pk=family_pk).first() if family_pk else None

            # 以 name 去判定是否已存在（你原本就是用 name 當唯一鍵）
            # 若你希望以 id 為唯一鍵，可改成 pk=_to_int(id_str)
            defaults = dict(
                id = id_i,
                name = name,
                eng_name = eng_name or None,
                level    = level_i,
                cost     = cost_i,
                HP       = hp_i,
                ATK      = atk_i,
                DEF      = def_i,
                family   = family_obj,
            )
            obj, created = Monster.objects.get_or_create(name=name, defaults=defaults)

            if created:
                created_cnt += 1
            else:
                # 已存在就更新（如果你不想更新，用 continue 即可）
                Monster.objects.filter(pk=obj.pk).update(**defaults)
                updated_cnt += 1
                # 如果你想跳過而不更新，改成：
                # skipped_cnt += 1
                # continue

        print(f"Monsters created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total monsters now: {Monster.objects.count()}")

def import_img(img_dir: str):
    for monster in Monster.objects.all():
        # 假設檔名規則是用 id 當檔名，例如 "1004.png"
        filename = f"{monster.id}.png"
        filepath = os.path.join(img_dir, filename)

        if not os.path.exists(filepath):
            print(f"[Error] 找不到檔案: {filepath}")
            continue

        # 打開檔案並存進 ImageField
        with open(filepath, "rb") as f:
            monster.image.save(filename, File(f), save=True)

def run():
    base_dir = "/Users/hungciyi/UL_site"
    csv_path = f'{base_dir}/crawl/csv_data/monsters.csv'
    img_dir = f'{base_dir}/images/monsters'
    #import_non_img_data(csv_path)
    import_img(img_dir)

    """
    # 刪除所有 monster
    monsters = Monster.objects.all()
    monsters.delete()
    print(Monster.objects.all())
    """