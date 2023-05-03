from django.test import SimpleTestCase
from django.urls import reverse, resolve
from schedule_advisor.views import index, browse, can_add_course, schedule, advisor

class TestUrls(SimpleTestCase):
	def test_index_url_is_resolved(self):
		url = reverse('schedule_advisor:index')
		self.assertEquals(resolve(url).func, index)

	def test_browse_url_is_resolved(self):
		url = reverse('schedule_advisor:browse')
		self.assertEquals(resolve(url).func, browse)

	def test_schedule_url_is_resolved(self):
		url = reverse('schedule_advisor:schedule')
		self.assertEquals(resolve(url).func, schedule)

	def test_advisor_url_is_resolved(self):
		url = reverse('schedule_advisor:advisor')
		self.assertEquals(resolve(url).func, advisor)