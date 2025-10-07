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
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        peek = next(reader, None)
        if peek is None:
            print("CSV 是空的")
            return
        rows = []
        if peek and (peek[0].strip().isdigit()):
            rows.append(peek)
        rows.extend(reader)

        created_cnt = 0
        skipped_cnt = 0
        updated_cnt = 0

        for row in rows:
            if not row or len(row) < 9:
                continue
            id_str, name, eng_name, level, cost, HP, ATK, DEF, family_id = row

            id_i = _to_int(id_str)
            level_i = _to_int(level)
            cost_i = _to_int(cost)
            hp_i   = _to_int(HP)
            atk_i  = _to_int(ATK)
            def_i  = _to_int(DEF)
            family_pk = _to_int(family_id)

            family_obj = Monster.objects.filter(pk=family_pk).first() if family_pk else None

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
                Monster.objects.filter(pk=obj.pk).update(**defaults)
                updated_cnt += 1

        print(f"Monsters created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total monsters now: {Monster.objects.count()}")

def import_img(img_dir: str):
    for monster in Monster.objects.all():
        filename = f"{monster.id}.png"
        filepath = os.path.join(img_dir, filename)

        if not os.path.exists(filepath):
            print(f"[Error] 找不到檔案: {filepath}")
            continue

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