"""Implements common functions for the financial manager package."""
import csv
import json
from datetime import date
from os import path
from typing import List, Dict

import plaid

_DELIMITER = '|'
_START_DATE = '2000-01-01'
_END_DATE = str(date.today())


def store_access_token(item_id: str, access_token: str, file_name: str) -> None:
    """Appends access token and item ID to specified file."""
    is_existing_file = path.exists(file_name)
    with open(file_name, 'a') as file:
        if not is_existing_file:
            file.write(f'item_id{_DELIMITER}access_token\n')
        file.write(f'{item_id}{_DELIMITER}{access_token}\n')


def get_transactions(
        access_token: str,
        start_date: str,
        end_date: str,
        plaid_client: plaid.Client,
) -> List[Dict]:
    response = plaid_client.Transactions.get(access_token,
                                             start_date=start_date,
                                             end_date=end_date)
    transactions = response['transactions']
    while len(transactions) < response['total_transactions']:
        response = plaid_client.Transactions.get(access_token,
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 offset=len(transactions)
                                                 )
        transactions.extend(response['transactions'])
    return transactions


def _flatten_transaction_list(input_transactions: List[Dict]) -> List[Dict]:
    max_list_columns = 3
    output_transactions = []
    prev_row_keys = []
    for transaction in input_transactions:
        output_transaction = {}
        for key, val in transaction.items():
            if isinstance(val, list):
                for index in range(max_list_columns):
                    output_transaction[f'{key}_{index + 1}'] = val[index] if index < len(val) else None
            elif isinstance(val, dict):
                for inner_key, inner_val in val.items():
                    output_transaction[f'{key}_{inner_key}'] = inner_val
            else:
                output_transaction[key] = val

        # check to make sure that transaction has the same field set as the previous transaction
        if prev_row_keys and prev_row_keys != output_transaction.keys():
            raise ValueError(f'Different number of columns found in different rows')
        prev_row_keys = output_transaction.keys()
        output_transactions.append(output_transaction)
    return output_transactions


def _save_transaction_data(
        item_id: str,
        target_directory: str,
        transactions: List[Dict]) -> None:
    # create the target file names
    json_file_name = f'{target_directory}/{item_id}.json'
    csv_file_name = f'{target_directory}/{item_id}.csv'

    # store transactions in json file
    json_string = json.dumps(transactions, indent=2, sort_keys=True)
    with open(json_file_name, 'w', encoding='utf-8') as file:
        file.write(json_string)

    # store transactions in csv file by flattening them
    with open(csv_file_name, 'w', encoding='utf-8') as file:
        flattened_list = _flatten_transaction_list(transactions)
        if flattened_list:
            fieldnames = flattened_list[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in flattened_list:
                writer.writerow(item)


def store_all_transactions(
        token_file_name: str,
        target_directory: str,
        plaid_client: plaid.Client) -> None:
    with open(token_file_name, 'r') as file:
        lines = file.readlines()[1:]
        for line in lines:
            line = line.strip()
            item_id, access_token = line.split(_DELIMITER)
            transactions = get_transactions(access_token=access_token,
                                            start_date=_START_DATE,
                                            end_date=_END_DATE,
                                            plaid_client=plaid_client)
            _save_transaction_data(item_id=item_id,
                                   target_directory=target_directory,
                                   transactions=transactions)
