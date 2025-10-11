import csv
from app.models import CharacterCard, Character

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
            id,card_type,level,HP,ATK,DEF,event_gun,event_sword,event_defense,event_special,event_move,event_chance,event_curse,memory,time,soul,light,unlight,chaosium,vanity,crazy,character = row

            if not id:
                continue
            
            # 轉型
            id_i = _to_int(id)
            level_i = _to_int(level)
            hp_i = _to_int(HP)
            atk_i = _to_int(ATK)
            def_i = _to_int(DEF)
            event_gun_i = _to_int(event_gun)
            event_sword_i = _to_int(event_sword)
            event_defense_i = _to_int(event_defense)
            event_special_i = _to_int(event_special)
            event_move_i = _to_int(event_move)
            event_chance_i = _to_int(event_chance)
            event_curse_i = _to_int(event_curse)
            memory_i = _to_int(memory)
            time_i = _to_int(time)
            soul_i = _to_int(soul)
            light_i = _to_int(light)
            unlight_i = _to_int(unlight)
            chaosium_i = _to_int(chaosium)
            vanity_i = _to_int(vanity)
            crazy_i = _to_int(crazy)

            chara_obj = Character.objects.filter(name=character).first() if character else None

            defaults = dict(
                id = id_i,
                card_type = card_type,
                level = level_i,
                HP = hp_i,
                ATK = atk_i,
                DEF = def_i,
                event_gun = event_gun_i,
                event_sword = event_sword_i,
                event_defense = event_defense_i,
                event_special = event_special_i,
                event_move = event_move_i,
                event_chance = event_chance_i,
                event_curse = event_curse_i,
                memory = memory_i,
                time = time_i,
                soul = soul_i,
                light = light_i,
                unlight = unlight_i,
                chaosium = chaosium_i,
                vanity = vanity_i,
                crazy = crazy_i,
                character = chara_obj
            )
            # 過濾掉 None 值
            defaults = {k: v for k, v in defaults.items() if v is not None}

            obj, created = CharacterCard.objects.get_or_create(id = id, defaults=defaults)

            if created:
                created_cnt += 1
            else:
                CharacterCard.objects.filter(pk=obj.pk).update(**defaults)
                updated_cnt += 1

        print(f"CharacterCards created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total CharacterCard now: {CharacterCard.objects.count()}")

def run():
    csv_path = '../crawl/csv_data/characards.csv'
    import_non_img_data(csv_path)