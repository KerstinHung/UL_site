import csv
from app.models import FrenchMonth, Calendar

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
        # 判斷第一欄的id是不是數字，不是就當標頭；是就當第一筆資料
        rows = []
        if peek and (peek[0].strip().isdigit()):
            rows.append(peek)  # 第一列就是資料
        # 把剩下的列加進來
        rows.extend(reader)

        created_cnt = 0
        skipped_cnt = 0
        updated_cnt = 0

        for row in rows:
            if not row or len(row) < 8:
                continue
            id,solar_m,solar_d,fr_m,fr_d,fr_name,en_name,cn_name = row
            print(row[:5])

            # 轉型
            id_i = _to_int(id)
            solar_m_i = _to_int(solar_m)
            solar_d_i = _to_int(solar_d)
            fr_d_i   = _to_int(fr_d)

            # 外鍵（可為 None）
            month_obj = FrenchMonth.objects.filter(fr_name=fr_m).first() if fr_m else None

            # 以 fr_name 去判定是否已存在
            # 若你希望以 id 為唯一鍵，可改成 pk=_to_int(xxx)
            defaults = dict(
                id = id_i,
                solar_m = solar_m_i,
                solar_d = solar_d_i,
                fr_m = month_obj,
                fr_d = fr_d_i,
                fr_name = fr_name,
                en_name = en_name,
                cn_name = cn_name,
            )
            obj, created = Calendar.objects.get_or_create(fr_name=fr_name, defaults=defaults)

            if created:
                created_cnt += 1
            else:
                # 已存在就更新（如果你不想更新，用 continue 即可）
                Calendar.objects.filter(pk=obj.pk).update(**defaults)
                updated_cnt += 1
                # 如果你想跳過而不更新，改成：
                # skipped_cnt += 1
                # continue

        print(f"Days created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total skills now: {Calendar.objects.count()}")

def run():
    base_dir = "/Users/hungciyi/UL_site"
    csv_path = f'{base_dir}/crawl/csv_data/french_republican_full.csv'
    import_non_img_data(csv_path)