import os
import sys
import plaid

from fm import store_all_transactions

# Runtime configuration: see server.py
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python transactions.py <token-filename> <target-directory>')
        sys.exit(-1)

    token_file_name = sys.argv[1]
    target_directory = sys.argv[2]

    # construct a plaid client instance
    plaid_client = plaid.Client(client_id=PLAID_CLIENT_ID,
                                secret=PLAID_SECRET,
                                public_key=PLAID_PUBLIC_KEY,
                                environment=PLAID_ENV,
                                api_version='2019-05-29')

    # pull and store all transactions for each access token
    store_all_transactions(token_file_name=token_file_name,
                           target_directory=target_directory,
                           plaid_client=plaid_client)
