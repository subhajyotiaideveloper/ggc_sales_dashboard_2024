import pandas as pd

# Path to your Excel file
file_path = r'C:\ggc\GGC_PROJECTS_old\data\project1\GGC Sales Data.xlsx'

try:
    # Read the data from the Excel file
    df = pd.read_excel(file_path)

    # Print the first 5 rows of the dataframe
    print('--- First 5 Rows ---')
    print(df.head())

    # Print the column names
    print('\n--- Column Names ---')
    print(df.columns.tolist())

    # Print a summary of the dataframe, including data types and non-null values
    print('\n--- Data Summary ---')
    df.info()

except FileNotFoundError:
    print(f"Error: The file was not found at '{file_path}'. Please check the file path and try again.")
except Exception as e:
    print(f'An error occurred: {e}')
