from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from icecream import ic
from time import sleep
from . import minimizer

def general_answer(q, PATH):
	url = f'https://duckduckgo.com/?q={q.lower().replace(" ", "+")}&ia=web'

	options = Options()
	options.headless = True

	try:
		driver = webdriver.Chrome(executable_path=PATH, options=options)
	except Exception as e:
		ic(e)
		return "OOPS! Our SEO suggests searching this query in other options! \n THANK YOU! :)"

	driver.get(url)
	sleep(5)

	# get information if card is present
	try:
		less_btn = driver.find_elements_by_class_name("module__toggle--more")
		if len(less_btn):
			for btn in less_btn:
				btn.click()
			result_elements = driver.find_elements_by_class_name("module__text")  # use "module__content to get the full card text"

			textBox = [i.find_element_by_class_name('js-about-item-abstr') for i in result_elements]

			text = '\n'.join([i.text for i in textBox])
			return text
	except:
		pass

	# if card is not present then collect the short summary provided by the site
	try:
		result__snippet = driver.find_elements_by_class_name("result__snippet")
		snippets = [i.text for i in result__snippet]

		result__links = driver.find_elements_by_class_name("result__a")
		links = [i.get_attribute('href') for i in result__links[:3]]


		return minimizer.generate_summary(snippets)

	except:
		pass

# general_answer scrape ends
