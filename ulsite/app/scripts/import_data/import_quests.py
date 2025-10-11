import csv
import os
from app.models import Character, CharacterCard, Monster, Quest, QuestStage, Region

def _to_bool(x):
    if x: return True
    else: return False

def _to_int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None

def import_quest_stage(csv_path: str):
    with open(csv_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        peek = next(reader, None)
        if peek is None:
            print("CSV 是空的")
            return
        rows = []
        rows.extend(reader)

        created_cnt = 0
        skipped_cnt = 0
        updated_cnt = 0

        for row in rows:
            quest_name = row[0]
            quest_obj = Quest.objects.filter(name=quest_name).first() if quest_name else None
            goal = quest_obj.goal

            cntr = 0 # Use mod to determine l/m/r. Use // to determine stage1/2/3...
            for rew in row[len(row)-18:]:
                mod = cntr % 3
                if mod == 0: position = 'L'
                elif mod == 1: position = 'M'
                else: position = 'R'
                stage = (cntr // 3) + 1
                if stage > goal: break

                monster_obj = Monster.objects.filter(name=rew).first() if rew else None
                if ('Lv' in rew):
                    level = _to_int(rew[2])
                    chara = rew[3:]
                elif ('L' in rew) and ('h' not in rew.lower()):
                    level = _to_int(rew[1])
                    chara = rew[2:]
                else:
                    level = 1
                    chara = rew
                chara_obj = Character.objects.filter(name = chara).first() if rew else None
                characard_obj = CharacterCard.objects.filter(card_type = 'Lv', level=level, character=chara_obj).first() if rew else None
                gem = 0
                if ("gem" in rew.lower()): gem = _to_int(rew[:len(rew)-3])
                if not gem: gem=0
                text_reward = ""
                if (not monster_obj) and (not characard_obj) and (not gem): text_reward = rew
                
                # create or update
                defaults = dict(
                    quest = quest_obj,
                    stage = stage,
                    position = position,
                    monster = monster_obj,
                    characard = characard_obj,
                    gem = gem,
                    text_reward = text_reward,
                )
                obj, created = QuestStage.objects.get_or_create(quest = quest_obj, stage=stage, position=position, defaults=defaults)

                if created:
                    created_cnt += 1
                else:
                    QuestStage.objects.filter(pk=obj.pk).update(**defaults)
                    updated_cnt += 1
                cntr += 1
    print(f"QuestStages created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
    print(f"Total questStages now: {QuestStage.objects.count()}")
    return

def import_quest(csv_path: str, region: str):
    # 開啟 CSV 檔案
    with open(csv_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        # 外鍵
        region_obj = Region.objects.filter(name=region).first() if region else None

        reader = csv.reader(csvfile, delimiter=',')

        # 第一列是標頭，跳過
        peek = next(reader, None)
        if peek is None:
            print("CSV 是空的")
            return
        times = peek[1:len(peek)-19]
        # 判斷第一欄是不是數字 id，不是就當標頭；是就當第一筆資料
        rows = []
        # 把剩下的列加進來
        rows.extend(reader)

        created_cnt = 0
        skipped_cnt = 0
        updated_cnt = 0
        
        i = 0
        for row in rows:
            quest_name = row[0]
            goal = row[-19]
            if len(times) == 11:
                min0,min3,min10,min30,hr1,hr2,hr4,hr8,hr16,day1,day3 = row[1:len(row)-19]
            else:
                whole_times = ['0分', '3分', '10分', '30分', '1小時', '2小時', '4小時', '8小時', '16小時', '1天', '3天']
                time_val = [None, None, None, None, None, None, None, None, None, None, None]
                for i in range(len(times)):
                    idx = whole_times.index(times[i])
                    time_val[idx] = row[i+1]
                min0,min3,min10,min30,hr1,hr2,hr4,hr8,hr16,day1,day3 = time_val
            treasure = False
            if (region_obj.area.name in "ShadowLand, MoonLand, Anemonea, AngelLand") and (i <= len(rows)-4) and (i >= len(rows)-6):
                treasure = True
            i+=1

            # 轉型
            boss = False
            if "BOSS" in quest_name: boss = True
            goal_i = _to_int(goal)
            min0_b = _to_bool(min0)
            min3_b = _to_bool(min3)
            min10_b = _to_bool(min10)
            min30_b = _to_bool(min30)
            hr1_b = _to_bool(hr1)
            hr2_b = _to_bool(hr2)
            hr4_b = _to_bool(hr4)
            hr8_b = _to_bool(hr8)
            hr16_b = _to_bool(hr16)
            day1_b = _to_bool(day1)
            day3_b = _to_bool(day3)

            defaults = dict(
                    name = quest_name,
                    boss = boss,
                    treasure = treasure,
                    goal = goal_i,
                    min0 = min0_b,
                    min3 = min3_b,
                    min10 = min10_b,
                    min30 = min30_b,
                    hr1 = hr1_b,
                    hr2 = hr2_b,
                    hr4 = hr4_b,
                    hr8 = hr8_b,
                    hr16 = hr16_b,
                    day1 = day1_b,
                    day3 = day3_b,
                    region = region_obj,
                )
            defaults = {k: v for k, v in defaults.items() if v is not None}
            obj, created = Quest.objects.get_or_create(name=quest_name, defaults=defaults)

            if created:
                created_cnt += 1
            else:
                # 已存在就更新
                Quest.objects.filter(pk=obj.pk).update(**defaults)
                updated_cnt += 1

        print(f"Quests created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total quests now: {Quest.objects.count()}")

def only_update_goal(csv_path: str, region: str):
    with open(csv_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        peek = next(reader, None)
        if peek is None:
            print("CSV 是空的")
            return
        rows = []
        rows.extend(reader)

        skipped_cnt = 0
        updated_cnt = 0
        
        for row in rows:
            quest_name = row[0]
            goal = row[-19]
            goal_i = _to_int(goal)
            obj = Quest.objects.get(name=quest_name)
            if obj:
                Quest.objects.filter(pk=obj.pk).update(goal=goal_i)
                updated_cnt += 1
            else:
                skipped_cnt += 1
        print(f"Quests updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total quests now: {Quest.objects.count()}")

def run():
    
    csv_dir = '../crawl/csv_data/quest_table/'
    paths = os.listdir(csv_dir)
    for p in paths:
        csv_path = os.path.join(csv_dir, p)
        #only_update_goal(csv_path, p.replace(".csv", ""))
        import_quest(csv_path, p.replace(".csv", ""))
        import_quest_stage(csv_path)