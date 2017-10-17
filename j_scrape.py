from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import webbrowser as wb

'''
	INDEED "https://www.indeed.com/jobs?q=" + search_query + "&l=Long+Beach%2C+CA"
	CRAIGSLIST "https://" + greater_area_query + "craigslist.org/d/" + field_of_work + "/search/" + minor_area + "/" + field_abbrev
	CAREERONESTOP "https://www.careeronestop.org/Toolkit/Jobs/find-jobs.aspx?keyword=" + keyword + "&location=" + location + "&radius=" + distance
'''

class Listing():
	'''
		Represents a listing or a result from the search query
	'''
	def __init__(self, _title="None", _company="None", _location="None", _date="None", _link="None"):
		self.title = _title
		self.company = _company
		self.location = _location
		self.date = _date
		self.link = _link

	def get_title(self):
		return self.title

	def get_company(self):
		return self.company

	def get_location(self):
		return self.location

	def get_date(self):
		return self.date

	def get_link(self):
		return self.link

def career_one_stop(_keyword, _location, _distance, _size):
	url = "https://www.careeronestop.org/Toolkit/Jobs/find-jobs.aspx?keyword=" + _keyword + "&location=" + _location + "&radius=" + _distance + "&pagesize=" + _size
	# &source=AJE
	j_sauce = urlopen(url).read()
	j_soup = BeautifulSoup(j_sauce, 'html.parser')

	results = j_soup.find('div', {'class': re.compile("div-Messages")})
	num_results = results.find('strong').text
	print(num_results)
	table = j_soup.find('table', {'class': re.compile("res-table")})
	rows = table.findAll('tr')

	#The first item is the table header...
	rows.pop(0)

	info = list()

	for _ in rows:
		title_wrapper = _.find('td', {'data-title': re.compile("Job Title")})
		title = title_wrapper.text.strip()
		link = title_wrapper.find('a').get('href')
		company =_.find('td', {'data-title': re.compile("Company")}).text.strip()
		location = _.find('td', {'data-title': re.compile("Location")}).text.strip()
		date = _.find('td', {'data-title': re.compile("Date Posted")}).text.strip()
		
		item = Listing(_title=title, _company=company, _location=location, _date=date, _link=link)
		info.append(item)

	for _ in info:
		print("  ____  \n")
		print("Title: " + _.get_title() + "\n")
		print("Company: " + _.get_company() + "\n")
		print("Location: " + _.get_location() + "\n")
		print("Date: " + _.get_date() + "\n")
		print("Link: " + _.get_link() + "\n")

	return info

def view_in_browser(view_count=0):
	for i in range(view_count):
			wb.open_new(listings[i].get_link())

if __name__ == "__main__":

	keyword = input("Enter key words for job search: ")
	keyword = keyword.replace(' ', '%20'.format())
	location = input("Enter a zip code: ")
	distance = input("Enter the distance: ")
	size = input("Enter the max number of results: ")

	listings = career_one_stop(_keyword=keyword, _location=location, _distance=distance, _size=size)
	
	n = int(input("How many would you like to open: "))

	view_in_browser(view_count=n)
