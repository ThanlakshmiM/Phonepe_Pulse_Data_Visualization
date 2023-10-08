# import Library
import pandas as pd
import requests
import json
import os

# Cloning
#!git clone https://github.com/PhonePe/pulse.git

# Aggregate Transaction
Agg_trans_path="/content/pulse/data/aggregated/transaction/country/india/state/"
Agg_trans_state_list=os.listdir(Agg_trans_path)
(Agg_trans_state_list).sort()
# Agg trans find all data
Agg_trans={'State':[],'Transaction_Year':[],'Quaters':[],'Transaction_type':[],'Transaction_count':[],'Transaction_amount':[]}
for s in Agg_trans_state_list:
  paths=Agg_trans_path+s+"/"
  Agg_yr=os.listdir(paths)
  for y in Agg_yr:
    paths1=paths+y+'/'
    Agg_yr_l=os.listdir(paths1)
    for yl in Agg_yr_l:
      paths2=paths1+yl
      Data=open(paths2,'r')
      D=json.load(Data)
      for z in D['data']['transactionData']:
        Name=z['name']
        Count=int(z['paymentInstruments'][0]['count'])
        Amount=z['paymentInstruments'][0]['amount']
        Agg_trans['Transaction_type'].append(Name)
        Agg_trans['Transaction_count'].append(Count)
        Agg_trans['Transaction_amount'].append(Amount)
        Agg_trans['State'].append(s)
        Agg_trans['Transaction_Year'].append(y)
        Agg_trans['Quaters'].append(int(yl.strip('.json')))


# Aggregate User 
Agg_user_path="/content/pulse/data/aggregated/user/country/india/state/"
Agg_user_state_list=os.listdir(Agg_user_path)
(Agg_user_state_list).sort()
#Agg user find all data
Agg_user={'State':[],'Transaction_Year':[],'Quaters':[],'Brand_Name':[],'count':[],'Percentage':[]}
for s in Agg_user_state_list:
  paths=Agg_user_path+s+"/"
  Agg_yr=os.listdir(paths)
  for y in Agg_yr:
    paths1=paths+y+'/'
    Agg_yr_l=os.listdir(paths1)
    for yl in Agg_yr_l:
      paths2=paths1+yl
      Data=open(paths2,'r')
      D=json.load(Data)
      data=D['data']['usersByDevice']
      if data is not None:
        for z in data:
           Brand=z['brand']
           Count=int(z['count'])
           Percentage=float(z['percentage'])
           Agg_user['Brand_Name'].append(Brand)
           Agg_user['count'].append(Count)
           Agg_user['Percentage'].append(Percentage)
           Agg_user['State'].append(s)
           Agg_user['Transaction_Year'].append(y)
           Agg_user['Quaters'].append(int(yl.strip('.json')))



# map_trans
map_trans_path="/content/pulse/data/map/transaction/hover/country/india/state/"
map_trans_state_list=os.listdir(map_trans_path)
(map_trans_state_list).sort()
#Map trans find all data
Map_trans={'State':[],'Transaction_Year':[],'Quaters':[],'District':[],'Transaction_Type':[],'Transaction_Count':[],'Transaction_Amount':[]}
for s in map_trans_state_list:
  paths=map_trans_path+s+"/"
  Map_yr=os.listdir(paths)
  for y in Map_yr:
    paths1=paths+y+'/'
    Map_yr_l=os.listdir(paths1)
    for yl in Map_yr_l:
      paths2=paths1+yl
      Data=open(paths2,'r')
      D=json.load(Data)
      for z in D['data']['hoverDataList']:
           District=z['name']
           Transaction_Type=z['metric'][0]['type']
           Transaction_Count=int(z['metric'][0]['count'])
           Transaction_Amount=int(z['metric'][0]['amount'])
           Map_trans['District'].append(District)
           Map_trans['Transaction_Type'].append(Transaction_Type)
           Map_trans['Transaction_Count'].append(Transaction_Count)
           Map_trans['Transaction_Amount'].append(Transaction_Amount)
           Map_trans['State'].append(s)
           Map_trans['Transaction_Year'].append(y)
           Map_trans['Quaters'].append(int(yl.strip('.json')))


# map_user
map_user_path="/content/pulse/data/map/user/hover/country/india/state/"
map_user_state_list=os.listdir(map_user_path)
(map_user_state_list).sort()
#Map user find all data
Map_user={'State':[],'Transaction_Year':[],'Quaters':[],'District':[],'RegisteredUsers':[],'appOpens':[]}
for s in map_user_state_list:
  paths=map_user_path+s+"/"
  Map_yr=os.listdir(paths)
  for y in Map_yr:
    paths1=paths+y+'/'
    Map_yr_l=os.listdir(paths1)
    for yl in Map_yr_l:
      paths2=paths1+yl
      Data=open(paths2,'r')
      D=json.load(Data)
      for district,values in D['data']['hoverData'].items():
           District=district
           RegisteredUsers=int(values['registeredUsers'])
           appOpens=values['appOpens']
           Map_user['State'].append(s)
           Map_user['Transaction_Year'].append(y)
           Map_user['Quaters'].append(int(yl.strip('.json')))
           Map_user['District'].append(District)
           Map_user['RegisteredUsers'].append(RegisteredUsers)
           Map_user['appOpens'].append(appOpens)

# API Pincode change district
def api_pin(Pincode):
  try:
      endpoint="https://api.postalpincode.in/pincode/"
      response=requests.get(endpoint+Pincode)
      pin_infor=json.loads(response.text)
      District=pin_infor[0]['PostOffice'][0]['District']
      return District
  except:
      pass


# Top_trans
Top_trans_path="/content/pulse/data/top/transaction/country/india/state/"
Top_trans_state_list=os.listdir(Top_trans_path)
(Top_trans_state_list).sort()
#Top trans find all data
Top_trans={'State':[],'Transaction_Year':[],'Quaters':[],'District':[],'Transaction_Type':[],'Transaction_Count':[],'Transaction_Amount':[]}
for s in Top_trans_state_list:
  paths=Top_trans_path+s+"/"
  Top_yr=os.listdir(paths)
  for y in Top_yr:
    paths1=paths+y+'/'
    Top_yr_l=os.listdir(paths1)
    for yl in Top_yr_l:
      paths2=paths1+yl
      Data=open(paths2,'r')
      D=json.load(Data)
      for z in D['data']['districts']:
           District=z['entityName']
           Transaction_Type=z['metric']['type']
           Transaction_Count=int(z['metric']['count'])
           Transaction_Amount=int(z['metric']['amount'])
           Top_trans['District'].append(District)
           Top_trans['Transaction_Type'].append(Transaction_Type)
           Top_trans['Transaction_Count'].append(Transaction_Count)
           Top_trans['Transaction_Amount'].append(Transaction_Amount)
           Top_trans['State'].append(s)
           Top_trans['Transaction_Year'].append(y)
           Top_trans['Quaters'].append(int(yl.strip('.json')))
      if D['data']['pincodes'] is not None:
       for x in D['data']['pincodes']:
            Pincode=x['entityName']
            District=api_pin(Pincode)
            Top_trans['District'].append(District)
            Pin_Transaction_Type=x['metric']['type']
            Pin_Transaction_Count=int(x['metric']['count']) if x['metric']['type'] is not None else  0
            Pin_Transaction_Amount=int(x['metric']['amount']) if x['metric']['type'] is not None else  0
            Top_trans['Transaction_Type'].append(Pin_Transaction_Type)
            Top_trans['Transaction_Count'].append(Pin_Transaction_Count)
            Top_trans['Transaction_Amount'].append(Pin_Transaction_Amount)
            Top_trans['State'].append(s)
            Top_trans['Transaction_Year'].append(y)
            Top_trans['Quaters'].append(int(yl.strip('.json')))


# Top_user
Top_user_path="/content/pulse/data/top/user/country/india/state/"
Top_user_state_list=os.listdir(Top_user_path)
(Top_user_state_list).sort()
#Top user find all data
Top_user={'State':[],'Transaction_Year':[],'Quaters':[],'District':[],'RegisteredUsers':[]}
for s in Top_user_state_list:
  paths=Top_user_path+s+"/"
  Top_yr=os.listdir(paths)
  for y in Top_yr:
    paths1=paths+y+'/'
    Top_yr_l=os.listdir(paths1)
    for yl in Top_yr_l:
      paths2=paths1+yl
      Data=open(paths2,'r')
      D=json.load(Data)
      for z in D['data']['districts']:
           District=z['name']
           RegisteredUsers=int(z['registeredUsers'])
           Top_user['District'].append(District)
           Top_user['RegisteredUsers'].append(RegisteredUsers)
           Top_user['State'].append(s)
           Top_user['Transaction_Year'].append(y)
           Top_user['Quaters'].append(int(yl.strip('.json')))
      if D['data']['pincodes'] is not None:
       for x in D['data']['pincodes']:
            Pincode=x['name']
            District=api_pin(Pincode)
            Top_user['District'].append(District)
            Pin_RegisteredUsers=int(x['registeredUsers'])
            Top_user['RegisteredUsers'].append(Pin_RegisteredUsers)
            Top_user['State'].append(s)
            Top_user['Transaction_Year'].append(y)
            Top_user['Quaters'].append(int(yl.strip('.json')))


#Succesfully created Dataframe
Agg_trans_DF=pd.DataFrame(Agg_trans)
Agg_user_DF=pd.DataFrame(Agg_user)
Map_trans_DF=pd.DataFrame(Map_trans)
Map_user_DF=pd.DataFrame(Map_user)
Top_trans_DF=pd.DataFrame(Top_trans)
Top_user_DF=pd.DataFrame(Top_user)

# Save csv file
Agg_trans_DF.to_csv("Agg_trans_DF.csv")
Agg_user_DF.to_csv("Agg_user_DF.csv")
Map_trans_DF.to_csv("Map_trans_DF.csv")
Map_user_DF.to_csv("Map_user_DF.csv")
Top_trans_DF.to_csv("Top_trans_DF.csv")
Top_user_DF.to_csv("Top_user_DF.csv")