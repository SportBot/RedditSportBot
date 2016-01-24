# editing this file to see what it does

import praw
from bs4 import BeautifulSoup
import urllib.request
import requests

username = input('Reddit username: ')
password = input('Reddit password: ')

"""
r = urllib.request.urlopen('http://espn.go.com/nfl/schedule/_/seasontype/2/week/1').read()
soup = BeautifulSoup(r, "html.parser")
teamnames = soup.find_all("a", class_="team-name")

counter = 0
for element in teamnames:
    #print (element.span.get_text())
    counter = counter + 1
#print (str(counter) + '\n')

tables = soup.find_all("table", attrs={"class":"schedule has-team-logos align-left"})

matrix = [["" for x in range(6)] for x in range(13)]

for table in tables:
    #headers = table.find("thead")

    body = table.find("tbody")
    rows = body.find_all("tr")
    rownum = 0
    for row in rows:
        teamnames = row.find_all("a", class_="team-name")
        items = row.find_all("td")
        colnum = 0
        for element in teamnames:
            #print (element.span.get_text())
            matrix[rownum][colnum] = element.span.get_text()
            colnum = colnum + 1

        for item in items:
            #print (item.a.get_text())
            matrix[rownum][colnum] = item.a.get_text()
            if item.a.get_text():
                colnum = colnum + 1
        #print ("\n")
        rownum = rownum + 1

for row in matrix:
    print (row)
"""


# unique user agent
user_agent = ("coltondot 0.1")

# create reddit instance, r
r = praw.Reddit(user_agent = user_agent)

# reddit stuff
client_id = 'husc2unbAXAvsg'
client_secret = 'gC3IEKuShLx7u5qoxPLzZr6zQeA'
redirect_uri = 'http://127.0.0.1:65010/authorize_callback'
scope = 'identity submit'
state = 'coltonbot!'

# authorize
r.set_oauth_app_info(client_id=client_id,
                      client_secret=client_secret,
                      redirect_uri=redirect_uri)



# accept on web browser open
url = r.get_authorize_url(state,  scope, True)

# browser session
b = requests.Session()
a = b.get(url)

#
headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
payload={'user':username,'passwd':password,'op':'login','dest':url,'api_type':'json'}
a = b.post('https://www.reddit.com/post/login', data=payload, headers=headers)

soup = BeautifulSoup(a.text, "html.parser")

uh = soup.find('input',{'name':'uh'})

uh = uh['value']

payload = {'client_id':client_id,'redirect_uri':redirect_uri,'scope':scope,'state':state,'response_type':'code','duration':'permanent','authorize':'allow','uh':uh}
a = b.post('https://www.reddit.com/api/v1/authorize',data=payload,headers=headers, allow_redirects=False)

code = a.headers['location'].split('&code=',1)[1]
#code = input("code: ")

access_information = r.get_access_information(code)
r.set_access_credentials(**access_information)

#authenticated_user = r.get_me()
#print (authenticated_user.name)
#print (authenticated_user.link_karma)

#sub = input("subreddit: ")
sub = 'SportsBotTest'
title = input("title: ")
body = input("body: ")

r.submit(sub, title, body)
