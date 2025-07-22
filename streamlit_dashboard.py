import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Load and Prepare Data ---
@st.cache_data
def load_data():
    file_path = r'C:\ggc\GGC_PROJECTS_old\data\project1\GGC Sales Data.xlsx'
    df = pd.read_excel(file_path)
    df['Billdate'] = pd.to_datetime(df['Billdate'])
    return df

df = load_data()

# --- 2. Page Configuration ---
st.set_page_config(layout="wide")
st.title('GGC Sales Dashboard ')

# --- 3. Sidebar Filters ---
st.sidebar.header('Filters')
selected_company = st.sidebar.selectbox(
    'Company Name',
    df['Company Name'].unique()
)

brand_options = ['All'] + list(df['Brand'].unique())
selected_brand = st.sidebar.selectbox(
    'Brand',
    brand_options
)

# Filter data based on selections
filtered_df = df[df['Company Name'] == selected_company].copy()
if selected_brand != 'All':
    filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]

# --- 4. Display KPIs ---
st.header('Key Performance Indicators')
total_revenue = filtered_df['Taxpaidvalue'].sum()
total_qty = filtered_df['Qty'].sum()
unique_customers = filtered_df['Customer Name'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Total Quantity Sold", f"{total_qty:,}")
col3.metric("Unique Customers", f"{unique_customers:,}")

# --- 5. Display Charts ---
st.header('Visualizations')

# Sales Over Time (Line Chart)
sales_by_date = filtered_df.groupby(filtered_df['Billdate'].dt.to_period('M'))['Taxpaidvalue'].sum().reset_index()
sales_by_date['Billdate'] = sales_by_date['Billdate'].dt.to_timestamp()
fig_time = px.line(sales_by_date, x='Billdate', y='Taxpaidvalue', title='Monthly Sales Revenue')
st.plotly_chart(fig_time, use_container_width=True)

# Top Performers (side-by-side)
col1, col2 = st.columns(2)

with col1:
    # Top 5 Sales Persons (Bar Chart)
    top_sales_persons = filtered_df.groupby('Sales Person')['Taxpaidvalue'].sum().nlargest(5).reset_index()
    fig_sales_persons = px.bar(top_sales_persons, x='Sales Person', y='Taxpaidvalue', title='Top 5 Sales Persons by Revenue')
    st.plotly_chart(fig_sales_persons, use_container_width=True)

with col2:
    # Top 5 Customers (Bar Chart)
    top_customers = filtered_df.groupby('Customer Name')['Taxpaidvalue'].sum().nlargest(5).reset_index()
    fig_customers = px.bar(top_customers, x='Customer Name', y='Taxpaidvalue', title='Top 5 Customers by Revenue')
    st.plotly_chart(fig_customers, use_container_width=True)

# Sales by Item Category (Pie Chart)
sales_by_category = filtered_df.groupby('Item Category')['Taxpaidvalue'].sum().reset_index()
fig_category = px.pie(sales_by_category, names='Item Category', values='Taxpaidvalue', title='Revenue by Item Category')
st.plotly_chart(fig_category, use_container_width=True)

# --- 6. Display Raw Data ---
st.header('Detailed Sales Data')
st.dataframe(filtered_df)
