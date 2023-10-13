import pandas as pd
import streamlit as st
import plotly_express as px
from datetime import datetime
st.set_page_config(page_title="Sales Dashboard",
                   layout="wide",
                   )

df = pd.read_csv('EDA_practice/supermarket.csv')
df.rename(columns={"Customer type": "Customer_type"}, inplace=True)
df.rename(columns={"Product line": "Product_line"}, inplace=True)
#Feature engineering and extracting informtion from date and time columns
df['hour']= pd.to_datetime(df['Time'], format="%H:%M").dt.hour
df['day']= pd.to_datetime(df['Date']).dt.day
day_name_mapping = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

df['DayName'] = df['day'].map(day_name_mapping)

# ---SideBar--- 
st.sidebar.header('Please Filter here')
city = st.sidebar.multiselect(
    "Select the city:",
    options=df['City'].unique(),
    default=df['City'].unique()
)

gender = st.sidebar.multiselect(
    "Select the gender:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

branch = st.sidebar.multiselect(
    "Select the branch:",
    options=df['Branch'].unique(),
    default=df['Branch'].unique()
)

cxtype = st.sidebar.multiselect(
    "Select the customer type:",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

product = st.sidebar.multiselect(
    "Select the product category:",
    options=df['Product_line'].unique(),
    default=df['Product_line'].unique()
)

payment = st.sidebar.multiselect(
    "Select the payment method:",
    options=df['Payment'].unique(),
    default=df['Payment'].unique()
)


#query the data filtering
df_selection = df.query(
    "City == @city & Payment == @payment & Gender == @gender & Product_line == @product & Customer_type == @cxtype & Branch==@branch"
)


#---Main Page---
st.title(":bar_chart: Sale Dashboard")
st.markdown('##')

#---Top KPI's---
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Avearge rating")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average sale / transaction")
    st.subheader(f"US $ {average_sale_by_transaction:,}")
    
    
st.markdown("---")



#BarChart

#Sales by product line
sales_by_product_line= (
    df_selection.groupby(by=["Product_line"]).sum()[['Total']].sort_values(by='Total')
)

fig_product_sales = px.bar(
    sales_by_product_line, 
    x='Total', 
    y=sales_by_product_line.index,
    template='plotly_white'
    )



#Sales by product line
sales_by_product_line= (
    df_selection.groupby(by=["Product_line"]).sum()[['Total']].sort_values(by='Total')
)


#Sales by hour 
sales_by_hour= (
    df_selection.groupby(by=['hour']).sum()[['Total']].sort_values(by='Total')
)


#defining the bar chart
fig_hour_sales = px.bar(
    sales_by_hour, 
    x=sales_by_hour.index, 
    y='Total',
    template='plotly_white'
    )
left_column_bar, right_column_bar = st.columns(2)

left_column_bar.plotly_chart(fig_hour_sales,use_container_width=True)
right_column_bar.plotly_chart(fig_product_sales, use_container_width=True)

st.markdown("---")


left_column_line, right_column_line = st.columns(2)

#defining line chart data
sales_by_day= (
    df_selection.groupby(by=['day']).sum()[['Total']].sort_values(by='Total')
)


#defining the line chart
sales_by_day = px.bar(
    sales_by_day, 
    x=sales_by_day.index, 
    y='Total',
    template='plotly_white'
    )
left_column_line.plotly_chart(sales_by_day,use_container_width=True)



st.markdown("---")
st.dataframe(df_selection)

