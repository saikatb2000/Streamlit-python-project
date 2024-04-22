#Import all pakages
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Survey Results')
st.header('Survey Result 2021')
###------LOAD DATASET
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df= pd.read_excel(excel_file,sheet_name=sheet_name,usecols='B:D',header=3)
df_partcipient = pd.read_excel(excel_file,sheet_name=sheet_name,usecols='F:G',header=3)
#----STREAMLIT SELECTION
department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()
age_selection = st.slider('Age:',min_value=min(ages),
                          max_value= max(ages),
                          value=(min(ages),max(ages)))
department_selection = st.multiselect('Department:', department, default=department)
#--- Filter database based on selection
mask = (df['Age'].between(*age_selection))& (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')
##--- Grouped Dataframe Selection
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age':'Votes'})
df_grouped = df_grouped.reset_index()

#----Plot Barchart ----
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence=['#F63366'] * len(df_grouped),
                   template='plotly_white')
st.plotly_chart(bar_chart)
col1, col2 = st.columns(2)
col1.dataframe(df[mask])
image = Image.open('undraw_cohort_analysis_stny.png')
col2.image(image, caption='Survey Result Animation', use_column_width=True)
pie_chart = px.pie(df_partcipient,title='Total No Of Participants', values='Participants',names='Departments')
df_partcipient.dropna(inplace=True)
st.plotly_chart(pie_chart)



