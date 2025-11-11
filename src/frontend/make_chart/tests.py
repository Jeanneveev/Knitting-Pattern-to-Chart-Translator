from django.test import TestCase
from django.http import HttpRequest
from make_chart.views import input_page

# Create your tests here.
class InputPageTest(TestCase):
    def test_view_returns_correct_html(self):
        request = HttpRequest()
        response = input_page(request)
        html = response.content.decode("utf8")

        self.assertIn("<title>Pattern to Chart", html)
    
    def test_url_returns_correct_template(self):
        # TODO: REMEMBER TO CHANGE WHEN ROUTE CHANGES LATER
        response = self.client.get("/")
        self.assertTemplateUsed(response, "input.html")

    def test_url_returns_correct_content(self):
        response = self.client.get("/")
        self.assertContains(response, '<form action="" method="POST">')
        self.assertContains(response, '<input type="text" name="pattern_input"')

    def test_can_respond_to_POST_request(self):
        response = self.client.post("/", data={"pattern_input": "k2, p2"})
        self.assertContains(response, "| - | - |   |   |")
