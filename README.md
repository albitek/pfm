# Modified Quickstart for plaid-python

## Overview
This repo is my effort to build a personal finance management tool using the 
development environment from the Plaid API. Rather than building my own client/server, 
I forked and modified Plaid's quickstart repo which significantly reduced the technical
scope of this project and allowed me to focus on the financial model. This repo's focus 
is solely about retrieving transactions which can then be further analyzed via Excel.

I have modified the python code for the forked plaid quickstart repo
in the following ways:

* Created an `fm` (financial manager) module for custom implementations.

* Modified `server.py` to intercept the access_token request/response and store those credentials.

* Modified `server.py` to require an additional CLI parameter - the filepath where 
access tokens are stored.

* Created a new entry-point file `transactions.py` which takes the tokens file as input
and retrieves and processes all transactions for each access token (institution) in two different files
in a specified target directory:

    * raw json data file
    * flattened csv data file

---
Note: the following are excerpts from the forked readme modified to fit the new requirements.

## Installing the quickstart app
``` bash
git clone https://github.com/albitek/quickstart.git
cd quickstart/python

# If you use virtualenv
# virtualenv venv
# source venv/bin/activate

pip install -r requirements.txt
```

## Running Plaid's Link widget locally
For each institution (up to 5 allowed in development), boot up the app, follow
the auth flow, and kill the process using CTRL-C. Repeat for each institution. The quickstart server code can only store one access token in memory but tokens will
be appended to the specified `<token-filename>` during each run.
``` bash
PLAID_CLIENT_ID='CLIENT_ID' \
PLAID_SECRET='SECRET' \
PLAID_PUBLIC_KEY='PUBLIC_KEY' \
PLAID_ENV='sandbox' \
PLAID_PRODUCTS='transactions' \
PLAID_COUNTRY_CODES='US,CA,GB,FR,ES' \
python server.py <token-filename>

# Go to http://localhost:5000
```

## Fetch and store transactions
After all access tokens are stored in the `<token-filename>` path, run the
following script to pull and store all transactions in json, and csv within
the `<target-directory>` path.

``` bash
PLAID_CLIENT_ID='CLIENT_ID' \
PLAID_SECRET='SECRET' \
PLAID_PUBLIC_KEY='PUBLIC_KEY' \
PLAID_ENV='sandbox' \
python transactions.py <token-filename> <target-directory>
```

After confirming correct functionality in `sandbox` mode, then you can
switch to `development` mode by using Plaid's dashboard to generate credentials
for that environment.