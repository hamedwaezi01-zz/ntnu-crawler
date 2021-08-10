# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import ElementNotInteractableException

# driver = webdriver.Firefox()
# url = """https://www.ntnu.edu/studies/courses#semester=2021&gjovik=false&trondheim=false&alesund=false&faculty=-1&institute=-1&multimedia=false&english=false&phd=false&courseAutumn=false&courseSpring=false&courseSummer=false&pageNo=398&season=autumn&sortOrder=ascTitle"""
# driver.get(url)


# fetchmore = WebDriverWait(driver, 10).until(
# 	EC.presence_of_element_located((By.XPATH, """//button[contains(@class,"fetchmore")]"""))
# )

# print(fetchmore)

# print(type(fetchmore))



import pickle


links = None
with open("links.pkl", 'rb',) as f:
	links = pickle.load(f)

for i,d in enumerate(links):
	# print(d)
	if "BA6017" in d:
		print(f"{i}/{len(links)} - {i/len(links)}")
