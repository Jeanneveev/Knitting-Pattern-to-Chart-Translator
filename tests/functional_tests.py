import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class MakeChartTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_translate_pattern_wo_repeats(self):
        # Precondition: User is on the homepage
        self.browser.get("http://localhost:8000")

        # 1. System prompts user to input pattern
        self.assertIn("Pattern to Chart", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Enter Pattern", header_text)

        # 2. User inputs pattern without any repeats
        pattern_input = self.browser.find_element(By.ID, "pattern_input")
        self.assertEqual(pattern_input.get_attribute("placeholder"), "Enter pattern here")

        pattern_input.send_keys("row 1: P1, K2, P2, K1")
        pattern_input.send_keys(Keys.ENTER)

        ## wait for form to send
        time.sleep(5)

        # 3. System updates page, showing corresponding knitting chart
        chart = self.browser.find_element(By.ID, "chart")
        chart_text = chart.text
        expected = (
            "---+---+---+---+---+---+---+---\n"
            "   |   | - | - |   |   | - | 1 \n"
            "---+---+---+---+---+---+---+---"
        )

        self.assertIn(expected, chart_text)

        # 4. User ends session by leaving page
            ## Done automatically via tearDown()

if __name__ == "__main__":
    unittest.main()