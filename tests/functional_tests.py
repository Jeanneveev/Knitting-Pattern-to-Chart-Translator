# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# class ModelTest():
#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_can_translate_pattern_wo_repeats(self):
#         # Precondition: User is on the homepage
#         self.browser.get("/")

#         # 1. System prompts user to input pattern
#         self.assertIn("Pattern to Chart", self.browser.title)
#         header_text = self.browser.find_element(By.TAG_NAME, "h1").text
#         self.assertIn("Enter Pattern", header_text)

#         # 2. User inputs pattern without any repeats
#         pattern_input = self.browser.find_element(By.ID, "pattern_input")
#         self.assertEqual(pattern_input.get_attribute("placeholder"), "Enter pattern here")

#         pattern_input.send_keys("P1, K2, P2, K1")
#         pattern_input.send_keys(Keys.ENTER)

#         # 3. System updates page, showing corresponding knitting chart
#         chart = self.browser.find_element(By.ID, "chart")

#         # 4. User ends session by leaving page
