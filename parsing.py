from bs4 import BeautifulSoup
import urllib.request
i = 0
url = 'https://guide.herzen.spb.ru/static/schedule.php'
main_domain = 'https://guide.herzen.spb.ru'
html_doc = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html_doc)
mas = []
for link in soup.findAll('li'):
    i += 1
    link2 = str(link)
    print(link2)

    if((i>256) and (i<294)):
       # print(link2)
       # print(i)
        pos = link2.find('<li>')
        liStarts = '<li>'
        if(pos == -1):
            pos = link2.find('<li class="ev">')
            liStarts = '<li class="ev">'
        lengthOfPos = len(liStarts)
        endOfGroup = link2.find('<div style')
        buttonStarts = link2.find('<button onclick="window.open(')
        lenofbutt = len('<button onclick="window.open(')
        posOfLink = buttonStarts+lenofbutt+1
        lenofhref = len('/static/schedule_view.php?id_group=6976&amp;sem=4')
        href = link2[posOfLink:posOfLink+lenofhref]
        print(href)
        amp = href.find('amp')
        href = href.replace('amp;','',-1)


        print(link2[lengthOfPos:endOfGroup])
        nameOfGruop = (link2[lengthOfPos:endOfGroup])
        #print(lengthOfPos)
        print(endOfGroup)

        mas.append([nameOfGruop,main_domain+href])


print(mas)