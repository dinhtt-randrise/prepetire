import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta  
from dateutil.relativedelta import relativedelta
import sys
import os
import json

JSON_FILE = None
CSV_FILE = None
JSD = None
STORAGE_DIR = None
CONTRIB_DATE = None
PAYER_NAME = None
CONTRIB_AMOUNT = None

if len(sys.argv) > 1:
    JSON_FILE = sys.argv[1]
    with open(JSON_FILE, 'r') as f:
        JSD = json.load(f)
        
        v = JSD['storage_dir'].strip()
        if len(v) > 0:
            try:
                STORAGE_DIR = v
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['contrib_date'].strip()
        if len(v) > 0:
            try:
                d1 = datetime.strptime(v, "%Y.%m.%d")
                CONTRIB_DATE = v
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['payer_name'].strip()
        if len(v) > 0:
            try:
                PAYER_NAME = v
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['contrib_amount'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                CONTRIB_AMOUNT = n
            except Exception as e:
                print('=> [E] ' + str(e))

                                                                                                                                                         
if STORAGE_DIR is not None and CONTRIB_DATE is not None and PAYER_NAME is not None and CONTRIB_AMOUNT is not None:
    CSV_FILE = f'{STORAGE_DIR}/401k_contrib_paycheck.csv'
    ddf = None
    balance_payer = 0
    balance_total = 0
    no = 0
    if os.path.exists(CSV_FILE):
    	ddf = pd.read_csv(CSV_FILE)
    	ddf = ddf.sort_values(by=['no'], ascending=[True])
    	no = len(ddf)
    	balance_total = ddf['balance_total'].iloc[len(ddf) - 1]
    	df = ddf[ddf['payer_code'] == PAYER_NAME]
    	if len(df) > 0:
    	    balance_payer = df['balance_payer'].iloc[len(df) - 1]
    balance_total += CONTRIB_AMOUNT
    balance_payer += CONTRIB_AMOUNT   
    rw = {'no': no + 1, 'contrib_date': CONTRIB_DATE, 'payer_code': PAYER_NAME, 'contrib_amount': CONTRIB_AMOUNT, 'balance_payer': balance_payer, 'balance_total': balance_total}
    df = pd.DataFrame([rw])
    if ddf is None:
        ddf = df
    else:
        ddf = pd.concat([ddf, df])
    ddf = ddf.sort_values(by=['no'], ascending=[True])
    ddf.to_csv(CSV_FILE, index=False)
    
