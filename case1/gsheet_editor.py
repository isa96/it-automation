import pandas as pd

# Funstion to update the gsheet with new DataFrame
def update_gsheet(worksheet, df):
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

# Function to add new row to a DataFrame
def add_rows(df, values):
    new_rows = pd.DataFrame(values).transpose()
    new_rows = new_rows.rename(columns=dict(zip(range(df.shape[1]), df.columns)))
    
    # Concat new row to the DataFrame
    return pd.concat([df, new_rows], ignore_index=True)