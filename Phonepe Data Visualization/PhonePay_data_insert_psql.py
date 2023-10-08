import psycopg2
import pandas as pd
import csv

# PostpreSQL connect 
cont=psycopg2.connect(host='localhost',user='postgres',password='thanalakshmi',port=5432,database='kavi') # connect to postgresql
cor=cont.cursor()

#Table create
cor.execute("""CREATE TABLE if not exists Agg_trans(State varchar(100),
            Transaction_Year int,
            Quaters int,
            Transaction_type varchar(100),
            Transaction_count int,
            Transaction_amount float
            )""")
cont.commit()

cor.execute("""CREATE TABLE if not exists Agg_user(State varchar(100),
            Transaction_Year int,
            Quaters int,
            Brand_Name varchar(100),
            User_count int,
            Percentage float
            )""")
cont.commit()

cor.execute("""CREATE TABLE if not exists Map_trans(State varchar(100),
            Transaction_Year int,
            Quaters int,
            District varchar(100),
            Transaction_count int,
            Transaction_amount float
            )""")
cont.commit()

cor.execute("""CREATE TABLE if not exists Map_user(State varchar(100),
            Transaction_Year int,
            Quaters int,
            District varchar(100),
            RegisteredUsers int,
            AppOpens int
            )""")
cont.commit()

cor.execute("""CREATE TABLE if not exists Top_trans(State varchar(100),
            Transaction_Year int,
            Quaters int,
            District varchar(100),
            Transaction_count int,
            Transaction_amount float
            )""")
cont.commit()

cor.execute("""CREATE TABLE if not exists Top_user(State varchar(100),
            Transaction_Year int,
            Quaters int,
            District varchar(100),
            RegisteredUsers int
            )""")
cont.commit()




#fun using Agg_trans csv file upload to postgresql
def Agg_trans_csv():
  query1="""INSERT INTO Agg_trans VALUES(%s,%s,%s,%s,%s,%s)"""
  with open('Agg_trans_DF.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row
    for row in reader:
        cor.execute(query1,tuple([row[1],row[2],row[3],row[4],row[5],row[6]]))

# fun calling
#Agg_trans_csv()

   
#fun using Agg_user csv file upload to postgresql
def Agg_user_csv():
  query2="""INSERT INTO Agg_user VALUES(%s,%s,%s,%s,%s,%s)"""
  with open('Agg_user_DF.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row
    for row in reader:
       cor.execute(query2,tuple([row[1],row[2],row[3],row[4],row[5],row[6]]))
    
# fun calling
#Agg_user_csv()

#fun using Map_trans csv file upload to postgresql
def Map_trans_csv():
  query3="""INSERT INTO Map_trans VALUES(%s,%s,%s,%s,%s,%s)"""
  with open('Map_trans_DF.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row
    for row in reader:
       cor.execute(query3,tuple([row[1],row[2],row[3],row[4],row[6],row[7]]))
    
# fun calling
#Map_trans_csv()

#fun using Map_user csv file upload to postgresql
def Map_user_csv():
  query4="""INSERT INTO Map_user VALUES(%s,%s,%s,%s,%s,%s)"""
  with open('Map_user_DF.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row
    for row in reader:
       cor.execute(query4,tuple([row[1],row[2],row[3],row[4],row[5],row[6]]))
    
# fun calling
#Map_user_csv()

#fun using Top_trans csv file upload to postgresql
def Top_trans_csv():
  query3="""INSERT INTO Top_trans VALUES(%s,%s,%s,%s,%s,%s)"""
  with open('Top_trans_DF.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row
    for row in reader:
       cor.execute(query3,tuple([row[1],row[2],row[3],row[4],row[6],row[7]]))
    
# fun calling
#Top_trans_csv()

#fun using Top_user csv file upload to postgresql
def Top_user_csv():
  query4="""INSERT INTO Top_user VALUES(%s,%s,%s,%s,%s)"""
  with open('Top_user_DF.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row
    for row in reader:
       cor.execute(query4,tuple([row[1],row[2],row[3],row[4],row[5]]))
    
# fun calling
#Top_user_csv()
cont.commit()

#----------------------------------------------------------------------------------------------------#


