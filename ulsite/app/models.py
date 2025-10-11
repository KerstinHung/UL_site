# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError

class SkillPhase(models.TextChoices):
            # value(constant), label(variable)
    ATTACK = "ATK", "Attack"
    DEFENSE = "DEF", "Defense"
    OTHER   = "MOV",   "Move"

class CompareOp(models.TextChoices):
    GE = "GE", "≥"
    LE = "LE", "≤"
    EQ = "EQ", "="

class EventCardType(models.TextChoices):
    GUN = "GUN", "Gun"
    SWORD = "SWD", "Sword"
    DEFENSE = "DEF", "Defense"
    SPECIAL = "SPE", "Special"
    MOVE = "MOV", "Move"
    ANY = "ANY", "Any"

class CardType(models.TextChoices):
    NORMAL = "LV", "Lv"
    RARE = "R", "R"
    EP = "EP", "EP"
    REVIVE = "RV", "Revive"

class FrenchMonth(models.Model):
    id = models.IntegerField(primary_key=True)
    fr_name = models.CharField(max_length=11, blank=True, default="")
    cn_name = models.CharField(max_length=1, blank=True, default="")
    image = models.ImageField(upload_to='french_month/', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'french_month'
    
    def __str__(self):
        return self.cn_name

class Calendar(models.Model):
    id = models.IntegerField(primary_key=True)
    solar_m = models.PositiveSmallIntegerField(blank=True, default=0)
    solar_d = models.PositiveSmallIntegerField(blank=True, default=0)
    fr_m = models.ForeignKey(FrenchMonth, on_delete=models.SET_NULL, null=True)
    fr_d = models.PositiveSmallIntegerField(blank=True, default=0)
    fr_name = models.CharField(max_length=15, blank=True, default="")
    en_name = models.CharField(max_length=19, blank=True, default="")
    cn_name = models.CharField(max_length=6, blank=True, default="")

    class Meta:
        managed = True
        db_table = 'calendar'
    
    def __str__(self):
        return self.cn_name

class Monster(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10, blank=True, default="")
    eng_name = models.CharField(max_length=25, blank=True, default="")
    level = models.PositiveSmallIntegerField(db_column='level', blank=True, default=0)
    cost = models.PositiveSmallIntegerField(blank=True, default=0)
    HP = models.PositiveSmallIntegerField(blank=True, default=0)
    ATK = models.PositiveSmallIntegerField(blank=True, default=0)
    DEF = models.PositiveSmallIntegerField(blank=True, default=0)
    image = models.ImageField(upload_to='monsters/', blank=True, null=True)
    family = models.ForeignKey("self", db_column='base_monster_id', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'monster'
    
    def __str__(self):
        return self.name

class BirthPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, blank=True, default="")
    eng_name = models.CharField(max_length=20, blank=True, default="")

    class Meta:
        managed = True
        db_table = 'birthplace'
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    ex = models.BooleanField(blank=True, default=False)
    name = models.CharField(max_length=15, blank=True, default="")
    eng_name = models.CharField(max_length=30, blank=True, default="")
    phase = models.CharField(max_length=15, choices=SkillPhase.choices, default="")
    near = models.BooleanField(blank=True, default=False)
    mid = models.BooleanField(blank=True, default=False)
    far = models.BooleanField(blank=True, default=False)
    card_requirements = models.JSONField(
        default=dict, blank=True,
        help_text="需求卡片/武器數量，例如 {\"gun\": 2} / {\"sword\": 1, \"gun\": 1}"
    )

    base_skill = models.ForeignKey("self", db_column='base_skill_id', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'skill'
    
    def __str__(self):
        return self.name

"""class SkillRequirement(models.Model):
    # One record = one request; Multiple requests for the same skill => "AND" each other。
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="requirements")
    card_type = models.CharField(max_length=16, choices=CardType.choices)
    comparator = models.CharField(max_length=4, choices=CompareOp.choices, default=CompareOp.GE)
    count = models.PositiveSmallIntegerField()

    # If「槍1 / 槍2 / 槍3」are different subclass, can create this column
    subtype = models.CharField(max_length=16, blank=True, null=True)  # 例："1"、"2"、"3"

    class Meta:
        db_table = "skill_requirement"
        indexes = [models.Index(fields=["card_type"])]"""

class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, blank=True, default="")
    eng_name = models.CharField(max_length=15, blank=True, default="")
    jp_name = models.CharField(max_length=10, blank=True, default=0)
    birth_day = models.ForeignKey(Calendar, on_delete=models.SET_NULL, blank=True, null=True)
    blood_type = models.CharField(max_length=3, blank=True, default="")
    height = models.PositiveSmallIntegerField(blank=True, default=0)
    weight = models.PositiveSmallIntegerField(blank=True, default=0)
    hobby = models.CharField(max_length=10, blank=True, default="")
    title = models.CharField(max_length=20, blank=True, default="")
    cv = models.CharField(max_length=6, blank=True, default="")
    description_cn = models.CharField(max_length=100, blank=True, default="")
    description_jp = models.CharField(max_length=50, blank=True, default="")
    
    skill1 = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name="skill1_character")
    skill2 = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name="skill2_character")
    skill3 = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name="skill3_character")
    skill4 = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name="skill4_character")
    exskill1 = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name="exskill1_character")
    exskill2 = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name="exskill2_character")
    exskill3 = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name="exskill3_character")
    exskill4 = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name="exskill4_character")
    
    #related_characters = models.ManyToManyField("self", db_column='related_character_id', on_delete=models.SET_NULL, blank=True, null=True, related_name="related_characters")
    birth_place = models.ForeignKey(BirthPlace, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'character'

    def __str__(self):
        return self.name

class CharacterCard(models.Model):
    class CardType(models.TextChoices):
        NORMAL = "LV", "Normal"
        RARE = "R", "Rare"
        OTHER   = "EP",   "Move"

    id = models.IntegerField(primary_key=True)
    card_type = models.CharField(max_length=3, blank=True, default="")
    level = models.PositiveSmallIntegerField(blank=True, default=0)
    cost = models.PositiveSmallIntegerField(blank=True, default=0)
    HP = models.PositiveSmallIntegerField(blank=True, default=0)
    ATK = models.PositiveSmallIntegerField(blank=True, default=0)
    DEF = models.PositiveSmallIntegerField(blank=True, default=0)
    event_gun = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    event_sword = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    event_defense = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    event_special = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    event_move = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    event_chance = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    event_curse = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    memory = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    time = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    soul = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    light = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    unlight = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    chaosium = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    vanity = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    crazy = models.PositiveSmallIntegerField(blank=True, null=True, default=0)

    character = models.ForeignKey(Character, db_column='character_id', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'character_card'

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column = 'area_name', max_length=10, blank=True, default="")

    class Meta:
        managed = True
        db_table = 'area'
    
    def __str__(self):
        return self.name

class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column = 'region_name', max_length=10, blank=True, default="")
    area = models.ForeignKey(Area, models.SET_NULL, related_name="regions", blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'region'
    
    def __str__(self):
        return self.name

class Quest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='quest_name', max_length=20, blank=True, default="")
    boss = models.BooleanField(blank=True, default=False)
    treasure = models.BooleanField(blank=True, default=False)
    goal = models.PositiveSmallIntegerField(blank=True, default=1)
    min0 = models.BooleanField(db_column='0分', blank=True, default=True)
    min3 = models.BooleanField(db_column='3分', blank=True, default=True)
    min10 = models.BooleanField(db_column='10分', blank=True, default=True)
    min30 = models.BooleanField(db_column='30分', blank=True, default=True)
    hr1 = models.BooleanField(db_column='1小時', blank=True, default=True)
    hr2 = models.BooleanField(db_column='2小時', blank=True, default=True)
    hr4 = models.BooleanField(db_column='4小時', blank=True, default=True)
    hr8 = models.BooleanField(db_column='8小時', blank=True, default=True)
    hr16 = models.BooleanField(db_column='16小時', blank=True, default=True)
    day1 = models.BooleanField(db_column='1天', blank=True, default=True)
    day3 = models.BooleanField(db_column='3天', blank=True, default=True)
    m1 = models.PositiveSmallIntegerField(db_column='M1', blank=True, default=0)  # Field name made lowercase.
    m2 = models.PositiveSmallIntegerField(db_column='M2', blank=True, default=0)  # Field name made lowercase.
    m3 = models.PositiveSmallIntegerField(db_column='M3', blank=True, default=0)  # Field name made lowercase.
    iron = models.PositiveSmallIntegerField(db_column='鐵幣', blank=True, default=0)
    bronze = models.PositiveSmallIntegerField(db_column='銅幣', blank=True, default=0)
    silver = models.PositiveSmallIntegerField(db_column='銀幣', blank=True, default=0)
    gold = models.PositiveSmallIntegerField(db_column='金幣', blank=True, default=0)
    platinum = models.PositiveSmallIntegerField(db_column='白金幣', blank=True, default=0)
    memory = models.PositiveSmallIntegerField(db_column='記憶的碎片', blank=True, default=0)
    time = models.PositiveSmallIntegerField(db_column='時間的碎片', blank=True, default=0)
    soul = models.PositiveSmallIntegerField(db_column='靈魂的碎片', blank=True, default=0)
    light = models.PositiveSmallIntegerField(db_column='生命的碎片', blank=True, default=0)
    unlight = models.PositiveSmallIntegerField(db_column='死亡的碎片', blank=True, default=0)
    region = models.ForeignKey(Region, db_column='region_id', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'quest'
        
    def __str__(self):
        return self.name

class QuestStage(models.Model):
    id = models.AutoField(primary_key=True)
    
    POS_CHOICES = [('L','L'), ('M','M'), ('R','R')]
    quest = models.ForeignKey(Quest, related_name='stages', on_delete=models.CASCADE)
    stage = models.PositiveSmallIntegerField()           # 1..6
    position = models.CharField(max_length=1, choices=POS_CHOICES)

    monster = models.ForeignKey(Monster, null=True, blank=True, on_delete=models.SET_NULL)
    characard = models.ForeignKey(CharacterCard, null=True, blank=True, on_delete=models.SET_NULL)
    gem = models.PositiveSmallIntegerField(default=0) 
    text_reward = models.CharField(max_length=15, default="")

    def clean(self):
        reward_fields = [
            ('monster', self.monster),
            ('characard', self.characard),
        ]

        # Calculate: which columns have value
        set_fields = [name for name, value in reward_fields if value not in (None, '', 0)]

        if len(set_fields) > 1:
            raise ValidationError(
                f"只能設定一種獎勵類型，目前同時設定了: {', '.join(set_fields)}"
            )

    def __str__(self):
        return f"QuestStage(quest={self.quest}, stage={self.stage}, pos={self.position})"
    
    class Meta:
        managed = True
        db_table = 'quest_stage'