import pandas as pd
import sqlite3
import os

# --- Configuration ---
DB_NAME = 'sales_data.db'
TRANSACTIONS_FILE = 'transactions.csv'
CUSTOMERS_FILE = 'customers.csv'
REPORTING_TABLE = 'sales_report'

def extract_data():
    """
    Reads data from the two simulated source CSV files.
    """
    print("1. Starting Extraction...")
    
    try:
        # Load transactions data
        df_transactions = pd.read_csv(TRANSACTIONS_FILE)
        print(f"   -> Loaded transactions: {df_transactions.shape[0]} rows")

        # Load customer data
        df_customers = pd.read_csv(CUSTOMERS_FILE)
        print(f"   -> Loaded customers: {df_customers.shape[0]} rows")
        
        return df_transactions, df_customers
    
    except FileNotFoundError as e:
        print(f"ERROR: Source file not found: {e.filename}")
        return None, None
def transform_data(df_transactions, df_customers):
    """
    Cleans, standardizes, and joins the extracted dataframes.
    """
    print("2. Starting Transformation...")

    # --- 2.1 Standardize City Names ---
    # Fix inconsistent capitalization and spelling (e.g., 'NYC' -> 'New York')
    city_mapping = {
        'NewYork': 'New York',
        'NYC': 'New York',
        'Los Angeles': 'Los Angeles',
        'LA': 'Los Angeles',
        'Chicago': 'Chicago' # Already clean
    }
    df_customers['city'] = df_customers['city'].map(city_mapping)
    print("   -> Standardized city names.")

    # --- 2.2 Calculate Final Price ---
    # Formula: Final Price = Price * (1 + Tax Rate)
    df_transactions['tax_amount'] = df_transactions['price'] * df_transactions['tax_rate']
    df_transactions['final_price'] = df_transactions['price'] + df_transactions['tax_amount']
    df_transactions = df_transactions.drop(columns=['price', 'tax_rate']) # Remove raw columns
    print("   -> Calculated final prices and tax amounts.")

    # --- 2.3 Join DataFrames ---
    # Merge transactions and customer data on the common key: user_id / customer_id
    # We use a left join to keep all transactions, even if customer data was missing (though none are missing here).
    df_reporting = pd.merge(
        df_transactions,
        df_customers,
        left_on='user_id',
        right_on='customer_id',
        how='left'
    )
    
    # Drop redundant ID columns
    df_reporting = df_reporting.drop(columns=['user_id', 'customer_id'])
    
    print(f"   -> Data merged into single reporting table: {df_reporting.shape[0]} rows.")
    
    # Select and reorder final columns for the database
    df_reporting = df_reporting[[
        'transaction_id', 'full_name', 'product_name', 'date', 
        'final_price', 'tax_amount', 'city', 'registration_date'
    ]]

    return df_reporting

def load_data(df_reporting):
    """
    Connects to the SQLite database and loads the transformed DataFrame.
    """
    print("3. Starting Loading...")
    
    conn = None
    try:
        # Connect to the SQLite database. It will create the file if it doesn't exist.
        conn = sqlite3.connect(DB_NAME)
        
        # Use pandas 'to_sql' method to load the DataFrame into the database table
        # if_exists='replace' means if the table exists, overwrite it.
        df_reporting.to_sql(REPORTING_TABLE, conn, if_exists='replace', index=False)
        
        print(f"   -> Successfully loaded {df_reporting.shape[0]} rows into '{REPORTING_TABLE}'.")
        
    except sqlite3.Error as e:
        print(f"ERROR: SQLite database error: {e}")
        
    finally:
        if conn:
            # Always close the connection
            conn.close()

    print("Loading Complete.")
def main():
    # 1. Extraction step
    df_transactions, df_customers = extract_data()

    if df_transactions is not None:
        print("\nExtraction Successful!")

        # 2. Transformation step
        df_reporting = transform_data(df_transactions, df_customers)
        print("Transformation Successful! Ready for Loading.")

        # 3. Load step (We will write this function next)
        load_data(df_reporting)
        
    else:
        print("\nPipeline failed during extraction.")

if __name__ == '__main__':
    main()