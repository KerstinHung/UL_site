from app.models import BirthPlace

places = [
    '荒蠻廢境', '隆茲布魯王國', '異世界', 
    '魯比歐那連合王國', '米利加迪亞王國', 
    '麥歐卡共和國', '荒野', '佛雷斯特希爾', 
    '導都潘德莫尼', '不明', '尹貝羅達', 
    '魔都羅占布爾克', '班賽德', '卡南', 
    '古朗德利尼亞帝國'
]

def run():
    created_cnt = 0
    skipped_cnt = 0
    updated_cnt = 0

    for p in places:
        defaults = dict(name = p,)
        obj, created = BirthPlace.objects.get_or_create(name=p)

        if created:
            created_cnt += 1
        else:
            # 已存在就更新（如果你不想更新，用 continue 即可）
            BirthPlace.objects.filter(pk=obj.pk).update(**defaults)
            updated_cnt += 1

        print(f"BirthPlaces created: {created_cnt}, updated: {updated_cnt}, skipped: {skipped_cnt}")
        print(f"Total birthplaces now: {BirthPlace.objects.count()}")