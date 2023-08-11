from django.shortcuts import render
from django.http import JsonResponse

import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

from . import wikiSearch as wiki
from . import generalSearch as gen
from . import chromeDriverInstall as chromeDriver

from icecream import ic

nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

try:
	versionNumber = chromeDriver.chromeDriverInstall()
	ic(versionNumber)
except:
	ic("Unable to download chromedriver")
	exit()

Driver_Path = f"chromedriver_{versionNumber}.exe"

def get_continuous_chunks(text):
	chunked = ne_chunk(pos_tag(word_tokenize(text)))
	continuous_chunk = []
	current_chunk = []

	for i in chunked:
		if type(i) == Tree:  # extract the markonikov tree
			current_chunk.append(" ".join([token for token, pos in i.leaves()]))
		elif current_chunk:
			named_entity = " ".join(current_chunk)
			if named_entity not in continuous_chunk:
				continuous_chunk.append(named_entity)
				current_chunk = []
		else:
			continue
	if current_chunk:
		named_entity = " ".join(current_chunk)
		if named_entity not in continuous_chunk:
			continuous_chunk.append(named_entity)
			current_chunk = []
	return continuous_chunk

def home(request):
	return render(request, 'app/home.html')


def error(request):
	return render(request, 'app/404.html')


def about(request):
	return render(request, 'app/about.html')

def search(request):
	if request.method == 'POST':
		qry_entered = request.POST.get('query')
		site = request.POST.get('site')
		ic(qry_entered, site)

		query = qry_entered.title()
		NE = get_continuous_chunks(query)
		if (len(NE) == 0):
			NE = query
		else:
			NE = ' '.join(NE)
		result_dict = {'query': NE}

		site_dict = {'ans': gen.general_answer(query, Driver_Path), 'site': 'General'} if site=='1' else\
					{'ans': wiki.scrape_wikipedia(query, Driver_Path), 'site': 'Wikipedia'}

		result_dict.update(site_dict)
		return JsonResponse(result_dict)
		# {'dict':qry_entered,'search_results_key':scrape_function(qry_entered)})
	else:
		return render(request, 'app/search.html')

def developers(request):
	return render(request, 'app/developers.html')
