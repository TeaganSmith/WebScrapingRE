import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

print("Please enter your property address. Ignore suffixes of 'Rd. , St. , and Ln. ")
print('---------------------------------------------------------------------------')
property_addr = input()
print('---------------------------------------------------------------------------')
# specify the path to chromedriver.exe (change it as needed)
path_to_chromedriver = '/usr/local/bin/chromedriver' 
s = Service(path_to_chromedriver)

browser = webdriver.Chrome(service=s)

# navigate to the URL
url = 'https://bexar.trueautomation.com/clientdb/?cid=110'
browser.get(url)

# find the search field element and fill it with the search query
search_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "propertySearchOptions_searchText")))
search_field.send_keys(property_addr) # replace 'your_search_text' with your actual search text

# submit the form
search_field.send_keys(Keys.RETURN)

# wait for the page to load
WebDriverWait(browser, 10).until(EC.title_contains('Property Search Results')) # the title should change to reflect the new page

# get the page source
html = browser.page_source

# you can now use the page source in BeautifulSoup or close the browser
soup = BeautifulSoup(html, 'html.parser')

# Find the span tag with prop_id attribute
property_id_tag = soup.find('span', attrs={'prop_id': True})

if property_id_tag is not None:
    property_id = property_id_tag['prop_id']  # get the value of prop_id attribute
else:
    property_id = "Not found"

browser.quit()

#Get the information using the property ID
url = 'https://bexar.trueautomation.com/clientdb/Property.aspx?cid=110&prop_id=' + property_id
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

tr_tags = soup.find_all('tr')

#Owner
owner_tag = tr_tags[16] # The owner's name is in the 16th 'tr' tag (Python lists are 0-indexed, so we use 15 as the index)
owner_td_tags = owner_tag.find_all('td') # Find all 'td' tags within the 'tr' tag
propertyOwner = owner_td_tags[1].text

#Neighborhood
neighborhood_tag = tr_tags[13] # The owner's name is in the 16th 'tr' tag (Python lists are 0-indexed, so we use 15 as the index)
neighborhood_td_tags = neighborhood_tag.find_all('td') # Find all 'td' tags within the 'tr' tag
propertyNeighborhood = neighborhood_td_tags[1].text

num = 1
#City / Zip
city_tag = tr_tags[17] # The owner's name is in the 16th 'tr' tag (Python lists are 0-indexed, so we use 15 as the index)
city_td_tags = city_tag.find_all('td') # Find all 'td' tags within the 'tr' tag
propertyCityZip_uncut = city_td_tags[1].text
propertyCityZip = propertyCityZip_uncut.split('  ')[1]
propertyCity = propertyCityZip.split(',')[0]
propertyZip = propertyCityZip.split('TX')[1]

#Legal Description
propertyLegalName = ''
propertyLegal = soup.find_all('td', class_='propertyDetailsLegalDescription')
for output in propertyLegal:
    print('Legal Desc: ' + output.text)

print('Owner: ' + propertyOwner)
print('Neighborhood: ' + propertyNeighborhood)
print('City: ' + propertyCity)
print('Zip Code: ' + propertyZip)

     




#Get the property ID
"""property = input()
url = 'https://bexar.trueautomation.com/clientdb/?cid=110'  # Replace with the form URL
data = {'propertySearchOptions:searchText': property}  # Replace 'my search text' with your search text

response1 = requests.post(url, data=data)

soup = BeautifulSoup(response1.text,'html.parser')

prop_id_tag = soup.find('span', attrs={'prop_id': True})

if prop_id_tag is not None:
    property_id = prop_id_tag['prop_id']  # get the value of prop_id attribute
else:
    property_id = "Not found"

print(property_id)
"""
