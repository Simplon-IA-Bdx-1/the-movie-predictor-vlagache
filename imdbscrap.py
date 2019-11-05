import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'en_US')


# titre , original_title ,  duration , release_date , rating 

# url = "https://www.imdb.com/title/tt"

# def randomImdbUrl()

url="https://www.imdb.com/title/tt2527338/" #Star Wars 
# url="https://www.imdb.com/title/tt0456123/" #Dikkenek 

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
title_wrapper = soup.find(class_="title_wrapper")


title_str = title_wrapper.findNext('h1').get_text()
title = title_str.split('(')[0]

if title_wrapper.find(class_="originalTitle"):
    original_title_str = title_wrapper.find(class_="originalTitle").get_text()
    original_title = original_title_str.split('(')[0]
else : 
    original_title = title 


subtext = title_wrapper.find(class_="subtext")
subtext_split = subtext.get_text().split('|')

print(subtext_split)
exit()
duration = subtext_split[1].strip()
ranking = subtext_split[0].strip()

release_date_str = subtext.find(title="See more release dates")
release_string = release_date_str.get_text().split('(')[0]
release_date_format = datetime.strptime(release_string.strip(), '%d %B %Y')
release_date_sql_string = release_date_format.strftime('%Y-%m-%d')


duration_str = duration.split('h')
hour = int(duration_str[0])*60
min  = int(duration_str[1].strip().replace('min',''))
duration = hour + min 


if ranking.find('Tous') != -1:
    ranking = 'TP'

print("________________________")
print("Titre : " +title)
if original_title:
    print("Titre original : " + original_title)
print("Ranking : " +ranking)
print("Durée : " + str(duration) + " min ")
print("Date de sortie : " + str(release_date_sql_string))
print("________________________")

