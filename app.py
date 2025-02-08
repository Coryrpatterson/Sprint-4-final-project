import streamlit as st
import pandas as pd
import plotly.express as px 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm


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

model_years = df_filtered['model_year']
xmin, xmax = model_years.min(), model_years.max()
x = np.linspace(xmin, xmax, 100)
mean = model_years.mean()
std = model_years.std()
normal_dist = norm.pdf(x, mean, std)  
fig = px.histogram(
    model_years, 
    nbins=30,  
    histnorm='density',  
    title="Distribution of Vehicle Year and Its Effect on Sales",
    labels={'value': 'Model Year', 'density': 'Density'},  
    color_discrete_sequence=['steelblue']
)

fig.add_trace(
    go.Scatter(
        x=x, 
        y=normal_dist, 
        mode='lines', 
        name='Normal Dist.',  
        line=dict(color='red', dash='dash')  
    )
)
fig.update_layout(
    xaxis_title="Model Year",
    yaxis_title="Density",
    title_x=0.5,
    legend_title="Legend",  
    showlegend=True  
)
st.plotly_chart(fig)

st.write('Here we see a scatter plot of what happens with the prices of vehicles as we get higher odometer readings. There are outliers here however, the majority of the prices steadily have a negative slope to them')

fig4=plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['odometer'], y=df['price'], alpha=0.3, s=10, color="darkblue")
sns.regplot(x=df['odometer'], y=df['price'], scatter=False, color='red', line_kws={"linewidth": 2})
plt.xlabel('Odometer Reading (miles)')
plt.ylabel('Purchase Price ($)')
plt.title('Vehicle Purchase Price vs. Odometer Reading')
max_miles = df['odometer'].max()
max_price = df['price'].max()
plt.xlim(0, 500000)
plt.ylim(0, 150000)
plt.xticks(np.arange(0, 500001, 50000), rotation=45)
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.yticks(np.arange(0, 100001, 5000))
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${int(x):,}')) 
st.pyplot(fig4)