import urllib, urllib2
from bs4 import BeautifulSoup

base_url = 'http://statistici.insse.ro/shop/'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')]

main_links = []
file = open('1_data_list_output.txt', 'w')

soup = BeautifulSoup(opener.open(base_url + '?lang=en').read(),'lxml')
for l in soup.findAll('a'):
   link = str(l.get('href'))
   if link.startswith('index.jsp'):
      main_links.append(base_url + link)
i=0
for sl in main_links:
   soup = BeautifulSoup(opener.open(sl).read())
   for l in soup.findAll('a'):
      link = str(l.get('href'))
      linkname = str(l.text)
      if 'page=tempo' in link and 'ind=' in link:
         i += 1
         print(linkname[:30] + '...'),
         file.write(linkname.strip() + '\n')
         print('done.')

file.close()
print
print('Finished collecting list info with %d elements.' % i)
print

