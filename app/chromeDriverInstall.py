import requests
import wget
import zipfile
import os

# get the latest chrome driver version number
def chromeDriverInstall():
	url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
	response = requests.get(url)
	versionNumber = response.text

	if not os.path.isfile(f'chromedriver_{versionNumber}.exe'):
		# build the donwload url
		download_url = "https://chromedriver.storage.googleapis.com/" + versionNumber +"/chromedriver_win32.zip"

		# download the zip file using the url built above
		latest_driver_zip = wget.download(download_url, f'chromedriver.zip')

		# extract the zip file
		with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
			zip_ref.extractall() # you can specify the destination folder path here
		os.rename('chromedriver.exe', f'chromedriver_{versionNumber}.exe')
		# delete the zip file downloaded above
		print(os.path.isfile(f'{latest_driver_zip}'))
		os.remove(latest_driver_zip)
	return versionNumber
