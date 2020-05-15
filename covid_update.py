import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from socket import error
import json
from datetime import datetime

ste_codes= {
    "State Codes":["AN","AP","AR","AS","BH","CH","CT","DN","DL","GA","GJ","HR","HP","JK","JH","KA","KL","LA","MP","MH","MN","ME","MI","OR","PY","PB","RJ","TN","TS","TR","UT","UP","WB"]
}
details = []
state_name = []
up = []
down = []
done = []
index = []
diction = {
    "State/UT" : state_name,
    "Active" : up,
    "Inactive" : down,
    "Deceased" : done,
    "dt":None
}

def get_and_create_data_strcut():
    global details,up,down,done,state_name,index,diction

    try:
        resp = requests.get("https://www.mohfw.gov.in/")
        
    except error as err:
        print("Request cannot be made, check connectivity or retry after some time\nChecking if offline data available......")
        return False
    
    soup = BeautifulSoup(resp.text,"html.parser")
    sec = soup.find(id= 'state-data')
    for sd in sec.find_all('td'):
        details.append(sd.string)

    details = details[0:len(details)-4]
    state_count = 0
    i=0
    while state_count < 33 :
        index.append(details[i])
        state_name.append(details[i+1])
        state_count+=1
        up.append(int(details[i+2]))
        down.append(int(details[i+3]))
        done.append(int(details[i+4]))
        i+=5
        
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    diction['State/UT'] = state_name
    diction['Active'] = up
    diction['Inactive'] = down
    diction['Deceased'] = done
    diction['dt'] = current_time
    return True

def save_json(diction):
    with open('data.json','w+') as fl:
        data = json.dumps(diction,indent= 4)
        fl.write(data)
        return True

def remove_element(obj,key):
    ob = dict(obj)
    del ob[key]
    return ob
    
def open_json():
    try:
        with open('data.json','r+') as fl:
            data = json.loads(s= fl.read())
            return data
    except FileNotFoundError:
        print("Offline Data Not available\nOnce Online,Data will be saved.\nTry again later or check internet connectivity")
        return False

def print_console_dict(obj):
    global details,index,ste_codes
    obj = {**obj,**ste_codes}
    res = pd.DataFrame(data= remove_element(obj,'dt'))
    if index != []:
        res.index = index
    print("\n\n")
    print(res,"\n")
    if details != []:
        print(details[-2]," ",details[-1])
    else:
        print("Total number of confirmed cases in India ",sum(obj['Active']),"*")
    print("\nLast Updated at ",obj['dt'])
    
def make_plt(stut,ac,dec,inac):
    global ste_codes
    a1,a2,a3 = 0,0,0
    fig,(a1,a2,a3) = plt.subplots(nrows= 3,ncols=1,sharex= True, sharey= True)
    a1.bar(stut,ac,color= 'r')
    a1.set(title= "Active",ylabel="Cases")
    a2.bar(stut,inac,color= 'm')
    a2.set(title= "Inactive",ylabel="Cases")
    a3.bar(stut,dec)
    a3.set(title= "Deceased",ylabel="Cases",xlabel= " State/UT")
    plt.xticks(stut, ste_codes['State Codes'], rotation=90)
    fig.canvas.set_window_title('Covid-19 India Updates')
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.15)
    fig.tight_layout()
    plt.show()
    
def main():
    global details,up,down,done,state_name,index,diction
    
    if get_and_create_data_strcut() == True:
        print_console_dict(diction)
        save_json(diction)
        make_plt(state_name,up,done,down)
    else:
        data = open_json()
        if data != False:
            print_console_dict(data)
            make_plt(data['State/UT'],data['Active'],data['Deceased'],data['Inactive'])
        
main()
