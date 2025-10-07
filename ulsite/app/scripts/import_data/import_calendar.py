import csv
from app.models import FrenchMonth, Calendar

def _to_int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None

def import_non_img_data(csv_path: str):
    # Open csv
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        # If the first row is header, skip it
        peek = next(reader, None)
        if peek is None:
            print("CSV 是空的")
            return
        # If the first column is not an int, skip it(It is the header)
        rows = []
        if peek and (peek[0].strip().isdigit()):
            rows.append(peek)  # First row is data
        # Add remaining data
        rows.extend(reader)

        created_cnt = 0
        skipped_cnt = 0
        updated_cnt = 0

        for row in rows:
            if not row or len(row) < 8:
                continue
            id,solar_m,solar_d,fr_m,fr_d,fr_name,en_name,cn_name = row
            print(row[:5])

            # Casting
            id_i = _to_int(id)
            solar_m_i = _to_int(solar_m)
            solar_d_i = _to_int(solar_d)
            fr_d_i   = _to_int(fr_d)

            # Foreign Key
            month_obj = FrenchMonth.objects.filter(fr_name=fr_m).first() if fr_m else None

            # Use `fr_name` for determine exist or not
            # If you want to use `id` as the unique key, use `pk=_to_int(xxx)`
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
                # If Exist, Update it
                Calendar.objects.filter(pk=obj.pk).update(**defaults)
                updated_cnt += 1
                # Do Not Want to Update, You Can:
                # skipped_cnt += 1
                # continue

        print(f"Days created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total skills now: {Calendar.objects.count()}")

def run():
    base_dir = "/Users/hungciyi/UL_site"
    csv_path = f'{base_dir}/crawl/csv_data/french_republican_full.csv'
    import_non_img_data(csv_path)