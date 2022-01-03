import requests
import lxml
from bs4 import BeautifulSoup
from xlwt import *

workbook = Workbook(encoding = 'utf-8')
table = workbook.add_sheet('data')
table.write(0, 0, 'Number')
table.write(0, 1, 'movie_url')
table.write(0, 2, 'movie_name')
table.write(0, 3, 'movie_introduction')
line = 1

url = "https://www.rottentomatoes.com/top/bestofrt/"
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

page = requests.get(url, headers = headers)
movies_lst = []
soup = BeautifulSoup(page.content,'html.parser')

movies = soup.find('table', {'class': 'table' }).find_all('a')
num = 0
for anchor in movies[0:25]:
  urls = 'https://www.rottentomatoes.com' + anchor['href']
  movies_lst.append(urls)
  num += 1
  movie_url = urls
  movie_f = requests.get(movie_url, headers = headers)
  movie_soup = BeautifulSoup(movie_f.content, 'html.parser')
  movie_content = movie_soup.find('div', {'class': 'movie_synopsis clamp clamp-6 js-clamp'})
  print(num, urls, '\n', 'Movie:' + anchor.string.strip())
  print('Movie info:' + movie_content.string.strip())
  
  table.write(line, 0, num)
  table.write(line, 1, urls)  
  table.write(line, 2, anchor.string.strip())
  table.write(line, 3, movie_content.string.strip())
  line += 1
  workbook.save('movies_top25.xls')