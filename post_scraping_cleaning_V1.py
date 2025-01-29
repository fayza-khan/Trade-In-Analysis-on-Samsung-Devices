import re
import pandas as pd

def extract_numerical_price(price):
    """
    Utility function to extract numerical price
    Parameter: price (str) - input price string
    Output: numeric_price (int) - extracted numerical price
    """
    match = re.search(r'\d+(?:,\d+)*', price)
    # \d - matches all the digits
    # (?:, - matches commas
    if match:
        numeric_price = int(match.group().replace(',','')) # remove any comma (example - 1,202)
        return numeric_price
    else:
        return price
        
def extract_condition_from_description(condition):
    """
    Utility function to extract condition 
    Parameter: condition (str) - input condition description
    Output: condition (str) - extracted condition
    """
    if "Flawless" in condition:
        return "Flawless"
    if "Average" in condition:
        return "Average"
    if "Broken" in condition:
        return "Broken"

def create_condition_columns(df):
    """
    Utility function to create separate columns for each condition
    Parameter: df (DataFrame) - input dataframe
    Output: df_final (DataFrame) - transformed dataframe with condition columns
    """
    flawless_df = df[df['Condition'] == 'Flawless'].reset_index(drop=True)
    flawless_df.rename({"Price (in AED)": "Flawless"}, axis=1, inplace=True)
    flawless_df.drop(columns=['Condition'], inplace=True)


    broken_df = df[df['Condition'] == 'Broken'].reset_index(drop=True)
    broken_df.rename({"Price (in AED)": "Broken"}, axis=1, inplace=True)
    broken_df.drop(columns=['Condition'], inplace=True)

    average_df = df[df['Condition'] == 'Average'].reset_index(drop=True)
    average_df.rename({"Price (in AED)": "Average"}, axis=1, inplace=True)
    average_df.drop(columns=['Condition'], inplace=True)

    # Merge flawless_df and broken_df on multiple columns
    merged_df = pd.merge(
        flawless_df,
        broken_df,
        on=['Date', 'Brand', 'Series nm', 'Series', 'Model', 'Storage'],
        how='outer'
    )

    # Merge the resulting DataFrame with average_df
    final_df = pd.merge(
        merged_df,
        average_df,
        on=['Date', 'Brand', 'Series nm', 'Series', 'Model', 'Storage'],
        how='outer'
    )

    # Fill NaN with 0 if needed (for prices)
    final_df.fillna(0, inplace=True)

    return final_df


def main_cleaning(df_name):
    """
    Main function to clean the raw scraped df
    Parameter: df_name (str) - name of the input Excel file
    """
    df = pd.read_excel(df_name)
    df.reset_index(drop=True, inplace=True)
    try:
        print(f"Column names before cleaning: {df.columns}")
        # Step 1: numerical transformation for price column
        df["Price (in AED)"] = df["Price (in AED)"].apply(lambda s: extract_numerical_price(s))
        # Step 2: extract the relevant condition
        df["Condition"] = df["Condition"].apply(lambda s: extract_condition_from_description(s))
        df = create_condition_columns(df)
        print(f"Column names after cleaning: {df.columns}")
        df.to_excel(f"Clean_{df_name}", engine='openpyxl', index=False)
    except Exception as e:
        print(f"Issue cleaning the raw scraped file: {e}")

df_name = "Scraped_Phone_Details_27-01-2025.xlsx" # replace it with the raw file
df = main_cleaning(df_name)