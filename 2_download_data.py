import os.path
import urllib, urllib2
from cookielib import CookieJar
from bs4 import BeautifulSoup

base_url = 'http://statistici.insse.ro/shop/index.jsp?page=tempo3&lang=en&ind='
pivot_url = 'http://statistici.insse.ro/shop/excelPivot.jsp'
login_url = 'http://statistici.insse.ro/shop/login'
username = 'molnar.robert87@yahoo.com'
password = 'hammer'
source_list_filename = '1_data_list_output.txt'
##descriptions_filename = '1_data_list_output.txt'

## Login
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')]

values = {'Login': username, 'Password': password, 'FormAction': 'login', 'lang': 'en'}
data = urllib.urlencode(values)
print login_url
response = opener.open(login_url, data)

## Load source code list
f_source_list = open(source_list_filename, 'r')
source_list = f_source_list.readlines()

##f_descriptions = open(

i = 0
for line in source_list:
   i += 1
   table_code = line[:7]
   print('%s - ' % table_code),
   if os.path.exists(table_code + '_data.csv'):
      print('exists, skipping.')
   else:
      page = base_url + table_code
      try:
         soup = BeautifulSoup(opener.open(page).read(),'lxml')
      except urllib2.HTTPError as e:
         print 'page ERROR:', e.code
      else:
         num_listboxes = 0
         num_choices = 0
         encQuery = ''
         for sel in soup.findAll('select'):
            id = str(sel.get('id'))
            valueList = []
            if id.startswith('pos'):
               num_listboxes += 1
               vals = sel.findChildren()
               for v in vals:
                  num_choices += 1
                  valueList.append(str(v.get('value')))
               encQuery = encQuery + ','.join(valueList) + ':'

         encQuery = encQuery[:-1]
         print('%d listboxes, %d choices (%d of %d)...' % (num_listboxes, num_choices, i, len(source_list))),

      ##   desc_output = [table_code]
      ##   desc_table = soup.find('table', 'class'='tempoResults').findChildren
         
      ##   desc_fields

         values = {"lang": "en",
                   "encQuery": encQuery,
                   "matCode": table_code,
                   "x": "8",
                   "y": "7"}

         data = urllib.urlencode(values)
         req = urllib2.Request(pivot_url, data)
         print pivot_url+'?'+ data
         try:
            response = urllib2.urlopen(req)
         except urllib2.HTTPError as e:
            print 'data ERROR:', e.code
         else:
            output = open(table_code + '_data.csv','w')
            #output.write(response.read())
            output.close()
            print("done.")

f_source_list.close()
print
print('Finished collecting data.')
print
