# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# import requests
# import json
# import pandas as pd
#
#
# def get_figi_data(api_key, composite_id):
#     url = 'https://api.openfigi.com/v3/mapping'
#     headers = {'Content-Type': 'text/json'}
#     payload = json.dumps([{"idType": "ID_BB_GLOBAL", "idValue": composite_id}])
#     params = {'apiKey': api_key}
#     response = requests.post(url, headers=headers, params=params, data=payload)
#
#     if response.status_code == 200:
#         json_response = response.json()
#         if json_response:
#             result = json_response[0]['data'][0]
#             id_exch_symbol = result.get('exchCode', '')
#             id_full_exchange_symbol = result.get('micCode', '')
#             return id_exch_symbol, id_full_exchange_symbol
#     else:
#         print('Error: ' + str(response.status_code))
#         return None, None
#
#
# def main():
#     # get user input for API key
#     api_key = input('Please enter your OpenFIGI API key: ')
#     # read funds.txt into pandas dataframe
#     funds_df = pd.read_csv('funds.txt', header=None, names=['composite_id'])
#     # apply get_figi_data function to each row in funds_df
#     funds_df[['id_exch_symbol', 'id_full_exchange_symbol']] = funds_df['composite_id'].apply(lambda x: pd.Series(get_figi_data(api_key, x)))
#     # export results to IDs.xlsx
#     funds_df.to_excel('IDs.xlsx', index=False)
#
#
# if __name__ == '__main__':
#     main()
#
import requests
import json
import pandas as pd
import math


def get_figi_data(api_key, composite_id):
    url = 'https://api.openfigi.com/v3/mapping'
    headers = {'Content-Type': 'text/json'}
    payload = json.dumps([{"idType": "ID_BB_GLOBAL", "idValue": composite_id}])
    params = {'apiKey': api_key}

    # Retry mechanism with exponential backoff
    for i in range(5):
        response = requests.post(url, headers=headers, params=params, data=payload)

        if response.status_code == 200:
            json_response = response.json()
            if json_response:
                result = json_response[0]['data'][0]
                id_exch_symbol = result.get('exchCode', '')
                id_full_exchange_symbol = result.get('micCode', '')
                return id_exch_symbol, id_full_exchange_symbol
            else:
                # No response data
                return None, None
        elif response.status_code == 429:
            # Rate limit exceeded, wait and retry
            wait_time = math.pow(2, i)
            print(f'Retrying after {wait_time} seconds...')
            time.sleep(wait_time)
        else:
            # Other error
            print('Error: ' + str(response.status_code))
            return None, None

    # Reached maximum number of retries
    print('Max retries exceeded')
    return None, None


def main():
    # get user input for API key
    api_key = input('Please enter your OpenFIGI API key: ')
    # read funds.txt into pandas dataframe
    funds_df = pd.read_csv('funds.txt', header=None, names=['composite_id'])
    # apply get_figi_data function to each row in funds_df
    funds_df[['id_exch_symbol', 'id_full_exchange_symbol']] = funds_df['composite_id'].apply(
        lambda x: pd.Series(get_figi_data(api_key, x)))
    # export results to IDs.xlsx
    funds_df.to_excel('IDs.xlsx', index=False)


if __name__ == '__main__':
    main()
