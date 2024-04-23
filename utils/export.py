import pandas as pd
from datetime import datetime


def append_to_excel(path, f2, f3, f4, f5, f6, profit):
    # Create a DataFrame with the provided data
    data = {
        'DateTime': [datetime.now().strftime('%Y/%m/%d %H:%M:%S')],
        'F2': [float(f2)],
        'F3': [float(f3)],
        'F4': [float(f4)],
        'F5': [float(f5)],
        'F6': [float(f6)],
        'Profit': [float(profit)]
    }

    new_record = pd.DataFrame(data)

    try:
        # Try to read the existing Excel file
        existing_data = pd.read_excel(path)

        # Concatenate the new record to the existing data
        updated_data = pd.concat([existing_data, new_record], ignore_index=True)

        # Write the updated data back to the Excel file
        updated_data.to_excel(path, index=False)

    except FileNotFoundError:
        # If the file doesn't exist, create a new one with the new record
        new_record.to_excel(path, index=False)