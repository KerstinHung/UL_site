from typing import Optional
from django.contrib import admin
from .models import Area, Region, Quest, QuestStage, Monster, BirthPlace, Skill, FrenchMonth, Calendar, Character, CharacterCard

class _NumberFilter(admin.SimpleListFilter):
    title = ""
    parameter_name = "" # URL query string 參數名稱 (?m1=pos)
    field_name = ""

    def lookups(self, request, model_admin):
        return [
            ("pos", "> 0"),
            ("nonpos", "<= 0"),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == "pos":
            return queryset.filter(**{f"{self.field_name}__gt": 0})
        if self.value() == "nonpos":
            return queryset.filter(**{f"{self.field_name}__lte": 0})
        return queryset

def make_sign_filter(field_name: str, *, title: Optional[str] = None, param: Optional[str] = None):
    """工廠：傳欄位名就動態建立一個 Filter 類別"""
    cls_name = f"{field_name.title().replace('_','')}SignFilter"
    attrs = {
        "title": title or field_name,
        "parameter_name": param or f"{field_name}_sign",
        "field_name": field_name,
    }
    return type(cls_name, (_NumberFilter,), attrs)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("name","id")
    search_fields = ("id","name")

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "area",)
    search_fields = ("name",)

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ("name",
                    "min0", "min3", "min10", "min30",
                    "hr1", "hr2", "hr4", "hr8", "hr16",
                    "day1", "day3",)
    fieldsets = (
        ("基本資訊", {
            "fields": ("name", "region", "goal", "boss", "treasure")
        }),
        ("任務時間", {
            "fields": ("min0", "min3", "min10", "min30",
            "hr1", "hr2", "hr4", "hr8", "hr16",
            "day1", "day3",)
        }),
        ("怪物資源", {
            "fields": ("m1", "m2", "m3",)
        }),
        ("金屬資源", {
            "fields": ("iron", "bronze", "silver", "gold", "platinum",)
        }),
        ("碎片資源", {
            "fields": ("memory", "time", "soul", "light", "unlight",)
        }),
    )
    search_fields = ("name",)
    
    list_filter = ["region", "boss", "treasure"]
    list_display_links = ("name",)  # ← 讓「任務名」變成可點的連結

    SIGN_FILTER_FIELDS = ["m1", "m2", "m3",
                          "iron", "bronze", "silver", "gold", "platinum",
                          "memory", "time", "soul", "light", "unlight"]
    def get_list_filter(self, request):
        # 先取得父類（也就是上面 list_filter）的設定
        base = list(super().get_list_filter(request))
        # 依 SIGN_FILTER_FIELDS 動態長出對應的 filter 類別
        dynamic_filters = [make_sign_filter(f, title=f) for f in self.SIGN_FILTER_FIELDS]
        # 合併並回傳
        return tuple(base + dynamic_filters)
    def get_ordering(self, request):
        return ['id']  # sort case insensitive

@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level", "cost", "HP", "ATK", "DEF", "family")
    fieldsets = (
        ("基本資訊", {
            "fields": ("id", "name", "eng_name", "family")
        }),
        ("白值", {
            "fields": ("HP", "ATK", "DEF",)
        }),
        ("其他", {
            "fields": ("cost","image")
        }),
    )
    def get_ordering(self, request):
        return ['id']  # sort case insensitive

@admin.register(BirthPlace)
class BirthPlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "eng_name")
    fields = ("name", "eng_name")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "eng_name", "ex", "phase", "near", "mid", "far", "card_requirements")
    list_filter = ["ex"]
    fields = ("name", "eng_name", "ex", "phase", "near", "mid", "far", "card_requirements", "base_skill")
    def get_ordering(self, request):
        return ['id']  # sort case insensitive

@admin.register(FrenchMonth)
class FrenchMonthAdmin(admin.ModelAdmin):
    list_display = ("id", "fr_name", "cn_name", "image")
    fields = ("id", "fr_name", "cn_name", "image")
    def get_ordering(self, request):
        return ['id']  # sort case insensitive

@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("id", "solar_m", "solar_d", "fr_m", "fr_d", "cn_name")
    fields = ("id", "solar_m", "solar_d", "fr_m", "fr_d", "fr_name", "en_name", "cn_name")
    def get_ordering(self, request):
        return ['id']  # sort case insensitive

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "birth_day", "birth_place", "blood_type", "hobby", "skill1", "skill2", "skill3", "skill4")
    fields = ("name", "eng_name", "jp_name", "birth_day", "birth_place", "blood_type", "height", "weight", "hobby", "title", "cv", "description_cn", "description_jp",
            "skill1", "skill2", "skill3", "skill4", "exskill1", "exskill2", "exskill3", "exskill4"
            )
    def get_ordering(self, request):
        return ['id']  # sort case insensitive

@admin.register(CharacterCard)
class CharacterCardAdmin(admin.ModelAdmin):
    list_display = ("id","character","card_type","level","HP","ATK","DEF","memory","time","soul","light","unlight","chaosium")
    fieldsets = (
        ("基本資訊", {
            "fields": ("id", "character",)
        }),
        ("等級", {
            "fields": ("card_type","level",)
        }),
        ("白值", {
            "fields": ("HP","ATK","DEF",)
        }),
        ("事件卡", {
            "fields": ("event_gun","event_sword","event_defense","event_special","event_move","event_chance","event_curse",)
        }),
        ("碎片資源", {
            "fields": ("memory", "time", "soul", "light", "unlight","chaosium","vanity","crazy")
        }),
    )
    def get_ordering(self, request):
        return ['id']  # sort case insensitive

@admin.register(QuestStage)
class QuestStageAdmin(admin.ModelAdmin):
    list_display = ("quest","stage","position","monster","characard","gem","text_reward")
    fieldsets = (
        ("基本資訊", {
            "fields": ("quest","stage","position")
        }),
        ("獎勵", {
            "fields": ("monster","characard","gem","text_reward")
        }),
    )
    list_filter = ["quest"]
    def get_ordering(self, request):
        return ['id']  # sort case insensitive