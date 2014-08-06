#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from soupselect import select
import requests

def main():
	with open('postcodes.txt','r') as f:
	    for line in f:
	        postcode = line.replace(" ","").strip()
	        if scrape(postcode) != 'Invalid':
	        	with open("result.txt", "a") as myfile:
	        	    myfile.write("%s\n"%postcode)

#given a post code, iterate over all the pages
def scrape(postcode,page=1):
	if page == 1:	print "*************** %s *******************"%postcode	
	
	post_url = 'http://finddrivinginstructor.direct.gov.uk/DSAFindNearestWebApp/findNearest.form?postcode=%s&pageNumber=%s'%(postcode,page)
	resp = requests.get(post_url).text
	
	if len(resp) < 8000:
		print "Invalid post codes"
		return 'Invalid'

	soup = BeautifulSoup(resp)
	results_list = select(soup, 'ul.results-list li')
	
	if len(results_list) == 0:		
		print "No more pages left."
		return "no pages left"
	
	print "Page %s"%page

	for i in results_list:
		name = select(i,'h3')[0].get_text()
		detail1 = select(i,'div.instructor-details')[0]
		mail = select(detail1,'a')[0].get('href').split(":")[-1]
		phone = select(detail1,'span')[0].get_text()
		detail2 = select(i,'div.instructor-details')[1]
		
		try:
			select(detail2,'span.cpd')[0]
			cpd = True
		except IndexError:
			cpd = False
			pass
		try:
			select(detail2,'span.cop')[0]
			cop = True
		except IndexError:
			cop = False
		print name,mail,phone,cpd,cop

	return scrape(postcode,page+1)

if __name__ == '__main__':
	main()
	#scrape("s")

