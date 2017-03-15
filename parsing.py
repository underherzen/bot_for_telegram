import time
from bs4 import BeautifulSoup
import urllib.request
import sqlite3
import imgkit
def GetImage(page, table):
    print(page)
    css = ['bootstrap.css', 'bootstrap.min.css']
    style2 ='''
    <style>

  table{
    margin: 50px 0;
    text-align: left;
    border-collapse: separate;
    border: 1px solid #ddd;
    border-spacing: 10px;
    border-radius: 3px;
    background: #fdfdfd;
    font-size: 14px;
    width: 100%;

  }
  table:nth-child(2) {
    display:none;
    opacity:0;
    position:absolute;


  }
  td,th{
    border: 1px solid #ddd;
    padding: 5px;
    border-radius: 3px;
    text-align: center;
  }
  th{
    background: #E4E4E4;
    font-size: 14px;
    width: 90px;
  }
  caption{
    font-style: italic;
    text-align: right;
    color: #547901;
  }
</style>'''
    style1 = '''<style>

table {
  font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
  font-size: 16px;
  background: white;

  border-collapse: collapse;
  text-align: left;
}
th {
  font-weight: normal;
  color: #039;
  border-bottom: 2px solid #6678b1;
  padding: 10px 8px;
}
td {
  color: #669;
  padding: 9px 8px;
  transition: .3s linear;
  text-align: center;
}
tr:hover td{
  color: #6699ff;
}
		</style>'''
    page = style2 + table + page + '</table>'
    options = {
    'format': 'jpg',
    'encoding': "UTF-8",
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ]
    }
    config = imgkit.config(wkhtmltoimage = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe')

    try:
        image = imgkit.from_string(page, False, config=config, options = options, css = css)
        return image
    except ValueError:
        print('evrthngisok')

a = time.strftime("%A")
if(a=="Sunday"):
    a = "Monday"
print(a)
def get_day(word):
    word = word.title()
    if(word.find("Сегодня")>-1):
        return a
    if(word.find("Понедельник")>-1):
        return "Monday"
    if(word.find("Вторник")>-1):
        return "Tuesday"
    if(word.find("Среда")>-1):
        return "Wednesday"
    if(word.find("Четверг")>-1):
        return "Thursday"
    if((word.find("Пятницу")>-1) or (word.find("Пятница")>-1)):
        return "Friday"
    if(word.find("Суббота")>-1):
        return "Saturday"
    return a



def return_word(word):
    print(word)
    return word

def get_raspisanie_na_den(day, message_id):
    mas_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    mas_of_days_rus = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
    url = 'https://guide.herzen.spb.ru/static/schedule.php'
    main_domain = 'https://guide.herzen.spb.ru'
    html_doc = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_doc)
    mas = []

    print(day)
    ivt = 'бакалавриат, 3 курс, группа ИВТ '
    i = 0
    conn = sqlite3.connect('faks.db')
    c = conn.cursor()
    c.execute('SELECT institut FROM users WHERE message_id = ?',(message_id,))
    inst = c.fetchone()
    inst = list(inst)
    inst = inst[0]
    print(str(inst))
    url_of_rasp = ''
    soup = str(soup)
    day = day.lower()
    soup = soup.lower()
    inst_starts = soup.find(inst)
    print(inst_starts)
    soup = soup[inst_starts:len(soup)]
    soup = BeautifulSoup(soup)
    #print(soup)
    c.execute('SELECT fakultet FROM users WHERE message_id = ? ',(message_id,))
    ivt = c.fetchone()
    ivt = list(ivt)
    ivt = ivt[0]
    checkingGroup = 0
    for link in soup.findAll('li'):
        i += 1
        link2 = str(link)
        #print(link2)
        ivt2 = link2.find(ivt)
        if( (ivt2>-1) and (checkingGroup == 0)):
            checkingGroup = 1
           # print(link2)
           # print(i)
            posOfLink = link2.find('/static/schedule_view')
            lenofhref = link2.find("', '_blank'")
            href = link2[posOfLink:lenofhref]
            print(href)
            href = href.replace('amp;','',-1)
            url_of_rasp = main_domain + href
    count = 0
    print(url_of_rasp)
    page = urllib.request.urlopen(url_of_rasp).read()
    page = BeautifulSoup(page)
    page = str(page)
    #page = get_podgrup(page)
    zachet = page.find('Зачеты')
    page = page[0:zachet]
    #page = str(page)
    #page = re.sub(r'(\<(/?[^>]+)>)', '', page)
    check = 0
    #print(page)
    for day_of_week in mas_of_days_rus:
        #print(mas_of_days_rus)
        #print(mas_of_days)
        count+=1
        if(page.find(day_of_week)<0):
            if(day == mas_of_days[count-1]):
                check = 1
            #print(day_of_week)
            mas_of_days_rus.pop(count-1)
            mas_of_days.pop(count-1)
    if(check == 1): day = mas_of_days[0]
    Table_starts = page.find('<table')
    print(mas_of_days)
    Table_ends = page.find(mas_of_days_rus[0])
    table = page[Table_starts:Table_ends]
    print(mas_of_days_rus)
    print(mas_of_days)
    if(day==mas_of_days[len(mas_of_days)-1].lower()):
        day_starts1 = mas_of_days_rus[len(mas_of_days_rus)-1]
        day_starts=page.find(day_starts1)
        day_ends=page.find('Зачеты')
        #print(day_starts)
        #print(day_ends)
        page = page[day_starts:day_ends]
        page = GetImage(page, table)
        print(day_starts)
        print(day_ends)
        return page
    else:
        count = 0
        for day_of_week in mas_of_days:
            count+=1

            if(day == day_of_week.lower()):
                day_starts1 = mas_of_days_rus[count-1]
                day_starts = page.find(day_starts1)
                day_ends = page.find((mas_of_days_rus[count]))
                #print(day_starts)
                #print(day_ends)
                page = page[day_starts:day_ends]
                page = GetImage(page, table)
                print(day_starts)
                print(day_ends)
                print(page)
                return page


    print(mas_of_days)

    return page















