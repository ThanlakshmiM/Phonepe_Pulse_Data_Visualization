# Phonepe_Pulse_Data_Visualization
Github Cloning, Python, Pandas, PostgreSQL, Postgresql-connector-python, Streamlit, and Plotly
### Github Cloning
#### Importing required libraries
#### Import Data Handling libraries
```python
import pandas as pd
import numpy as np
```
#### Import Dashboard libraries
```python
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
```
#### Import Clone libraries
```python
import requests
import json
```
#### if the module shows any error or module not found it can be overcome by using below command
```python
pip install<module name>
```
```python
#aggregated transaction path
path="/content/pulse/data/aggregated/transaction/country/india/state/"
aggr_state_list=os.listdir(path)
```
## E T L Process

### a) Extract data

* Initially, we Clone the data from the Phonepe GitHub repository by using Python libraries.
#### In order to get the data clone the github 
- Inorder to clone the github data into to working environment use below command
```python
!git clone https://github.com/PhonePe/pulse
```
### b) Process and Transform the data
#### Fetch data & Creating csv file 
- after cloning the data from github the dat in the form of json file
- In order to convert json file into data frame we use below code to another 2 folders
```python
#aggregation-->transation---->state--->years--->json data to fetch
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

```
```python
#create CSV file
#df to Csv
aggr_trans.to_csv('aggregated_transaction.csv',index=False)
```
### c) Load  data 
* #### Create Table and Insert into Postgresql
- After creating dataframe insert the dataframe into sql  inner server by using postgresql
- To Establish the connection with sql server
- below table to reference another tables 
```python
#postgresql connect
import psycopg2
cont=psycopg2.connect(host='localhost',user='postgres',password='basith',port=5432,database='basith')
csr=cont.cursor()
```
```python
#create tables
cor.execute("""CREATE TABLE if not exists Agg_trans(State varchar(100),
            Transaction_Year int,
            Quaters int,
            Transaction_type varchar(100),
            Transaction_count int,
            Transaction_amount float
            )""")
cont.commit()
```

## E D A Process and Frame work

### a) Access PostSQL DB 

* Create a connection to the postgreSQL server and access the specified postgreSQL DataBase by using **psycopg2** library
  
```python
#insert df to sql
#table aggregated transaction
def Agg_trans_csv():
  query1="""INSERT INTO Agg_trans VALUES(%s,%s,%s,%s,%s,%s)"""
  with open('Agg_trans_DF.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row
    for row in reader:
        cor.execute(query1,tuple([row[1],row[2],row[3],row[4],row[5],row[6]]))
cont.commit()
```
### b) Filter the data
```
* Filter and process the collected data depending on the given requirements by using SQL queries
#### Creating Sql Querys and Plot the data to visualization
- Create sql queries to fetch the data as per the user requirement
- plot the data to visualization in streamlit dashboard
```python
SELECT * FROM "Table"
WHERE "Condition"
GROUP BY "Columns"
ORDER BY "Data"
```
### Streamlit, and plotly
I have created a dashboard to Phonepe pulse Data visualize Github repository data(https://github.com/ThanlakshmiM/Phonepe_Pulse_Data_Visualization) using Streamlit and Plotly in Python
### The main components of dashboard are
* 1.Top 10 states & district chart
         Transaction Analysis
         User Analysis
* 2.Explore the Data Geo Visualization
         Transaction Analysis
         User Analysis

1.Top 10 states & district chart
  1.Transaction Analysis
   *Select any Year,Quarter options
     1 State-wise Transaction count 
         *Top 10 State based on Total number of transaction and Total amount spent on phonepe.
               The above pie chart shows the percentage of PhonePe Transactions according to the states of India, 
               Here we can observe the top states with the highest percentage Transaction by looking at chart

     2 District-wise Transaction count 
        *Top 10 District based on Total number of transaction and Total amount spent on phonepe.
               The above pie chart shows the percentage of PhonePe Transactions according to the district of India, 
               Here we can observe the top district with the highest percentage Transaction by looking at chart
     
     3 District-wise Transaction count 
        *Top 10 District and its percentage based on the how many people transaction use phonepe
           We can observe the District with total transactions in particular mode in the selected Year & Quarter

  2.User Analysis
   *Select any Year,Quarter options
     1 Brand wise User count 
        *Top 10 mobile brands and its Average of percentage based on the how many people use phonepe.
               The above bar shows the percentage increasing order of PhonePe user according to the brand of India, 
               Here we can observe the top brand with the highest percentage user by looking at graph

     2 District wise app user count
       *Top 10 District based on Total phonepe users and their app opening count.
          The above bar shows the percentage increasing order of PhonePe user according to the District of India, 
          Here we can observe the top District with the highest percentage user by looking at graph

     3 Top User District wise count
       *Top 10 District based on Total phonepe users and their app opening frequency.
          The above pie chart shows the PhonePe user count according to the District of India, 
          Here we can observe the top user District with the highest percentage user by looking at chart

     4 State wise app user count
       *Top 10 District based on Total phonepe users and their app opening count.
          The above pie chart shows the percentage of PhonePe user according to the District of India, 
          Here we can observe the top District with the highest percentage user by looking at graph

2.Explore the Data Geo Visualization
  1.Transaction Analysis
   * Select any Transaction Type,State,Year options
      * Quarter wise Transaction Amount(pie chart)
      * Quarter wise Transaction Count(pie chart)
   * All Transaction Type of view Count & Amount
   * Registered user & App installed -> State and Districtwise:
        * select any quarter option
        * The above bar shows the increasing order of PhonePe Transaction according to the District of India, 
          Here we can observe the top District with the highest Transaction by looking at graph
    * Top Transaction--> Statewise:
         * Select any Year
         * Explore the State wise of show in increasing PhonePe Transaction according to the state of India
          Here we can observe the top state with the highest Transaction by looking at graph
  2. Users Analysis
      * All Brand of Aggregate User count in india
           * Brand wise user count in using Geo map Visualization in India
           * the above the line chart using PhonePe Brand wise user count
      * Select any brand,State,Year to explore more
           * Explore the Quarter wise user count in percentage user.
      * Select any State,Quarter to explore more
           * Explore the District wise Total user count in India
      * The bar chart of State wise App open count in india
      * Top Register user count in Geo Visualization in india


#### To Ploting code model
-using plotly express
```python
cor.execute(f"SELECT DISTINCT State,Transaction_Year,Quaters,Transaction_type,Transaction_count,Transaction_amount FROM agg_trans WHERE State = '{selected_state}' AND Transaction_type = '{selected_type}' And Transaction_Year = '{selected_year}' ORDER BY State,Quaters,Transaction_Year")
        df = pd.DataFrame(cor.fetchall(), columns=['State', 'Year',"Quater", 'Transaction_type','Transaction_count', 'Transaction_amount'])
        col1,col2=st.columns(2)
        #pie chart agg_trans Quarter wise Transaction Amount
        with col1:
         st.markdown('## Quarter wise Transaction Amount')
         fig = px.pie(df, names="Quater",
                          values="Transaction_amount",
                          hole=0.5, 
                          title=f" {selected_type} in {selected_year} at {selected_state}")
         fig.update_layout(title_x=0.10, title_font_size=22)

         fig.update_traces(text=df['Transaction_amount'], textinfo='percent+value', 
                          texttemplate='%{value:.4s}<br>%{percent}' )

         st.plotly_chart(fig, theme=None, use_container_width=True)
````

- create the streamlit app with basic tabs [Reference](https://docs.streamlit.io/library/api-reference)
- visualizing the data with plotly and streamlit
- streamlit run <filename.py> to run terminal
#### I hope this project helps you to the understand more about phonepe data
    
     

        


        







     



