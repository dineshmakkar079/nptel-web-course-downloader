import urllib.request
#import urllib2
from bs4 import BeautifulSoup
import os
import sys
from random import randint
import time

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

if __name__ == '__main__':
	startTime = time.time()
	url = sys.argv[1]
	url = 'http://' + url[ url.find('nptel') : ]
	courseId = url.split('/')[4]
	title = ""
	topicList = []
	req = urllib.request.Request(url)
	with urllib.request.urlopen(req) as response:
		html = response.read()
		soup = BeautifulSoup(html, 'lxml')
		title = soup.find('ul', id='breadcrumbs-course').findAll('li')[2].text
		title = title[ : title.find('(') ]
		topicList = [row.text for row in soup.find('div', id='div_lm').findAll('li') if len(row.findChildren()) == 1]

	fileNumber = 1
	BASE_URL = 'http://nptel.ac.in/courses/' + courseId + '/'
	os.mkdir(title)
	prevDirectory = os.getcwd()
	os.chdir(title)
	notDownloadedNumbers = []
	notDownloadedUrls = []

	totalFilesDownloaded = 0
	print("Files Downloaded : \n#0000")
	while True : 
		visitUrl = BASE_URL + str(fileNumber)
		req = urllib.request.Request(visitUrl)
		with urllib.request.urlopen(req) as response:
			html = response.read()
			soup = BeautifulSoup(html, 'lxml')
			iframeElement = soup.find('iframe')
			if iframeElement == None :
				break
			downloadUrlPart = str(iframeElement['src'])
			fileNumberName = str(1000 + fileNumber)[1:] + '. '
			downloadUrl = 'http://nptel.ac.in/courses/' + downloadUrlPart[ downloadUrlPart.find('/') + 1 : ]
			downloadUrl = "%20".join(downloadUrl.split(' '))
			saveFileName = fileNumberName + topicList[fileNumber-1]
			saveFileName = saveFileName.replace("/", "")
			try :	
				urllib.request.urlretrieve( downloadUrl , saveFileName )
				#print("Downloaded : " + saveFileName)
				totalFilesDownloaded = totalFilesDownloaded + 1
				print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
				print("#" + str(10000 + totalFilesDownloaded)[1:] + " : " + saveFileName)
			except FileNotFoundError as f:
				notDownloadedNumbers.append(fileNumber)
				notDownloadedUrls.append(downloadUrl)
				print("Can't download file : " + saveFileName)
		fileNumber = fileNumber + 1
	os.chdir(prevDirectory)
	endTime = time.time()
	if(len(notDownloadedNumbers) == 0):
		print("\nCourse downloaded successfully.\n")
	else : 
		print("Following files were not downloaded : ")
		for i in range(len(notDownloadedNumbers)):
			print(str(1000 + notDownloadedNumbers[i])[1:] + '. ' + topicList[notDownloadedNumbers[i]-1])
			print("Source Url : " + notDownloadedUrls[i])
	print("Total time taken : " + (str("{0:.2f}".format(round(endTime - startTime,2)))) + "s\n")
