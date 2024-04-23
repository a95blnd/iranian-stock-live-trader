import pandas as pd
from datetime import datetime


def append_to_excel_summin(
        *,
        path,
        zspa1220,
        zspa1221,
        zspa1222,
        zkhpars1216,
        zkhpars1200,
        zkhpars1201,
        zhrm1223,
        zhrm1224,
        zhrm1225,
        ztavan1201,
        ztavan1203,
        ztavan1205,
        symbol,
        result,
        signal_zspa1220,
        signal_zspa1221,
        signal_zspa1222,
        signal_zkhpars1216,
        signal_zkhpars1200,
        signal_zkhpars1201,
        signal_zhrm1223,
        signal_zhrm1224,
        signal_zhrm1225,
        signal_ztavan1201,
        signal_ztavan1203,
        signal_ztavan1205,
):
    # Create a DataFrame with the provided data
    data = {
        'DateTime': [datetime.now().strftime('%Y/%m/%d %H:%M:%S')],
        'zspa1220': [float(zspa1220)],
        'zspa1221': [float(zspa1221)],
        'zspa1222': [float(zspa1222)],
        'zkhpars1216': [float(zkhpars1216)],
        'zkhpars1200': [float(zkhpars1200)],
        'zkhpars1201': [float(zkhpars1201)],
        'zhrm1223': [float(zhrm1223)],
        'zhrm1224': [float(zhrm1224)],
        'zhrm1225': [float(zhrm1225)],
        'ztavan1201': [float(ztavan1201)],
        'ztavan1203': [float(ztavan1203)],
        'ztavan1205': [float(ztavan1205)],
        '': [''],
        'symbol': [str(symbol)],
        'result': [float(result)],
        '': [''],
        '': [''],
        '': [''],
        'signal_zspa1220': [str(signal_zspa1220)],
        'signal_zspa1221': [str(signal_zspa1221)],
        'signal_zspa1222': [str(signal_zspa1222)],
        'signal_zkhpars1216': [str(signal_zkhpars1216)],
        'signal_zkhpars1200': [str(signal_zkhpars1200)],
        'signal_zkhpars1201': [str(signal_zkhpars1201)],
        'signal_zhrm1223': [str(signal_zhrm1223)],
        'signal_zhrm1224': [str(signal_zhrm1224)],
        'signal_zhrm1225': [str(signal_zhrm1225)],
        'signal_ztavan1201': [str(signal_ztavan1201)],
        'signal_ztavan1203': [str(signal_ztavan1203)],
        'signal_ztavan1205': [str(signal_ztavan1205)],
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