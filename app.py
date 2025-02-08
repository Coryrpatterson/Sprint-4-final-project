import streamlit as st
import pandas as pd
import plotly.express as px 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go


st.title('Buying and Selling Strategies for Cars')

st.write('Now that we are looking to add inventory to your dealership, I have created an easy to use tool that will allow not only management to look and see what cars are currently being sold, but also to see what cars are being sold at what prices. This will allow us to make better decisions. We will be able to train the salesmen and any other individual that we deem to be able to review, analyze, and make decisions based on the data that is presented. This will allow us to make better decisions about what cars to bring in and to be able to make more money in the long run.')
st.write('Below I have created a tool that will make this process much easier for you and your team! I have complied all the vehicles in the data for cars being sold around the US. This will give you the upper hand when negotiating prices whether that be with a customer to buy their car or in selling them a car. Go a head and move the slider and watch the information on the chart change to your desired results!')
df=pd.read_csv('vehicles_us.csv')
for col in df.select_dtypes(include=['object', 'float']).columns:
    df[col].fillna(df[col].mode()[0], inplace=True)
df['is_4wd'] = df['is_4wd'].fillna(0)
df['is_4wd'] = df['is_4wd'].astype(int)
df['paint_color'] = df['paint_color'].fillna('unknown')
df['cylinders'] = df['cylinders'].fillna(0) 
df['cylinders'] = df['cylinders'].astype(int)
df['odometer'] = df['odometer'].fillna(0)  
df['odometer'] = df['odometer'].astype(int)
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

st.write('As shown below it isnt always the latest and greatest car that sales first! Make sure that you know your market before buying or selling  a car from a customer')

model_year_data = df['model_year'].dropna()
xmin, xmax = model_year_data.min(), model_year_data.max()
x = np.linspace(xmin, xmax, 100)
mean = model_year_data.mean()
std = model_year_data.std()
kde_values = norm.pdf(x, mean, std)
fig = go.Figure()
fig.add_trace(go.Histogram(
    x=model_year_data,
    nbinsx=30,
    histnorm='density',  
    name='Histogram of Model Year',
    marker_color='steelblue',
    opacity=0.7
))
fig.add_trace(go.Scatter(
    x=x, y=kde_values,
    mode='lines',
    name="Normal Dist.",
    line=dict(color='red', dash='dash')
))
fig.update_layout(
    title="Distribution of Vehicle Year and Its Effect on Sales",
    xaxis_title="Model Year",
    yaxis_title="Total Vehicle Sales (Density)",
    showlegend=True,
    template="plotly_white"
)
st.plotly_chart(fig)

st.write('Here we see a scatter plot of what happens with the prices of vehicles as we get higher odometer readings. There are outliers here however, the majority of the prices steadily have a negative slope to them. Feel free to click on any of the types of vehicles to remove them from the list and gain greater insight into what a particular vehicle will sell for!')


fig1 = px.scatter(
    df, x='odometer', y='price',
    title="Vehicle Purchase Price vs. Odometer Reading",
    labels={"odometer": "Odometer Reading (miles)", "price": "Purchase Price ($)"},
    color='type',  
    opacity=0.7
)
fig1.update_layout(
    xaxis=dict(
        range=[0, 500000],  
        tickmode='array',
        tickvals=np.arange(0, 500000 + 1, 50000),  
        title="Odometer Reading (miles)"
    ),
    yaxis=dict(
        range=[0, 150000],  
        tickmode='array',
        tickvals=np.arange(0, 150000 + 1, 15000), 
        title="Purchase Price ($)"
    ),
    template="plotly_white"
)

st.plotly_chart(fig1)

