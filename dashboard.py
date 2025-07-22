import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# --- 1. Load and Prepare Data ---
file_path = r'C:\ggc\GGC_PROJECTS_old\data\project1\GGC Sales Data.xlsx'
df = pd.read_excel(file_path)

# Convert 'Billdate' to datetime objects for proper time-series analysis
df['Billdate'] = pd.to_datetime(df['Billdate'])

# --- 2. Initialize the Dash App ---
app = dash.Dash(__name__)

# --- 3. Define the App Layout ---
app.layout = html.Div([
    html.H1('GGC Sales Dashboard', style={'textAlign': 'center'}),

    # Filters
    html.Div([
        html.Div([
            html.Label('Company Name:'),
            dcc.Dropdown(
                id='company-filter',
                options=[{'label': i, 'value': i} for i in df['Company Name'].unique()],
                value=df['Company Name'].unique()[0]
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Brand:'),
            dcc.Dropdown(
                id='brand-filter',
                options=[{'label': 'All Brands', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Brand'].unique()],
                value='All'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'padding': '10px'}),

    # KPIs
    html.Div([
        html.Div(id='kpi-revenue', style={'width': '32%', 'display': 'inline-block', 'textAlign': 'center', 'border': '1px solid #eee', 'padding': '10px', 'margin': '5px'}),
        html.Div(id='kpi-qty', style={'width': '32%', 'display': 'inline-block', 'textAlign': 'center', 'border': '1px solid #eee', 'padding': '10px', 'margin': '5px'}),
        html.Div(id='kpi-customers', style={'width': '32%', 'display': 'inline-block', 'textAlign': 'center', 'border': '1px solid #eee', 'padding': '10px', 'margin': '5px'})
    ]),

    # Charts
    dcc.Graph(id='sales-over-time'),
    html.Div([
        dcc.Graph(id='top-sales-persons', style={'width': '49%', 'display': 'inline-block'}),
        dcc.Graph(id='sales-by-category', style={'width': '49%', 'display': 'inline-block', 'float': 'right'})
    ])
])

# --- 4. Define Callbacks for Interactivity ---
@app.callback(
    [
        Output('kpi-revenue', 'children'),
        Output('kpi-qty', 'children'),
        Output('kpi-customers', 'children'),
        Output('sales-over-time', 'figure'),
        Output('top-sales-persons', 'figure'),
        Output('sales-by-category', 'figure')
    ],
    [
        Input('company-filter', 'value'),
        Input('brand-filter', 'value')
    ]
)
def update_dashboard(selected_company, selected_brand):
    # Filter data based on selections
    filtered_df = df[df['Company Name'] == selected_company].copy()
    if selected_brand != 'All':
        filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]

    # 1. KPIs
    total_revenue = filtered_df['Taxpaidvalue'].sum()
    total_qty = filtered_df['Qty'].sum()
    unique_customers = filtered_df['Customer Name'].nunique()

    kpi_revenue_div = [html.H3('Total Revenue'), html.H4(f'₹{total_revenue:,.2f}')]
    kpi_qty_div = [html.H3('Total Quantity Sold'), html.H4(f'{total_qty:,}')]
    kpi_customers_div = [html.H3('Unique Customers'), html.H4(f'{unique_customers:,}')]

    # 2. Sales Over Time (Line Chart)
    sales_by_date = filtered_df.groupby(filtered_df['Billdate'].dt.to_period('M'))['Taxpaidvalue'].sum().reset_index()
    sales_by_date['Billdate'] = sales_by_date['Billdate'].dt.to_timestamp()
    fig_time = px.line(sales_by_date, x='Billdate', y='Taxpaidvalue', title='Monthly Sales Revenue')

    # 3. Top 5 Sales Persons (Bar Chart)
    top_sales_persons = filtered_df.groupby('Sales Person')['Taxpaidvalue'].sum().nlargest(5).reset_index()
    fig_sales_persons = px.bar(top_sales_persons, x='Sales Person', y='Taxpaidvalue', title='Top 5 Sales Persons by Revenue')

    # 4. Sales by Item Category (Pie Chart)
    sales_by_category = filtered_df.groupby('Item Category')['Taxpaidvalue'].sum().reset_index()
    fig_category = px.pie(sales_by_category, names='Item Category', values='Taxpaidvalue', title='Revenue by Item Category')

    return kpi_revenue_div, kpi_qty_div, kpi_customers_div, fig_time, fig_sales_persons, fig_category

# --- 5. Run the App ---
if __name__ == '__main__':
    app.run_server(debug=True)
