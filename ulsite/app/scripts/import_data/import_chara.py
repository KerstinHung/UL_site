import csv
from app.models import BirthPlace, Skill, FrenchMonth, Calendar, Character

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
        if peek and (peek[4].strip().isdigit()):
            rows.append(peek)
        rows.extend(reader)

        created_cnt = 0
        skipped_cnt = 0
        updated_cnt = 0

        for row in rows:
            if not row or len(row) < 9:
                continue
            name,jp_name,eng_name,birth_month,birth_day,blood_type,birth_place,height,weight,hobby,title,cv,skill1,skill2,skill3,skill4,exskill1,exskill2,exskill3,exskill4,description_cn,description_jp = row
            # For example:
            # 艾伯李斯特,エヴァリスト,Evarist,雪月,23,A,佛雷斯特希爾,178,67,戰史研究,ReichsRitter,島崎信長,精密射撃,雷撃,茨林,智略,Ex精密射撃,Ex雷撃,Ex茨林,Ex智略,雄心壯志，智勇雙全的帝國騎士。 古朗德利尼亞帝國騎士。以意志和智謀鞏固其在帝國的地位。,グランデレニア帝國騎士。その意志と知略をもって帝國での地位を固める。

            bd_i = _to_int(birth_day)
            height_i = _to_int(height)
            weight_i = _to_int(weight)
            
            birth_month = birth_month.replace("月","")
            month_obj = FrenchMonth.objects.filter(cn_name=birth_month).first() if birth_month else None

            if blood_type not in "ABOAB":
                blood_type = ""

            day_obj = Calendar.objects.filter(fr_m=month_obj, fr_d=bd_i).first() if month_obj and bd_i else None
            skill1_obj = Skill.objects.filter(name=skill1).first() if skill1 else None
            skill2_obj = Skill.objects.filter(name=skill2).first() if skill2 else None
            skill3_obj = Skill.objects.filter(name=skill3).first() if skill3 else None
            skill4_obj = Skill.objects.filter(name=skill4).first() if skill4 else None
            exskill1_obj = Skill.objects.filter(name=exskill1).first() if exskill1 else None
            exskill2_obj = Skill.objects.filter(name=exskill2).first() if exskill2 else None
            exskill3_obj = Skill.objects.filter(name=exskill3).first() if exskill3 else None
            exskill4_obj = Skill.objects.filter(name=exskill4).first() if exskill4 else None
            birth_place_obj = BirthPlace.objects.filter(name=birth_place).first() if birth_place else None

            defaults = dict(
                name = name,
                jp_name = jp_name,
                eng_name = eng_name,
                birth_day = day_obj,
                blood_type = blood_type,
                height = height_i,
                weight = weight_i,
                hobby = hobby,
                title = title,
                description_cn = description_cn,
                description_jp = description_jp,
                skill1 = skill1_obj,
                skill2 = skill2_obj,
                skill3 = skill3_obj,
                skill4 = skill4_obj,
                exskill1 = exskill1_obj,
                exskill2 = exskill2_obj,
                exskill3 = exskill3_obj,
                exskill4 = exskill4_obj,
                birth_place = birth_place_obj,
            )
            defaults = {k: v for k, v in defaults.items() if v is not None}
            obj, created = Character.objects.get_or_create(name=name, defaults=defaults)

            if created:
                created_cnt += 1
            else:
                Character.objects.filter(pk=obj.pk).update(**defaults)
                updated_cnt += 1

        print(f"Characters created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total character now: {Character.objects.count()}")

def run():
    csv_path = '../crawl/csv_data/characters.csv'
    #img_dir = '../images/monsters'
    import_non_img_data(csv_path)
    #import_img(img_dir)