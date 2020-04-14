import smtplib
import requests
from bs4 import BeautifulSoup as bs
import re
import configparser

# uses the ini file to store data
my_config_parser = configparser.ConfigParser()
my_config_parser.read('configfile.ini')

# ini file data example
# payload = {
#     'Location': my_config_parser.get('DEFAULT','URL'),
#     'email': my_config_parser.get('DEFAULT','email'),
#     'password': my_config_parser.get('DEFAULT','password')
# }

# print (URL)

#email using smtp
def emailer():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    my_email = my_config_parser['DEFAULT']['my_email']
    my_password = ""

    zto_email = my_config_parser['DEFAULT']['to_email']
    # email = "beatdro6@gmail.com"
    # password = 'jeskajzbqhazztho'
    server.login(my_email, my_password)
    to_email = [zto_email, "mrjanrar@yahoo.com"]
    subject = f"~WCA Competitions Announced in {location}~"
    body = f"Competitions in {location}:"
    msg = f"Subject: {subject} \n\n {body} \n\n {zz}"
    server.sendmail(my_email, to_email, msg)
    print("sent")
    server.quit()

# URL = 'https://www.worldcubeassociation.org/competitions?utf8=%E2%9C%93&region=all&search=Toronto&state=present&year=all+years&from_date=&to_date=&delegate=&display=list'
# URL = 'https://www.worldcubeassociation.org/competitions?utf8=%E2%9C%93&region=_North+America&search=&state=present&year=all+years&from_date=&to_date=&delegate=&display=list'
# head ={"	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}

# parses data from wca
parsed = []
location = (my_config_parser['DEFAULT']['location'])
url = f'http://www.worldcubeassociation.org/competitions?utf8=%%E2%%9C%%93&region=all&search={location}&state=present&year=all+years&from_date=&to_date=&delegate=&display=list'
page = requests.get(url)
soup = bs(page.content, 'lxml')
comp = soup.find_all('li', {'class': "list-group-item not-past"})

# formats text
ok = [i.text.replace('\n', ' ').replace('     ', ' ').strip() for i in comp]
# zz = parsed.extend(link.find_all('.competition-link a'))

# parses links
suburl = 'https://www.worldcubeassociation.org'
alllinks = soup.findAll('a', attrs={'href': re.compile("^/competitions/")})
zz = [suburl + link.get('href') for link in alllinks if ("/competitions/mine" not in link.get('href'))]
for line in ok:
    parsed.append(str(line))

# print (len(parsed))
print(ok)

# for c1, c2 in zip(parsed, zz):
#     print ("%s %s" % (c1, c2))

# joins data and urls to pass to emailer func
zz = ("\n".join("{0}\t{1}".format(a, b) for a, b in zip(parsed, zz)))
print(zz)

if len(zz) >= 3:
    print("comps sending via email")
    emailer()
else:
    print("no comps")
    pass
# ok = soup.find(span ="date")


# print(comp)

# check_WCA()
