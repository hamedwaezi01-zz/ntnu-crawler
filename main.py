from selenium.webdriver import Firefox as TheWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.webelement import FirefoxWebElement as TheWebElement

import pandas as pd

import time
import logging
import pickle

links_in_pickle = True
is_debugging = False
WAIT_DURATION = 3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f_handler = logging.FileHandler(filename="crawler.log", mode='w', encoding='utf-8')
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter('%(asctime)s - %(levelname)s - @{%(lineno)d} - %(name)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)


columns = ["course_id", "course_name", "year", "exam_arrangement", "course_content",
					 "outcome", "methods", "coordinators", "lecturers", "department",
					 "materials", "assignments", "subject_areas", "required_knowledge", "url"]
df = pd.DataFrame(columns=columns)



def extract_data(link: str, driver: TheWebDriver,) -> pd.DataFrame:
	global columns
	retries = 0
	while retries < 5:
		try:
			driver.get(link)
			break
		except Exception:
			logger.debug(f"Retrying for: {link}")
			retries += 1
			time.sleep(1.5)
	if retries >= 5:
		return None

	logger.debug(f"Page loaded: {link}")
	course_id = None
	course_name = None
	try:
		course_id, course_name = driver.find_element_by_xpath("""//div[@id="course-details"]/h1""").text.split('-')[0:2]
	except Exception as e:
		logger.error(e)
	logger.debug(f"Course ID: {course_id}")
	
	
	# record.loc[ 'course_id'] = course_id
	# data={'':course_id, 'course_name': course_name}

	# record[0]['course_id'] = course_id
	# record[0]['course_name'] = course_name
	year = None
	try:
		year = WebDriverWait(driver, WAIT_DURATION).until(EC.presence_of_element_located(
				(By.XPATH, """//select[@id="selectedYear"]/option[contains(@selected,"selected")]"""),
		)).get_attribute("value")
	except TimeoutException:
		pass

	logger.debug(f"Year: {year}")
	# record.loc[ ['year']] = year
	exam_arrangement = None
	try:
		exam_arrangement = WebDriverWait(driver, WAIT_DURATION).until(EC.presence_of_element_located(
			(By.XPATH, """//div[@id="assessment-toggler"]/div[@class="content-assessment"]/p""")
		)).text
	except TimeoutException:
		pass
	logger.debug(f"Exam Arrangement: {exam_arrangement}")
	# record.loc[ ['exam_arrangement']] = exam_arrangement
	course_content = None
	try:
		course_content = WebDriverWait(driver, WAIT_DURATION).until(EC.presence_of_element_located(
			(By.XPATH, """//div[@id="course-content-toggler"]//*[contains(@class,"content-course-content")]""")
		)).text
	except TimeoutException:
		pass
	logger.debug(f"Course Content: {course_content}")
	# record.loc[ ['course_content']] = course_content

	temp = driver.find_elements_by_xpath("""//div[@id="learning-goal-toggler"]/*""")
	outcome = ""
	for t in temp:
		outcome += t.text + "\n"
	outcome = outcome.strip()
	logger.debug(f"Outcome: {outcome}")
	# record.loc[ ['outcome']] = outcome

	temp = driver.find_elements_by_xpath("""//div[@id="learning-method-toggler"]/*""")
	methods = ""
	for t in temp:
		methods += t.text + "\n"
	methods = methods.strip()
	
	logger.debug(f"Methods: {methods}")
	# record.loc[ ['methods']] = methods

	temp = driver.find_elements_by_xpath("""//div[@id="omEmnet"]//div[@class="card"]/div[@class="card-header" and text()="Contact information"]/following-sibling::div/span[text()="Course coordinator:"]/following-sibling::ul[1]/li/a""")
	coordinators = ""
	for t in temp:
		coordinators += t.text + "\n"
	coordinators = coordinators.strip()

	logger.debug(f"Coordinators: {coordinators}")
	# record.loc[ ['coordinators']] = coordinators

	temp = driver.find_elements_by_xpath("""//div[@id="omEmnet"]//div[@class="card"]/div[@class="card-header" and text()="Contact information"]/following-sibling::div/span[contains(text(), "Lecturer")]/following-sibling::ul[1]/li/a""")
	lecturers = ""
	for t in temp:
		lecturers += t.text + "\n"
	lecturers = lecturers.strip()

	logger.debug(f"Lecturers: {lecturers}")
	# record.loc[ ['lecturers']] = lecturers

	department = driver.find_element_by_xpath("""//div[@id="omEmnet"]//div[@class="card"]/div[@class="card-header" and text()="Contact information"]/following-sibling::div/p[contains(text(), "Department")]/a""").text
	logger.debug(f"Department: {department}")
	# record.loc[ ['department']] = department

	temp = driver.find_elements_by_xpath("""//div[@id="course-materials-toggler"]/*""")
	materials = ""
	for t in temp:
		materials += t.text + "\n"
	
	materials = materials.strip()
	logger.debug(f"Materials: {materials}")
	# record.loc[ ['materials']] = materials

	temp = driver.find_elements_by_xpath("""//div[@id="mandatory-activities-toggler"]/ul/li""")
	assignments = ""
	for t in temp:
		assignments += t.text + "\n"

	assignments = assignments.strip()
	logger.debug(f"Assignments: {assignments}")
	# record.loc[ ['assignments']] = assignments

	temp = driver.find_elements_by_xpath("""//div[@id="omEmnet"]//div[@class="card"]/div[@class="card-header" and contains(text(), "Subject area")]/following-sibling::div/ul/li""")
	subject_areas = ""
	for t in temp:
		subject_areas += t.text + "\n"
	
	subject_areas = subject_areas.strip()
	logger.debug(f"Subject Areas: {subject_areas}")
	# record.loc[['subject_areas']]= subject_areas

	required_knowledge = None
	try:
		required_knowledge = driver.find_element_by_xpath("""//div[@id="required-knowledge-toggler"]/p""").text.strip()
	except NoSuchElementException:
		pass
	logger.debug(f"Required Knowledge: {required_knowledge}")
	# record.loc[ ['required_knowledge']] = required_knowledge
	data={"course_id": course_id, 'year':year, 'course_name': course_name, 'exam_arrangement': exam_arrangement,
			'course_content': course_content, 'outcome': outcome, 'methods': methods, 'coordinators': coordinators,
			'lecturers': lecturers, 'department': department, 'materials': materials, 'assignments':assignments,
			'subject_areas': subject_areas, 'required_knowledge': required_knowledge, 'url': link,
	}
	record = pd.DataFrame.from_dict(data=[data,],)
	logger.info(f"New Record created:\n{record}")
	return record





driver = TheWebDriver()
url = """https://www.ntnu.edu/studies/courses#semester=2021&gjovik=false&trondheim=false&alesund=false&faculty=-1&institute=-1&multimedia=false&english=false&phd=false&courseAutumn=false&courseSpring=false&courseSummer=false&pageNo=1&season=autumn&sortOrder=ascTitle"""
driver.get(url)
links = []
if not links_in_pickle:
	logger.info("Finding Fetch more button")
	fetchmore = WebDriverWait(driver, WAIT_DURATION).until(
		EC.presence_of_element_located((By.XPATH, """//button[contains(@class,"fetchmore")]"""))
	)
	logger.info("Fetch more button is found")

	if not is_debugging:
		try:
			while True:
				logger.info("Clicking on fetch more")
				fetchmore.click()
				time.sleep(0.5)
		except ElementNotInteractableException as e:
			logger.info("Finished fetching more page. The link of all classes are now retrievable")



	time.sleep(3)
	logger.info("Extracting the url of courses")
	courses_element = driver.find_elements_by_xpath("""//table[@id="myTable"]/tbody/tr[@class="courserow"]/td[@class='location']/a""")
	

	for el in courses_element:
		links.append(el.get_attribute("href"))

	with open('links.pkl', 'wb') as f:
		pickle.dump(links, f)
	del courses_element

else:
	with open('links.pkl', 'rb') as f:
		links = pickle.load(f)


logger.info(f"Total number of pages to be crawled: #&# {len(links)}")

try:
	for link in links:
		logger.info(f"Starting to Extract link: {link}")
		record = extract_data(link=link, driver=driver)
		if record is not None:
			df = df.append(record)
		logger.debug("Added new record to DataFrame")
		# Respect the server
		time.sleep(1)
except Exception as e:
	# logger.error(f"{e.with_traceback}\n{str(e)}")
	raise e
finally:
	df.to_csv("ntnu_crawled.csv")
	logger.info("Saving CSV file")
	

