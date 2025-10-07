from app.models import Character, CharacterCard, Monster, Quest, QuestStage, Region
import os

def get_quest_rew(region: str):
    region_obj = Region.objects.filter(name=region).first() if region else None
    quest_objs = Quest.objects.filter(region=region_obj) if region else None
    toReturn = {}
    for q in quest_objs:
        qss = q.stages.all()
        gems = 0
        m123 = [0,0,0]
        chara = []
        iron = 0
        bronze = 0
        silver = 0
        gold = 0
        platinum = 0
        memory = 0
        time = 0
        soul = 0
        light = 0
        unlight = 0
        for i in range(1,7):
            l = qss.filter(stage=i, position='L').first()
            m = qss.filter(stage=i, position='M').first()
            r = qss.filter(stage=i, position='R').first()
            lm = l.monster.level if l.monster else 0
            mm = m.monster.level if m.monster else 0
            rm = r.monster.level if r.monster else 0
            for i in range(1,4):
                if lm == i or mm == i or rm == i: m123[i-1]+=1
            lc = l.characard
            mc = m.characard
            rc = r.characard
            if lc: chara.append(lc.character.name)
            if mc: chara.append(mc.character.name)
            if rc: chara.append(rc.character.name)
            gems += max(l.gem, m.gem, r.gem)
            lt = l.text_reward
            mt = m.text_reward
            rt = r.text_reward
            raw_txt = ''
            if ("鐵幣" in lt) or ("鐵幣" in mt) or ("鐵幣" in rt): iron += 1
            if ("銅幣" in lt) or ("銅幣" in mt) or ("銅幣" in rt): bronze += 1
            if ("銀幣" in lt) or ("銀幣" in mt) or ("銀幣" in rt): silver += 1
            if ("金幣" in lt) or ("金幣" in mt) or ("金幣" in rt): gold += 1
            if ("白金幣" in lt) or ("白金幣" in mt) or ("白金幣" in rt): platinum += 1
            if ("記憶的碎片" in lt) or ("記憶的碎片" in mt) or ("記憶的碎片" in rt): memory += 1
            if ("時間的碎片" in lt) or ("時間的碎片" in mt) or ("時間的碎片" in rt): time += 1
            if ("靈魂的碎片" in lt) or ("靈魂的碎片" in mt) or ("靈魂的碎片" in rt): soul += 1
            if ("生命的碎片" in lt) or ("生命的碎片" in mt) or ("生命的碎片" in rt): light += 1
            if ("死亡的碎片" in lt) or ("死亡的碎片" in mt) or ("死亡的碎片" in rt): unlight += 1
            raw_txt += f"{lt},{mt},{rt},"
        toReturn[q.name] = {'m1': m123[0], 'm2': m123[1], 'm3': m123[2], 
                            'iron': iron, 'bronze': bronze, 'silver': silver, 'gold': gold, 'platinum': platinum,
                            'memory': memory, 'time': time, 'soul': soul, 'light': light, 'unlight': unlight,
                            'chara': chara,'gem':gems,'raw_txt':raw_txt}
    return toReturn

def write_rew(quest_name: str, rews: dict):
    quest_obj = Quest.objects.filter(name=quest_name).first() if quest_name else None
    if not quest_obj: return
    """
    quest_obj.update(m1=rews['m1'],m2 = rews['m2'],m3 = rews['m3'],
                     iron = rews['iron'],bronze = rews['bronze'],silver = rews['silver'],gold = rews['gold'],
                     memory = rews['memory'],time = rews['time'],soul = rews['soul'],light = rews['light'],unlight = rews['unlight'])
    """ 
    quest_obj.m1 = rews['m1']
    quest_obj.m2 = rews['m2']
    quest_obj.m3 = rews['m3']
    quest_obj.iron = rews['iron']
    quest_obj.bronze = rews['bronze']
    quest_obj.silver = rews['silver']
    quest_obj.gold = rews['gold']
    quest_obj.platinum = rews['platinum']
    quest_obj.memory = rews['memory']
    quest_obj.time = rews['time']
    quest_obj.soul = rews['soul']
    quest_obj.light = rews['light']
    quest_obj.unlight = rews['unlight']
    quest_obj.save()
    print(f"{quest_obj}: m1={quest_obj.m1}, m2={quest_obj.m2}, m3={quest_obj.m3}")

def run():
    
    csv_dir = '/Users/hungciyi/UL_site/crawl/csv_data/quest_table/'
    regions = os.listdir(csv_dir)
    for region in regions:
        region = region.replace(".csv","")
        results = get_quest_rew(region)
        for q,r in results.items():
            #print(q,r)
            write_rew(q,r)
    """
    results = get_quest_rew("白魔的圓環石陣")
    for q,r in results.items():
            #print(q,r)
            write_rew(q,r)
    """
    