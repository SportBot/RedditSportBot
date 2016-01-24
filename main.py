import praw
from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import datetime

#username = input('Reddit username: ')
#password = input('Reddit password: ')

sport = input("sport: ")

# url's obviously
if sport == "nfl":
    url = "http://www.nfl.com/ajax/schedules/matchup?gameId=YYYYMMDDGAMEID&gameState=PRE"

if sport == "nba":
    url = "http://data.nba.com/jsonp/1m/json/cms/2015/tntot/games.json?callback=schedule"

# if nfl, format url with date
if "nfl.com" in url:

    # format current date for url
    gamedate = datetime.datetime.now().strftime("%Y%m%d")
    print ("today is " + today)

    # put the current date into the url, change gameID if needed
    url = url.replace("YYYYMMDD", gamedate)
    url = url.replace("GAMEID", "00")

    # print url
    print (url)

    # load the url
    r = requests.get(url)

    # get json
    data = r.json()

    # prints who plays today
    print (data["homeTeam"]["city"] + " plays today")

    # pretty print json
    #print(json.dumps(data, sort_keys=True, indent=4))



# check if nba url, delete some pesky text
if "nba.com" in url:

    # format current date for searching
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today ="2016-03-10"
    print ("today is " + today)

    # print url
    print (url)

    # load the url
    r = requests.get(url)

    # gets rid of pesky text in json
    r = r.text.replace("schedule(", "")
    r = r.replace(");", "")

    # convert string back to json
    data = json.loads(r)

    # find nba stuff
    for game in data["sports_content"]["games"]:
        if today == game["gameDate"]:
            print (game["visitor"] + " plays " + game["home"])

    # pretty print json
    #print(json.dumps(data, sort_keys=True, indent=4))


#r = urllib.request.urlopen(url).read()
#soup = BeautifulSoup(r, "html.parser")



"""
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
"""
