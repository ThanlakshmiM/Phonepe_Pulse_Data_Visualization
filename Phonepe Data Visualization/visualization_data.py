#import library package
import psycopg2
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import json
import requests

# PostpreSQL connect 
cont=psycopg2.connect(host='localhost',user='postgres',password='thanalakshmi',port=5432,database='kavi') # connect to postgresql
cor=cont.cursor()


#----------------------------------------------------Date preparation for geo-visualization-------------------------------------------------------------
#streamlit app open
# CREATING OPTION MENU IN THE SET_PAGE_CONFIG
st.set_page_config(page_title= "PhonePe Pulse Data Visualization | By Thana Lakshmi",
                   page_icon= '📈',
                   layout='wide',
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This app is created by *Thana Lakshmi!*"""})

st.markdown(f'<h1 style="text-align: center;">PhonePe Pulse Data Visualization \
            and Exploration</h1>', unsafe_allow_html=True)
st.balloons()

# Creating option menu 
selected = option_menu(
    menu_title = None,
    options = ["About","Home","Top Charts","Explore Data"],
    icons =["bar-chart","house","toggles","graph-up-arrow","bar-chart-line","at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100%"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}})


#request geo state
def geo():

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data_geo = json.loads(response.content)
    geo_state = [i['properties']['ST_NM'] for i in data_geo['features']]
    geo_state.sort(reverse=False)
    return geo_state

 # dictof equate geo state and original state
def state_dict(data):
    original=data
    geo_state=geo()
    data = {}
    for i in range(0,len(original)):
      data[original[i]]=geo_state[i]
    return data

def state_list(data):
    original=data
    data_dict=state_dict(data)
    missed = set(original).symmetric_difference(set(data_dict))
    missed = list(missed)

    if len(missed) > 0:
     for i in missed:
        del data_dict[i]
    return list(data_dict.values())

# execute a SELECT statement
cor.execute("SELECT  State,sum(Transaction_count) FROM Agg_trans GROUP BY State order by State asc")
rows = cor.fetchall() 
# MENU 1 - HOME
if selected == "Home":
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        df = pd.DataFrame(rows, columns=['State','Transaction_count'])
        df['State']=state_list(data=[i for i in df['State']])
        fig = px.choropleth(
                             df,
                             geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                             featureidkey='properties.ST_NM',
                             locations='State',
                             color='Transaction_count',
                             color_continuous_scale='rainbow'
                                                               )

        fig.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig)
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, PostgreSQL, Postgresql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, and which brand has most number of users and so on. Bar charts, Pie charts,line chart and Geo map visualization are used to get some insights.")

  
    with col2:
         fig =px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM', 
                             locations="State",
                            color='Transaction_count',
                            color_continuous_scale=px.colors.diverging.RdYlGn,
                            height=700,width=500,
         title="Live Geo Visualization of India")
         st.plotly_chart(fig)
         st.video("Phonepe.mp4")
         st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    
# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type=st.radio(
        "Select Type👉",
        key="visibility",
        options=["Transactions", "Users"],
    )   
   
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )

# Top Charts - TRANSACTIONS
    if Type == "Transactions":
        col1,col2,col3 = st.columns([2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Aggregate Transaction-State]")
            cor.execute(f"select State, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where Transaction_Year = {Year} and Quaters = {Quarter} group by State order by Total desc limit 10")
            df = pd.DataFrame(cor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                                        names='State',
                                        title='Top 10',
                                        color_discrete_sequence=px.colors.sequential.Agsunset,
                                        hover_data=['Transactions_Count'],
                                        labels={'Transactions_Count':'Transactions_Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

    
        with col2:
            st.markdown("### :violet[Map Transaction-District]")
            cor.execute(f"select District , sum(Transaction_count) as Transaction_count,sum(Transaction_amount) as Total from map_trans where Transaction_Year = {Year} and Quaters = {Quarter} group by District order by Total desc limit 10")
            df = pd.DataFrame(cor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                                        names='District',
                                        title='Top 10',
                                        color_discrete_sequence=px.colors.sequential.Agsunset,
                                        hover_data=['Transactions_Count'],
                                        labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("### :violet[Top Transaction-District]")
            cor.execute(f"select District, sum(Transaction_count) as Transactions_count, sum(Transaction_amount) as Transaction_amount from Top_trans where Transaction_Year = {Year} and Quaters = {Quarter} group by District order by Transaction_amount desc limit 10")
            df = pd.DataFrame(cor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


# Top Charts - USERS
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")

        with col1:
            st.markdown("### :violet[Aggregate User-Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                cor.execute(f"select Brand_Name, sum(user_count) as user_count, avg(Percentage)*100 as Avg_Percentage from agg_user where Transaction_Year = {Year} and Quaters = {Quarter} group by Brand_Name order by user_count desc limit 10")
                df = pd.DataFrame(cor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)


        with col2:
            st.markdown("### :violet[Map User-District]")
            cor.execute(f"select District, sum(RegisteredUsers) as RegisteredUsers,sum(AppOpens) as AppOpens from Map_user where  Transaction_Year= {Year} and Quaters = {Quarter} group by District order by RegisteredUsers desc limit 10")
            df = pd.DataFrame(cor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("### :violet[Top User-District]")
            cor.execute(f"select District, sum(RegisteredUsers) as RegisteredUsers from Top_user where Transaction_Year = {Year} and Quaters = {Quarter} group by District order by RegisteredUsers desc limit 10")
            df = pd.DataFrame(cor.fetchall(), columns=['District', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col4:
            st.markdown("### :violet[Map User-State]")
            cor.execute(f"select State, sum(RegisteredUsers) as RegisteredUsers, sum(AppOpens) as AppOpens from Map_user where Transaction_Year = {Year} and Quaters = {Quarter} group by State order by RegisteredUsers desc limit 10")
            df = pd.DataFrame(cor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
      
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    st.markdown("## :green[Select Type]")
    Type=st.radio(
        "Select Type👉",
        key="visibility",
        options=["Transactions", "Users"],
    )  
    col1,col2 = st.columns(2)

# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        st.markdown('## ')
        st.markdown("## :violet[Select any Transaction Type]")
        selected_type = st.selectbox("",('Merchant payments','Peer-to-peer payments','Recharge & bill payments','Financial Services','Others'))
        st.markdown("## :violet[Select any State]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        st.markdown("## :violet[Select any Year]")
        selected_year = st.selectbox("",(2021, 2020, 2022, 2019, 2018))
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
    
         #pie chart agg_trans Quarter wise Transaction Count
        with col2:
         st.markdown('## Quarter wise Transaction Count')
         fig = px.pie(df, names="Quater",
                          values="Transaction_count",
                          title=f" {selected_type} in {selected_year} at {selected_state}",
                          hole=0.5)
         fig.update_layout(title_x=0.10, title_font_size=22)
         fig.update_traces(text=df['Transaction_amount'], textinfo='percent+value', 
                          texttemplate='%{value:.4s}<br>%{percent}' )
         st.plotly_chart(fig, theme=None, use_container_width=True)
       
        # h_bar chart
        st.markdown(f'<h1 style="text-align: center;">All Transaction Type of view Count & Amount </h1>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        cor.execute(f"SELECT DISTINCT State,Transaction_Year,Quaters,Transaction_type,Transaction_count,Transaction_amount FROM agg_trans  ORDER BY State,Quaters,Transaction_Year")
        df = pd.DataFrame(cor.fetchall(), columns=['State', 'Year',"Quater", 'Transaction_type','Transaction_count', 'Transaction_amount'])
       #bar chart Type wise Transaction Count
        with col1:
         fig=px.bar(df,y='Transaction_type',
                    x='Transaction_count', 
                    labels={'Transaction_count': '', 'Transaction_type': ''}, 
                    title='Type wise Transaction Count')
         fig.update_layout(title_x=0.35, title_font_size=22)

         text_position = ['inside' if val >= max(df['Transaction_count']) * 0.75 else 'outside' for val in df['Transaction_count']]

         fig.update_traces(marker_color='#5cb85c', 
                          text=df["Transaction_count"], 
                          textposition=text_position,
                          textfont=dict(size=14),
                          insidetextfont=dict(color='white'),
                          textangle=0,
                          hovertemplate='%{x}<br>%{y}')
         st.plotly_chart(fig, use_container_width=True)
         #bar chart Type wise Transaction Amount
        with col2:
            fig=px.bar(df,y='Transaction_type',
                    x='Transaction_amount', 
                    labels={'Transaction_amount': '', 'Transaction_type': ''}, 
                    title='Type wise Transaction Amount')
            fig.update_layout(title_x=0.35, title_font_size=22)

            text_position = ['inside' if val >= max(df['Transaction_amount']) * 0.75 else 'outside' for val in df['Transaction_amount']]

            fig.update_traces(marker_color='#5cb85c', 
                          text=df["Transaction_amount"], 
                          textposition=text_position,
                          textfont=dict(size=14),
                          insidetextfont=dict(color='white'),
                          textangle=0,
                          hovertemplate='%{x}<br>%{y}')
            st.plotly_chart(fig, use_container_width=True)
         # BAR CHART TOTAL TRANSACTION - DISTRICT WISE DATA
        st.subheader(':violet[Registered user & App installed -> State and Districtwise:]')
        st.markdown("### :green[Select any Quater:]")
        Quarter = st.slider("Quater", min_value=1, max_value=4)
        st.markdown("## :violet[Select any State & Year to explore more]")
        cor.execute(f"select State,Transaction_Year,Quaters,District,sum(Transaction_Count) as Transaction_Count, sum(Transaction_Amount) as Transaction_Amount from Map_trans where Transaction_Year = {selected_year} and Quaters = {Quarter} and State = '{selected_state}' group by State, District,Transaction_Year,Quaters order by State,District")
        df = pd.DataFrame(cor.fetchall(), columns=['State','year', 'quater', 'District', 'Total_count','Tranasaction_amount'])
        fig = px.bar(df,
                     title=f"{selected_state} in {selected_year}",
                     x="District",
                     y="Total_count",
                     orientation='v',
                     color='Tranasaction_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

        st.subheader(':violet[Top Transaction--> Statewise:]')
        st.markdown("## :violet[Select any Year to explore more]")
        cor.execute(f"select State,Transaction_Year,Quaters,Transaction_Count,Transaction_Amount from Top_trans where Transaction_Year = {selected_year}  order by State")
        df = pd.DataFrame(cor.fetchall(), columns=['State','year', 'quater', 'Total_count','Tranasaction_amount'])
        fig = px.bar(df,
                     title=f"Statewise in {selected_year} transaction ",
                     x='State',
                     y="Total_count",
                     orientation='v',
                     color='Tranasaction_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)


# EXPLORE DATA - USERS
    if Type == "Users": 
        st.markdown(f'<h1 style="text-align: center;">All Brand of Aggregate User count in india</h1>', unsafe_allow_html=True)
        col1,col2=st.columns(2)
        with col1:
         cor.execute(f"SELECT State,sum(User_count),avg(Percentage) FROM agg_user GROUP BY State ORDER BY State")
         df = pd.DataFrame(cor.fetchall(), columns=['State','total_count','percentage'])
         df['State']=state_list(data=[i for i in df['State']])
         fig = px.choropleth(
                             df,
                             geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                             featureidkey='properties.ST_NM',
                             locations='State',
                             color='total_count',
                             color_continuous_scale='agsunset',
                             width=600
                         )
         fig.update_layout(
            title={
            'text' :"State wise Brand user count in india",
            'x':0.5,
            'xanchor': 'center'
            },title_font_size=22)

         fig.update_geos(fitbounds="locations", visible=False)

         st.plotly_chart(fig)
        with col2:
            cor.execute(f"SELECT State,Transaction_Year,Quaters,Brand_Name,User_count,Percentage FROM agg_user ORDER BY State,Quaters,Brand_Name")
            df = pd.DataFrame(cor.fetchall(), columns=['State', 'Year',"Quater",'Brand', 'total_count','percentage'])
            fig = px.line(df, x="Quater", y='total_count', color='Brand', 
                      labels={"Quarter": '', 'total_count': ''}, title="Brand wise User Count")

            fig.update_layout(
            title={
            'text' :"Brand wise User Count",
            'x':0.5,
            'xanchor': 'center'
            },title_font_size=22)

            fig.update_traces(mode='lines+markers',
                        marker=dict(symbol='diamond', size=5),
                        hovertemplate='%{x}<br>%{y}')

            st.plotly_chart(fig, use_container_width=True)

        # user select the any one brand,state,year explore the bar chat
        st.markdown("## :violet[Select any brand to explore more]")
        selected_brand = st.selectbox("",('Xiaomi', 'Vivo', 'Samsung', 'Oppo', 'Realme', 'Tecno', 'Apple',
       'OnePlus', 'Motorola', 'Huawei', 'Others', 'Micromax', 'Lenovo',
       'Infinix', 'HMD Global', 'Lava', 'Gionee', 'Lyf', 'Asus',
       'COOLPAD'))
        st.markdown("## :violet[Select any State]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        st.markdown("## :violet[Select any Year]")
        selected_year = st.selectbox("",(2021, 2020, 2022, 2019, 2018))
        cor.execute(f"SELECT State,Transaction_Year,Quaters,Brand_Name,User_count,Percentage FROM agg_user WHERE State = '{selected_state}' AND Brand_Name = '{selected_brand}' And Transaction_Year = '{selected_year}' ORDER BY State,Quaters,Brand_Name")
        df = pd.DataFrame(cor.fetchall(), columns=['State', 'Year',"Quater",'Brand', 'total_count','percentage'])
        fig = px.bar(df, x="Quater",
                          y="total_count",
                          title=f" {selected_brand} in {selected_year} at {selected_state}",
                          color="percentage")
        st.plotly_chart(fig, theme=None, use_container_width=True)

        # BAR CHART TOTAL USERS - DISTRICT WISE DATA
        st.markdown("## :violet[Select any State to explore more]")
        Quarter = st.slider("Quater", min_value=1, max_value=4)
        cor.execute(f"select State,Transaction_Year,QuaterS,District,sum(RegisteredUsers) as RegisteredUsers , sum(AppOpens) as AppOpens from Map_user where Transaction_Year = {selected_year} and Quaters = {Quarter} and State = '{selected_state}' group by State, District,Transaction_Year,Quaters order by State,District")
        df = pd.DataFrame(cor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        fig = px.bar(df,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(
            title={
            'text' :f"{selected_state} in {selected_year}",
            'x':0.5,
            'xanchor': 'center'
            },title_font_size=22)
        st.plotly_chart(fig,use_container_width=True)

        # App Opens count State wise
        st.markdown("## :red[ App Opens Count ]")
        cor.execute(f"SELECT State,Transaction_Year,sum(appOpens) FROM map_user group by State,Transaction_Year ORDER BY State asc ")
        df = pd.DataFrame(cor.fetchall(), columns=['State', 'Year',"appOpens"])
        fig = px.bar(df,
                     title=f"Statewise in App Opens Count ",
                     x='State',
                     y="appOpens",
                     orientation='v',
                     color='Year',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
     
        # Top RegisteredUsers Count
        cor.execute("SELECT  State,sum(RegisteredUsers) FROM Top_user GROUP BY State order by State asc")
        rows = cor.fetchall() 
        df = pd.DataFrame(rows, columns=['State','Register_user_count'])
        df['State']=state_list(data=[i for i in df['State']])
        fig =px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM', 
                             locations="State",
                            color='Register_user_count',
                            color_continuous_scale=px.colors.diverging.RdYlGn,
                            height=700,width=1200)
        fig.update_layout(
            title={
            'text' :"Top Register User of the Count Live Geo Visualization of India",
            'x':0.5,
            'xanchor': 'center'
            },title_font_size=22)
        st.plotly_chart(fig)


# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")

        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")

        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
    with col2:
        st.image("phonepeimg.png")
        st.video("phonepesample.mp4")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

