from django.test import TestCase
from django.test import client
from decouple import config

# Create your tests here.
class QuestWebpageTestCase(TestCase):

    def setUp(self):
        self.c = client.Client()
        self.host = config("HOST_IP")
    
    def test_quest_visiting(self):
        resp = self.c.get('self.host/quests')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "HexRealm")
        self.assertTemplateUsed(resp, 'areas.html')