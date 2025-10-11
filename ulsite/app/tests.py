from django.test import TestCase
from django.test import client
from app.models import Area, Region, Quest
from django.core.management import call_command
# Create your tests here.
class QuestWebpageTestCase(TestCase):

    def setUp(self):
        self.c = client.Client()

        # 建立測試資料
        call_command('runscript', 'import_data.import_areas')
        call_command('runscript', 'import_data.import_regions')
        call_command('runscript', 'import_data.import_calendar')
        call_command('runscript', 'import_data.import_birthplaces')
        call_command('runscript', 'import_data.import_monsters')
        call_command('runscript', 'import_data.import_quests')
        call_command('runscript', 'import_data.import_chara')
        call_command('runscript', 'import_data.import_skills')
        call_command('runscript', 'import_data.import_characard')
        call_command('runscript', 'list_rew_per_region')
    
    def test_quest_visiting(self):
        resp = self.c.get('/quests/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "HexRealm")
        self.assertContains(resp, "MoonLand")
        self.assertContains(resp, "ExQuest")
        self.assertContains(resp, "妖蛆的巢穴")
        self.assertContains(resp, "齋戒之湖")
        self.assertContains(resp, "通往玉座的回廊")
        self.assertTemplateUsed(resp, 'areas.html')