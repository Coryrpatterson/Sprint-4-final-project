import streamlit as st
import pandas as pd
import plotly.express as px 
import seaborn as sns

st.title('Buying and Selling Strategies for Cars')

st.write('Now that we are looking to add inventory to your dealership, I have created an easy to use tool that will allow not only management to look and see what cars are currently being sold, but also to see what cars are being sold at what prices. This will allow us to make better decisions. We will be able to train the salesmen and any other individual that we deem to be able to review, analyze, and make decisions based on the data that is presented. This will allow us to make better decisions about what cars to bring in and to be able to make more money in the long run.')
st.write('Below I have created a tool that will make this process much easier for you and your team! I have complied all the vehicles in the data for cars being sold around the US. This will give you the upper hand when negotiating prices whether that be with a customer to buy their car or in selling them a car. Go a head and move the slider and watch the information on the chart change to your desired results!')
df=pd.read_csv('vehicles_us.csv')
min_year, max_year = int(df['model_year'].min()),int(df['model_year'].max())
year_range = st.slider("Choose years",value=(min_year, max_year), min_value=min_year,max_value= max_year )

actual_range = list(range(year_range[0],year_range[1]+1))
df_filtered = df[df.model_year.isin(list(actual_range))]
df_filtered

st.write('Below once can see the distribution of the prices of the vehicles in the dataset. what this will allow you to do is see the average prices of the vehicle looking to be bought or sold. This should be able to help you increase your bottom line by seeing not just your area  but also the average prices from around the country! This data below will change as you move the slider above to match the criteria you are looking for!')

fig2 = px.strip(df_filtered, x='condition', y='price', 
                color='condition', 
                color_discrete_sequence=px.colors.sequential.Viridis,
                title='Vehicle Price by Condition')
fig2.update_layout(
    xaxis_title='Condition',
    yaxis_title='Price ($)',
    title_x=0.5,  
    xaxis_tickangle=-45,  
)
st.plotly_chart(fig2)