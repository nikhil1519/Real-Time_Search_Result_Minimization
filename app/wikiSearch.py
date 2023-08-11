import wikipedia
from . import generalSearch as gen

# wikipedia scrape begins
def scrape_wikipedia(qry, Path):
	try:
		page_py = wikipedia.page(qry)
	except:
		return gen.general_answer(qry, Path)
	return page_py.summary

