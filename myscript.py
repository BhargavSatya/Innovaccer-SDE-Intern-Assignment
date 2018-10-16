import requests
from bs4 import BeautifulSoup
from googlesearch import search
import datetime,time
import mymysql
import mymail 

global message
base_url="https://www.imdb.com"
global season_no
# Make a google search
def googleSearch(query):
    return next(search(query, tld="co.in", num=1, stop=1, pause=2))
#get the beautified Soup component
def get_soup(url):    
    response= requests.get(url)
    if response.status_code != 200:
        return None
    html= response.text
    soup = BeautifulSoup(html, 'lxml')
    return soup

def get_recent_season(url):    
    soup=get_soup(url)
    titles= soup.findAll('div', {'class': 'titleBar'})
    titles=titles[0].findAll('h1')
    name=titles[0].text
    global message
    message+="\n------------------------------------\n"
    message+="TV series name: "
    message+=name+"\n"
    seasons= soup.findAll('div', {'class': 'seasons-and-year-nav'})
    slinks=seasons[0].findAll('a')
    global season_no
    season_no=slinks[0].text
    surl=slinks[0]['href']
    surl=base_url+surl
    return surl

#SEASONS CHECKING= THE FINAL CHECK
def check_season(dates,flag,epinames):
    global message
    if flag=="nextSeason":
        message+="Status: The next season (%s) begins in "%(season_no)+str(dates[0].year)+"\n"
    
    else:
        today=datetime.date.today()    
        for i,j,no in zip(dates,epinames,range(len(dates))):
            if(today<i):                        
                message+="Status: The next episode [%s]' %s' of 'Season-%s' airs on "%(str(no+1),j,season_no)+i.strftime("%Y-%m-%d")+"\n"
                
                
                break
        else:
            message+="Status: The show has finished streaming all its episodes\n No of Seasons aired : %s \n"%(season_no)
            

# GET LATEST INFO ON THE SERIES
def get_latest(surl):

    soup=get_soup(surl)
    epi=soup.findAll('div',{'class': 'list detail eplist'})
    date=[] 
    epinames=[]
    for item in epi[0].findAll('div',{'class': 'list_item'}):
        ex=item.findAll('div',{'class': 'airdate'})
        nm=item.findAll('div',{'class': 'info'})
        name=nm[0].find_all(['a'],title=True)
        epinames.append(name[0]['title'])
        rd=str(ex[0].text)
        rd=rd.strip()
        rd=rd.replace('.','')
        if rd !='':
            date.append(rd)
    dicMonth={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug": 8, "Sep":9,"Oct":10,"Nov":11,"Dec":12  }
    dates=[]
    flag=""
    for i in date:
        i=i.split(' ')
        d=datetime.date.today()
        if len(i)==3:
            d=datetime.date(int(i[2]), dicMonth[i[1]], int(i[0]))
            flag="current"
        elif len(i)==2:
            d=datetime.date(int(i[1]), dicMonth[i[0]],1)
            flag="noDate"
        else:
            flag="nextSeason"
            d=datetime.date(int(i[0]),1,1)
        dates.append(d)
    
    check_season(dates,flag,epinames)


#MAIN
if __name__ == '__main__':
    db=mymysql.dbConnect()
    global message
    message=""
    email=raw_input("Email address: ")
    series=raw_input("TV Series: ")
    mymysql.insertData(db,email,series)

    series=series.split(",")
    for serial in series:
        query="imdb "+serial+" TV series"
        url= googleSearch(query)
        surl=get_recent_season(url)
        get_latest(surl)

    print(message)
    mymail.sendMail(message,email)
    db.close()



