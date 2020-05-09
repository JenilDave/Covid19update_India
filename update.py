import requests
from bs4 import BeautifulSoup
import pandas as pd

details = []
state_name = []
up = []
down = []
done = []
index = []
state_count = 0

resp = requests.get("https://www.mohfw.gov.in/")
soup = BeautifulSoup(resp.text,"html.parser")
sec = soup.find(id= 'state-data')
#print(state_data.find_all('td'))
for sd in sec.find_all('td'):
    details.append(sd.string)

details = details[0:len(details)-4]

i=0
while state_count < 33 :
    #print(i)
    index.append(details[i])
    state_name.append(details[i+1])
    state_count+=1
    up.append(details[i+2])
    down.append(details[i+3])
    done.append(details[i+4])
    i+=5

diction = {
    "State" : state_name,
    "Active" : up,
    "Inactive" : down,
    "Deceased" : done
}

res = pd.DataFrame(diction)
res.index = index
print("\n\n")
print(res,"\n")
print(details[-2]," ",details[-1])