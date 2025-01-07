import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta  
from dateutil.relativedelta import relativedelta
import sys
import os
import json

#==========vvvvv==========>] OPTIONS [<==========vvvvv==========#

DATE_RUN = '2025.01.03'
PERSON_CODE = 'vbakjohn'
PERSON_NAME = 'John Baker'
BIRTH_DATE = '1980.02.14'
START_YEAR = '2025'
END_AGE = 120
EARLY_RETIRE_AGE = 45
RETIRE_AGE = 60

CUR_401K_BALANCE = 3000
CUR_INVEST_BALANCE = 5000

#HOURS_PER_MONTH = 156.429 # 9 hours / day, 4 days / week
HOURS_PER_MONTH = 173.81 # 10 hours / day, 4 days / week
HOUR_PAY = 25

MOBILE_HOUSE_NEED = 50000 + 11000
MOBILE_HOUSE_NEED = None
SINGLE_HOUSE_NEED = 400000
SINGLE_HOUSE_NEED = None

MONTH_EXPENSE_WORK = 1500
MONTH_EXPENSE_RETIRE = 5000
MONTH_EXPENSE_EARLY_RETIRE = 2500

RELAX_EXPENSE_WORK = 0
RELAX_EXPENSE_RETIRE = 0
RELAX_EXPENSE_EARLY_RETIRE = 0

PER_CONTRIB_WORK = 0.39
EMP_CONTRIB_WORK = 0.04
TAXES_RATE_WORK = 0.18
PENALTY_RATE_WORK = 0.1
WITHDRAW_TAX_RATE_WORK = 0.2

PER_CONTRIB_RETIRE = 0.39
EMP_CONTRIB_RETIRE = 0
TAXES_RATE_RETIRE = 0.2
PENALTY_RATE_RETIRE = 0.1
WITHDRAW_TAX_RATE_RETIRE = 0.2

PER_CONTRIB_EARLY_RETIRE = 0.39
EMP_CONTRIB_EARLY_RETIRE = 0
TAXES_RATE_EARLY_RETIRE = 0.2
PENALTY_RATE_EARLY_RETIRE = 0.1
WITHDRAW_TAX_RATE_EARLY_RETIRE = 0.2

GAIN_CALC_RATE_WORK = 0
GAIN_CALC_RATE_RETIRE = 0
GAIN_CALC_RATE_EARLY_RETIRE = 0

WITHDRAW_BEFORE_SINGLE_HOUSE_NEED = False
REINVEST_OVER_WITHDRAW = True
WITHDRAW_FOR_HOUSE_FROM_401K = True
MIN_401K_FOR_HOUSE = 1200000

#--------------------------------------------------#

NAME_STOCK_401K = 'TG3I - State Street Large Cap Growth Index Trust'
LINK_STOCK_401K = 'https://retiretxn.fidelity.com/nbretail/workplacefunds/summary/TG3I?fundnbr=TG3I'
RETURN_1Y_STOCK_401K = 0.3336
RETURN_3Y_STOCK_401K = 0.1047
RETURN_YTD_STOCK_401K = 0.3336
RETURN_LIFE_STOCK_401K = 0.1575
NAV_STOCK_401K = 17.47

#--------------------------------------------------#

NAME_STOCK_INVEST = 'FSELX - Fidelity® Select Semiconductors Portfolio'
LINK_STOCK_INVEST = 'https://fundresearch.fidelity.com/mutual-funds/summary/316390863'
RETURN_1Y_STOCK_INVEST = 0.4351
RETURN_3Y_STOCK_INVEST = 0.1834
RETURN_YTD_STOCK_INVEST = 0.4351
RETURN_LIFE_STOCK_INVEST = 0.1494
NAV_STOCK_INVEST = 33.47

#--------------------------------------------------#

JSON_FILE = None
HTML_FILE = None

if len(sys.argv) > 1:
    JSON_FILE = sys.argv[1]
    HTML_FILE = JSON_FILE.replace('.json', '.html')
    DATE_RUN = datetime.now().strftime('%Y.%m.%d') 
    START_YEAR = datetime.now().strftime('%Y')
    with open(JSON_FILE, 'r') as f:
        JSD = json.load(f)
        
        v = JSD['date_of_birth'].strip()
        if len(v) > 0:
            try:
                d1 = datetime.strptime(v, "%Y.%m.%d")
                BIRTH_DATE = v
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['run_date'].strip()
        if len(v) > 0:
            try:
                d1 = datetime.strptime(v, "%Y.%m.%d")
                DATE_RUN = v
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['planner_name'].strip()
        if len(v) > 0:
            try:
                fds = v.split(' ')
                c = 'v' + fds[-1].strip()[:3].lower() + fds[0].strip().lower()
                PERSON_NAME = v
                PERSON_CODE = c
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['starting_year'].strip()
        if len(v) > 0:
            try:
                n = int(v)
                START_YEAR = str(n)
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['age_of_early_retirement'].strip()
        if len(v) > 0:
            try:
                n = int(v)
                EARLY_RETIRE_AGE = n
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['age_of_retirement'].strip()
        if len(v) > 0:
            try:
                n = int(v)
                RETIRE_AGE = n
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['balance_401k_account'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                CUR_401K_BALANCE = n
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['balance_investment_account'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                CUR_INVEST_BALANCE = n
            except Exception as e:
                print('=> [E] ' + str(e))

        v = JSD['work_hours_per_week'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                HOURS_PER_MONTH = (n * 173.81) / 40.0
            except Exception as e:
                print('=> [E] ' + str(e))
                
        v = JSD['hourly_pay_rate'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                HOUR_PAY = n
            except Exception as e:
                print('=> [E] ' + str(e))
                
        v = JSD['monthly_expense_working'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                MONTH_EXPENSE_WORK = n
            except Exception as e:
                print('=> [E] ' + str(e))
                
        v = JSD['monthly_expense_early_retirement'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                MONTH_EXPENSE_EARLY_RETIRE = n
            except Exception as e:
                print('=> [E] ' + str(e))
                
        v = JSD['monthly_expense_retirement'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                MONTH_EXPENSE_RETIRE = n
            except Exception as e:
                print('=> [E] ' + str(e))
                
        v = JSD['401k_contribution_rate_personal'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                PER_CONTRIB_WORK = n
            except Exception as e:
                print('=> [E] ' + str(e))
                
        v = JSD['401k_contribution_rate_employer'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                EMP_CONTRIB_WORK = n
            except Exception as e:
                print('=> [E] ' + str(e))
                
        v = JSD['all_taxes_rate'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                TAXES_RATE_WORK = n
            except Exception as e:
                print('=> [E] ' + str(e))
                
        v = JSD['mobile_house_buying_amount'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                if n > 0:
                    MOBILE_HOUSE_NEED = n
            except Exception as e:
                print('=> [E] ' + str(e))
                
        v = JSD['single_house_buying_amount'].strip()
        if len(v) > 0:
            try:
                n = float(v)
                if n > 0:
                    SINGLE_HOUSE_NEED = n
            except Exception as e:
                print('=> [E] ' + str(e))
                                                                                                                                                         
        v = JSD['information_of_bought_stocks'].strip()
        if len(v) > 0:
            try:
                vjsd = json.loads(v)

                #--------------------------------------------------#

                NAME_STOCK_401K = vjsd['401k']['name']
                LINK_STOCK_401K = vjsd['401k']['link']
                RETURN_1Y_STOCK_401K = float(vjsd['401k']['return_1y'])
                RETURN_3Y_STOCK_401K = float(vjsd['401k']['return_3y'])
                RETURN_YTD_STOCK_401K = float(vjsd['401k']['return_ytd'])
                RETURN_LIFE_STOCK_401K = float(vjsd['401k']['return_life'])
                NAV_STOCK_401K = float(vjsd['401k']['nav'])

                #--------------------------------------------------#

                NAME_STOCK_INVEST = vjsd['invest']['name']
                LINK_STOCK_INVEST = vjsd['invest']['link']
                RETURN_1Y_STOCK_INVEST = float(vjsd['invest']['return_1y'])
                RETURN_3Y_STOCK_INVEST = float(vjsd['invest']['return_3y'])
                RETURN_YTD_STOCK_INVEST = float(vjsd['invest']['return_ytd'])
                RETURN_LIFE_STOCK_INVEST = float(vjsd['invest']['return_life'])
                NAV_STOCK_INVEST = float(vjsd['invest']['nav'])
                                                        
            except Exception as e:
                print('=> [E] ' + str(e))
                                                                                                                                                         


MONTHLY_GAIN_401K_WORK = RETURN_YTD_STOCK_401K / 12
MONTHLY_GAIN_INVEST_WORK = RETURN_YTD_STOCK_INVEST / 12

MONTHLY_GAIN_401K_EARLY_RETIRE = RETURN_LIFE_STOCK_401K / 12
MONTHLY_GAIN_INVEST_EARLY_RETIRE = RETURN_LIFE_STOCK_INVEST / 12

MONTHLY_GAIN_401K_RETIRE = RETURN_LIFE_STOCK_401K / 12
MONTHLY_GAIN_INVEST_RETIRE = RETURN_LIFE_STOCK_INVEST / 12
                
#==========^^^^^==========>] OPTIONS [<==========^^^^^==========#

def pad_2(n):
    s = str(n)
    if len(s) < 2:
        return '0' + s
    else:
        return s

def pad_3(n):
    s = pad_2(n)
    if len(s) < 3:
        return '0' + s
    else:
        return s

def pad_4(n):
    s = pad_3(n)
    if len(s) < 4:
        return '0' + s
    else:
        return s

def to_money(n):
    return '$' + "{:.0f}".format(n)

def to_money_2(n):
    return '$' + "{:.2f}".format(n)
    
#==========vvvvv==========>] OPTIONS PROCESSING [<==========vvvvv==========#

def get_date_by_age(age, start_date = BIRTH_DATE):
    d1 = datetime.strptime(start_date, "%Y.%m.%d")
    d2 = d1 + relativedelta(years=int(+age))
    end_date = d2.strftime('%Y.%m.%d') 
    return end_date

def get_date_by_month(months, start_date = BIRTH_DATE):
    d1 = datetime.strptime(start_date, "%Y.%m.%d")
    d2 = d1 + relativedelta(months=int(+months))
    end_date = d2.strftime('%Y.%m.%d') 
    return end_date

#--------------------------------------------------#

START_DATE = f'{START_YEAR}.01.01'
MONEY_FILE = f'/kaggle/working/money-{PERSON_CODE}-{START_YEAR}.csv'
MONEY_DF = None
END_DATE = get_date_by_age(END_AGE)
EARLY_RETIRE_DATE = get_date_by_age(EARLY_RETIRE_AGE)
RETIRE_DATE = get_date_by_age(RETIRE_AGE)

if EARLY_RETIRE_AGE >= 60:
    PENALTY_RATE_EARLY_RETIRE = 0
if RETIRE_AGE >= 60:
    PENALTY_RATE_RETIRE = 0

MONTH_PAY_WORK = HOUR_PAY * HOURS_PER_MONTH

CONTRIB_WORK = PER_CONTRIB_WORK + EMP_CONTRIB_WORK
TAKE_HOME_RATE_WORK = 1 - PER_CONTRIB_WORK - TAXES_RATE_WORK

CONTRIB_RETIRE = PER_CONTRIB_RETIRE + EMP_CONTRIB_RETIRE
TAKE_HOME_RATE_RETIRE = 1 - PER_CONTRIB_RETIRE - TAXES_RATE_RETIRE

CONTRIB_EARLY_RETIRE = PER_CONTRIB_EARLY_RETIRE + EMP_CONTRIB_EARLY_RETIRE
TAKE_HOME_RATE_EARLY_RETIRE = 1 - PER_CONTRIB_EARLY_RETIRE - TAXES_RATE_EARLY_RETIRE

WITHDRAW_RATE_WORK = 1 - PENALTY_RATE_WORK - WITHDRAW_TAX_RATE_WORK
WITHDRAW_RATE_RETIRE = 1 - PENALTY_RATE_RETIRE - WITHDRAW_TAX_RATE_RETIRE
WITHDRAW_RATE_EARLY_RETIRE = 1 - PENALTY_RATE_EARLY_RETIRE - WITHDRAW_TAX_RATE_EARLY_RETIRE

MONTH_SAVING_WORK = TAKE_HOME_RATE_WORK * MONTH_PAY_WORK - MONTH_EXPENSE_WORK - RELAX_EXPENSE_WORK

YEAR_EXPENSE_WORK = MONTH_EXPENSE_WORK * 12
YEAR_EXPENSE_RETIRE = MONTH_EXPENSE_RETIRE * 12
YEAR_EXPENSE_EARLY_RETIRE = MONTH_EXPENSE_EARLY_RETIRE * 12

TOTAL_HOUSE_NEED = 0
if MOBILE_HOUSE_NEED is not None:
    S_MOBILE_HOUSE_BUDGET = to_money(MOBILE_HOUSE_NEED)
    TOTAL_HOUSE_NEED += MOBILE_HOUSE_NEED
else:
    S_MOBILE_HOUSE_BUDGET = to_money(0)
if SINGLE_HOUSE_NEED is not None:
    S_SINGLE_HOUSE_BUDGET = to_money(SINGLE_HOUSE_NEED)
    if not WITHDRAW_BEFORE_SINGLE_HOUSE_NEED:
        TOTAL_HOUSE_NEED += SINGLE_HOUSE_NEED
else:
    S_SINGLE_HOUSE_BUDGET = to_money(0)

#--------------------------------------------------#

def build_money_1():
    global MONEY_DF
    rows = []
    date_start = START_DATE
    year_cnt = 0
    age_cnt = 0
    phase = 1
    while True:
        date_age_start = get_date_by_age(age_cnt)
        if date_age_start > date_start:
            break
        age_cnt += 1
    while True:
        date_year_start = get_date_by_age(year_cnt, date_start)
        month_cnt = 0
        while month_cnt < 12:
            date_cur = get_date_by_month(month_cnt, date_year_start)
            new_year = 0
            if month_cnt == 0:
                new_year = 1
            phase = 1
            if age_cnt < EARLY_RETIRE_AGE:
                phase = 1
            elif age_cnt < RETIRE_AGE:
                phase = 2
            else:
                phase = 3
            rw = {'date': date_cur, 'year_cnt': year_cnt, 'month_cnt': month_cnt, 'age_cnt': age_cnt, 'new_year': new_year, 'phase': phase}
            rows.append(rw)
            month_cnt += 1
        year_cnt += 1
        age_cnt += 1
        date_year_start = get_date_by_age(year_cnt, date_start)
        if date_year_start >= END_DATE:
            break
    mdf = pd.DataFrame(rows)
    mdf = mdf.sort_values(by=['date'], ascending=[True])
    mdf.to_csv(MONEY_FILE, index=False)
    MONEY_DF = mdf

def build_money_row_start(rw_all_start, rw_year_start, rw_year_start_prv, rw_processed, rw_month_prv, rw):
    phase = rw['phase']
    balance_401k_cur = 0
    balance_401k_prv = 0
    house_budget_cur = 0
    balance_invest_cur = 0
    balance_invest_prv = 0
    no_contrib = False
    no_gain = False
    if rw_month_prv is None:
        balance_401k_cur = rw_all_start['balance_401k']
        balance_invest_cur = rw_all_start['balance_invest']
        house_budget_cur = rw_all_start['house_budget']
        no_contrib = True
    else:
        balance_401k_cur = rw_month_prv['balance_401k']
        balance_invest_cur = rw_month_prv['balance_invest']
        house_budget_cur = rw_month_prv['house_budget']
    if rw_year_start_prv is None:
        balance_401k_prv = rw_all_start['balance_401k']
        balance_invest_prv = rw_all_start['balance_invest']
        no_gain = True
    else:
        balance_401k_prv = rw_year_start_prv['balance_401k']
        balance_invest_prv = rw_year_start_prv['balance_invest']
        
    if phase == 1:
        if not no_contrib or True:
            take_home_amount_401k = MONTH_PAY_WORK * TAKE_HOME_RATE_WORK
            contrib_amount_401k = MONTH_PAY_WORK * CONTRIB_WORK
            rw['contrib_401k'] = contrib_amount_401k
            rw_processed['contrib_401k'] = contrib_amount_401k
            balance_401k_cur += contrib_amount_401k

            expense_invest = MONTH_EXPENSE_WORK + RELAX_EXPENSE_WORK
            take_home_invest = TAKE_HOME_RATE_WORK * MONTH_PAY_WORK
            contrib_invest = take_home_invest - expense_invest
            if contrib_invest <= 0:
                contrib_invest = 0
            rw['contrib_invest'] = contrib_invest
            rw_processed['contrib_invest'] = contrib_invest
            balance_invest_cur += contrib_invest
            
            if no_contrib:
                rw['contrib_401k'] = 0
                balance_401k_cur -= contrib_amount_401k
                rw['contrib_invest'] = 0
                balance_invest_cur -= contrib_invest

        if not no_gain:
            more_401k = (balance_401k_cur - balance_401k_prv) * GAIN_CALC_RATE_WORK
            balance_gain_401k = balance_401k_prv + more_401k
            gain_401k = MONTHLY_GAIN_401K_WORK * balance_gain_401k
            rw['gain_401k'] = gain_401k * 12
            rw_processed['gain_401k'] = 0
            balance_401k_cur += gain_401k * 12
            rw['contrib_401k'] = rw['contrib_401k'] + gain_401k * 12   
            #rw_processed['contrib_401k'] = rw['contrib_401k']   

            more_invest = (balance_invest_cur - balance_invest_prv) * GAIN_CALC_RATE_WORK
            balance_gain_invest = balance_invest_prv + more_invest
            gain_invest = MONTHLY_GAIN_INVEST_WORK * balance_gain_invest
            rw['gain_invest'] = gain_invest * 12
            rw_processed['gain_invest'] = 0
            balance_invest_cur += gain_invest * 12
            rw['contrib_invest'] = rw['contrib_invest'] + gain_invest * 12
            #rw_processed['contrib_invest'] = rw['contrib_invest'] 
        #else:
        #    rw_processed['gain_401k'] = 0
        #    rw_processed['contrib_401k'] = 0
        #    rw_processed['withdraw_401k'] = 0
        #    rw_processed['contrib_invest'] = 0
        #    rw_processed['withdraw_remain_401k'] = 0
    elif phase == 2:
        if not no_gain:
            more_401k = (balance_401k_cur - balance_401k_prv) * GAIN_CALC_RATE_EARLY_RETIRE
            balance_gain_401k = balance_401k_prv + more_401k
            if rw['age_cnt'] <= EARLY_RETIRE_AGE:
                gain_401k = MONTHLY_GAIN_401K_WORK * balance_gain_401k
            else:
                gain_401k = MONTHLY_GAIN_401K_EARLY_RETIRE * balance_gain_401k
            rw['gain_401k'] = gain_401k * 12
            rw_processed['gain_401k'] = 0
            balance_401k_cur += gain_401k * 12
            rw['contrib_401k'] = gain_401k * 12
            rw_processed['contrib_401k'] = 0

            more_invest = (balance_invest_cur - balance_invest_prv) * GAIN_CALC_RATE_EARLY_RETIRE
            balance_gain_invest = balance_invest_prv + more_invest
            if rw['age_cnt'] <= EARLY_RETIRE_AGE:
                gain_invest = MONTHLY_GAIN_INVEST_WORK * balance_gain_invest
            else:
                gain_invest = MONTHLY_GAIN_INVEST_EARLY_RETIRE * balance_gain_invest
            rw['gain_invest'] = gain_invest * 12
            rw_processed['gain_invest'] = 0
            balance_invest_cur += gain_invest * 12
            rw['contrib_invest'] = gain_invest * 12
            rw_processed['contrib_invest'] = 0 
        #else:
        #    rw_processed['gain_401k'] = 0
        #    rw_processed['contrib_401k'] = 0
        #    rw_processed['withdraw_401k'] = 0
        #    rw_processed['withdraw_remain_401k'] = 0
        #    rw_processed['contrib_invest'] = 0
        
        if rw['gain_401k'] * WITHDRAW_RATE_EARLY_RETIRE >= MONTH_EXPENSE_WORK * 12 * 0.125:
            MONTH_EXPENSE = MONTH_EXPENSE_EARLY_RETIRE
            withdraw_cur = 0
            while True:
                if rw['gain_401k'] * (1 - WITHDRAW_RATE_EARLY_RETIRE) >= MONTH_EXPENSE_WORK * 12 * 0.125:
                    withdraw_cur = (MONTH_EXPENSE / (1 - WITHDRAW_RATE_EARLY_RETIRE)) * 12
                    if rw['gain_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                        break
                    else:
                        withdraw_cur = 0
                else:
                    withdraw_cur = 0
                if withdraw_cur == 0:
                    MONTH_EXPENSE -= MONTH_EXPENSE_WORK * 0.075
                    if MONTH_EXPENSE <= MONTH_EXPENSE_WORK * 0.075:
                        MONTH_EXPENSE = MONTH_EXPENSE_WORK * 0.075
                        withdraw_cur = (MONTH_EXPENSE / (1 - WITHDRAW_RATE_EARLY_RETIRE)) * 12
                        if rw['gain_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                            break
                        else:
                            withdraw_cur = 0
                            break
                else:
                    if rw['gain_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                        break
                    else:
                        withdraw_cur = 0
                        break

            expense_invest = MONTH_EXPENSE_EARLY_RETIRE + RELAX_EXPENSE_EARLY_RETIRE
            withdraw_cur_2 = withdraw_cur
            if withdraw_cur_2 > expense_invest * 12 * 0.125:
                contrib_invest = (withdraw_cur_2 - expense_invest * 12) / 12.0
                if contrib_invest <= 0:
                    contrib_invest = 0
                    withdraw_cur_2 = 0
                else:
                    #balance_invest_cur -= rw['contrib_invest']
                    rw['contrib_invest'] = rw['contrib_invest'] + contrib_invest * 12
                    rw_processed['contrib_invest'] = 0
                    balance_invest_cur += contrib_invest * 12
                    withdraw_cur_2 = contrib_invest * 12
            #else:
            #    rw['contrib_invest'] = 0
            #    rw_processed['contrib_invest'] = 0
                
            balance_401k_cur -= withdraw_cur
            rw['withdraw_401k'] = withdraw_cur
            rw_processed['withdraw_401k'] = 0
            rw['withdraw_remain_401k'] = (withdraw_cur - withdraw_cur_2)
            rw_processed['withdraw_remain_401k'] = 0
            rw['contrib_401k'] = rw['contrib_401k'] - withdraw_cur
            #rw_processed['contrib_401k'] = rw['contrib_401k']

        if rw['gain_invest'] * WITHDRAW_RATE_EARLY_RETIRE >= MONTH_EXPENSE_WORK:
            MONTH_EXPENSE = MONTH_EXPENSE_EARLY_RETIRE
            withdraw_cur = 0
            while True:
                if rw['gain_invest'] * (1 - WITHDRAW_RATE_EARLY_RETIRE) >= MONTH_EXPENSE_WORK * 12 * 0.125:
                    withdraw_cur = (MONTH_EXPENSE / (1 - WITHDRAW_RATE_EARLY_RETIRE)) * 12
                    if rw['gain_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                        break
                    else:
                        withdraw_cur = 0
                else:
                    withdraw_cur = 0
                if withdraw_cur <= 0:
                    MONTH_EXPENSE -= MONTH_EXPENSE_WORK * 0.075
                    if MONTH_EXPENSE <= MONTH_EXPENSE_WORK * 0.075:
                        MONTH_EXPENSE = MONTH_EXPENSE_WORK * 0.075
                        withdraw_cur = (MONTH_EXPENSE / (1 - WITHDRAW_RATE_EARLY_RETIRE)) * 12
                        if rw['gain_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                            break
                        else:
                            withdraw_cur = 0
                            break
                else:
                    if rw['gain_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                        break
                    else:
                        withdraw_cur = 0
                        break
                
            balance_invest_cur -= withdraw_cur
            rw['withdraw_invest'] = withdraw_cur
            rw_processed['withdraw_invest'] = 0
            rw['contrib_invest'] = rw['contrib_invest'] - withdraw_cur
            rw_processed['contrib_invest'] = 0
            rw['expense_invest'] = MONTH_EXPENSE
            rw_processed['expense_invest'] = MONTH_EXPENSE            

    elif phase == 3:
        if not no_gain:
            more_401k = (balance_401k_cur - balance_401k_prv) * GAIN_CALC_RATE_EARLY_RETIRE
            balance_gain_401k = balance_401k_prv + more_401k
            if rw['age_cnt'] <= RETIRE_AGE:
                gain_401k = MONTHLY_GAIN_401K_EARLY_RETIRE * balance_gain_401k
            else:
                gain_401k = MONTHLY_GAIN_401K_RETIRE * balance_gain_401k
            rw['gain_401k'] = gain_401k * 12
            rw_processed['gain_401k'] = 0
            balance_401k_cur += gain_401k * 12
            rw['contrib_401k'] = gain_401k * 12
            rw_processed['contrib_401k'] = 0

            more_invest = (balance_invest_cur - balance_invest_prv) * GAIN_CALC_RATE_EARLY_RETIRE
            balance_gain_invest = balance_invest_prv + more_invest
            if rw['age_cnt'] <= RETIRE_AGE:
                gain_invest = MONTHLY_GAIN_INVEST_EARLY_RETIRE * balance_gain_invest
            else:
                gain_invest = MONTHLY_GAIN_INVEST_RETIRE * balance_gain_invest
            rw['gain_invest'] = gain_invest * 12
            rw_processed['gain_invest'] = 0
            balance_invest_cur += gain_invest * 12
            rw['contrib_invest'] = gain_invest * 12
            rw_processed['contrib_invest'] = 0 
        #else:
        #    rw_processed['gain_401k'] = 0
        #    rw_processed['contrib_401k'] = 0
        #    rw_processed['withdraw_401k'] = 0
        #    rw_processed['withdraw_remain_401k'] = 0
        #    rw_processed['contrib_invest'] = 0
        
        if rw['gain_401k'] * WITHDRAW_RATE_RETIRE >= MONTH_EXPENSE_WORK * 12 * 0.125:
            MONTH_EXPENSE = MONTH_EXPENSE_RETIRE
            withdraw_cur = 0
            while True:
                if rw['gain_401k'] * (1 - WITHDRAW_RATE_RETIRE) >= MONTH_EXPENSE_WORK * 12 * 0.125:
                    withdraw_cur = (MONTH_EXPENSE / (1 - WITHDRAW_RATE_RETIRE)) * 12
                    if rw['gain_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                        break
                    else:
                        withdraw_cur = 0
                else:
                    withdraw_cur = 0
                if withdraw_cur == 0:
                    MONTH_EXPENSE -= MONTH_EXPENSE_WORK * 0.075
                    if MONTH_EXPENSE <= MONTH_EXPENSE_WORK * 0.075:
                        MONTH_EXPENSE = MONTH_EXPENSE_WORK * 0.075
                        withdraw_cur = (MONTH_EXPENSE / (1 - WITHDRAW_RATE_RETIRE)) * 12
                        if rw['gain_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                            break
                        else:
                            withdraw_cur = 0
                            break
                else:
                    if rw['gain_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_401k'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                        break
                    else:
                        withdraw_cur = 0
                        break

            expense_invest = MONTH_EXPENSE_RETIRE + RELAX_EXPENSE_RETIRE
            withdraw_cur_2 = withdraw_cur
            if withdraw_cur_2 > expense_invest * 12 * 0.125:
                contrib_invest = (withdraw_cur_2 - expense_invest * 12) / 12.0
                if contrib_invest <= 0:
                    contrib_invest = 0
                    withdraw_cur_2 = 0
                else:
                    #balance_invest_cur -= rw['contrib_invest']
                    rw['contrib_invest'] = rw['contrib_invest'] + contrib_invest * 12
                    rw_processed['contrib_invest'] = 0
                    balance_invest_cur += contrib_invest * 12
                    withdraw_cur_2 = contrib_invest * 12
            #else:
            #    rw['contrib_invest'] = 0
            #    rw_processed['contrib_invest'] = 0
                
            balance_401k_cur -= withdraw_cur
            rw['withdraw_401k'] = withdraw_cur
            rw_processed['withdraw_401k'] = 0
            rw['withdraw_remain_401k'] = (withdraw_cur - withdraw_cur_2)
            rw_processed['withdraw_remain_401k'] = 0
            rw['contrib_401k'] = rw['contrib_401k'] - withdraw_cur
            #rw_processed['contrib_401k'] = rw['contrib_401k']

        if rw['gain_invest'] * WITHDRAW_RATE_RETIRE >= MONTH_EXPENSE_WORK:
            MONTH_EXPENSE = MONTH_EXPENSE_RETIRE
            withdraw_cur = 0
            while True:
                if rw['gain_invest'] * (1 - WITHDRAW_RATE_RETIRE) >= MONTH_EXPENSE_WORK * 12 * 0.125:
                    withdraw_cur = (MONTH_EXPENSE / (1 - WITHDRAW_RATE_RETIRE)) * 12
                    if rw['gain_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                        break
                    else:
                        withdraw_cur = 0
                else:
                    withdraw_cur = 0
                if withdraw_cur <= 0:
                    MONTH_EXPENSE -= MONTH_EXPENSE_WORK * 0.075
                    if MONTH_EXPENSE <= MONTH_EXPENSE_WORK * 0.075:
                        MONTH_EXPENSE = MONTH_EXPENSE_WORK * 0.075
                        withdraw_cur = (MONTH_EXPENSE / (1 - WITHDRAW_RATE_RETIRE)) * 12
                        if rw['gain_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                            break
                        else:
                            withdraw_cur = 0
                            break
                else:
                    if rw['gain_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125 and rw['contrib_invest'] / 12.0 - withdraw_cur / 12.0 > MONTH_EXPENSE_WORK * 0.125:
                        break
                    else:
                        withdraw_cur = 0
                        break
                
            balance_invest_cur -= withdraw_cur
            rw['withdraw_invest'] = withdraw_cur
            rw_processed['withdraw_invest'] = 0
            rw['contrib_invest'] = rw['contrib_invest'] - withdraw_cur
            rw_processed['contrib_invest'] = 0
            rw['expense_invest'] = MONTH_EXPENSE
            rw_processed['expense_invest'] = MONTH_EXPENSE            

    #else:
    #    rw_processed['gain_401k'] = 0
    #    rw_processed['contrib_401k'] = 0
    #    rw_processed['withdraw_401k'] = 0
    #    rw_processed['contrib_invest'] = 0
    #    rw_processed['withdraw_remain_401k'] = 0

    if MOBILE_HOUSE_NEED is not None:
        tax_withdraw = 0
        if rw['phase'] == 2:
            tax_withdraw = WITHDRAW_TAX_RATE_EARLY_RETIRE
        if rw['phase'] == 3:
            tax_withdraw = WITHDRAW_TAX_RATE_RETIRE
        if rw['phase'] == 1:
            tax_withdraw = WITHDRAW_TAX_RATE_WORK
        house_need = MOBILE_HOUSE_NEED / (1 - tax_withdraw)
        if balance_invest_cur >= house_need and house_budget_cur < house_need:
            balance_invest_cur -= house_need
            house_budget_cur += house_need
    if SINGLE_HOUSE_NEED is not None and not WITHDRAW_FOR_HOUSE_FROM_401K:
        tax_withdraw = 0
        if rw['phase'] == 2:
            tax_withdraw = WITHDRAW_TAX_RATE_EARLY_RETIRE
        if rw['phase'] == 3:
            tax_withdraw = WITHDRAW_TAX_RATE_RETIRE
        if rw['phase'] == 1:
            tax_withdraw = WITHDRAW_TAX_RATE_WORK
        house_need = SINGLE_HOUSE_NEED / (1 - tax_withdraw)
        total_house_need = TOTAL_HOUSE_NEED / (1 - max(WITHDRAW_TAX_RATE_WORK, WITHDRAW_TAX_RATE_EARLY_RETIRE, WITHDRAW_TAX_RATE_RETIRE))
        if balance_invest_cur >= house_need and house_budget_cur < total_house_need:
            balance_invest_cur -= house_need
            house_budget_cur += house_need

    rw['balance_401k'] = balance_401k_cur
    rw['balance_invest'] = balance_invest_cur
    rw['house_budget'] = house_budget_cur
    rw_processed['house_budget'] = house_budget_cur
    rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']

    if REINVEST_OVER_WITHDRAW:
        if phase == 2 or phase == 3:
            tax_withdraw = 0
            if rw['phase'] == 2:
                tax_withdraw = WITHDRAW_TAX_RATE_EARLY_RETIRE
            if rw['phase'] == 3:
                tax_withdraw = WITHDRAW_TAX_RATE_RETIRE
            withdraw_max = YEAR_EXPENSE_WORK
            if phase == 2:
                withdraw_max = YEAR_EXPENSE_EARLY_RETIRE / (1 - tax_withdraw)
            if phase == 3:
                withdraw_max = YEAR_EXPENSE_RETIRE / (1 - tax_withdraw)
            if rw['withdraw_total'] > withdraw_max:
                reinvest_amount_2 = 0
                reinvest_amount = rw['withdraw_total'] - withdraw_max
                if reinvest_amount > 0 and reinvest_amount > rw['withdraw_remain_401k']:
                    reinvest_invest = reinvest_amount - rw['withdraw_remain_401k']
                    reinvest_amount -= reinvest_invest
                    rw['withdraw_remain_401k'] = 0
                    rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                    rw['contrib_401k'] = rw['contrib_401k'] + reinvest_invest
                    rw['balance_401k'] = rw['balance_401k'] + reinvest_invest
                elif reinvest_amount > 0:
                    rw['withdraw_remain_401k'] = rw['withdraw_remain_401k'] - reinvest_amount
                    rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                    rw['contrib_401k'] = rw['contrib_401k'] + reinvest_amount
                    rw['balance_401k'] = rw['balance_401k'] + reinvest_amount
                    reinvest_amount = 0
                if reinvest_amount > 0 and reinvest_amount > rw['withdraw_401k']:
                    reinvest_invest = reinvest_amount - rw['withdraw_401k']
                    reinvest_amount -= reinvest_invest
                    rw['withdraw_401k'] = 0
                    rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                    rw['contrib_401k'] = rw['contrib_401k'] + reinvest_invest
                    rw['balance_401k'] = rw['balance_401k'] + reinvest_invest
                elif reinvest_amount > 0:
                    rw['withdraw_401k'] = rw['withdraw_401k'] - reinvest_amount
                    rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                    rw['contrib_401k'] = rw['contrib_401k'] + reinvest_amount
                    rw['balance_401k'] = rw['balance_401k'] + reinvest_amount
                    reinvest_amount = 0
                if reinvest_amount > 0 and reinvest_amount > rw['withdraw_invest']:
                    reinvest_invest = reinvest_amount - rw['withdraw_invest']
                    reinvest_amount -= reinvest_invest
                    rw['withdraw_invest'] = 0
                    rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                    rw['contrib_invest'] = rw['contrib_invest'] + reinvest_invest
                    rw['balance_invest'] = rw['balance_invest'] + reinvest_invest
                elif reinvest_amount > 0:
                    rw['withdraw_invest'] = rw['withdraw_invest'] - reinvest_amount
                    rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                    rw['contrib_invest'] = rw['contrib_invest'] + reinvest_amount
                    rw['balance_invest'] = rw['balance_invest'] + reinvest_amount
                    reinvest_amount = 0

                if rw['withdraw_401k'] > 0 and rw['withdraw_remain_401k'] == 0:
                    if rw['withdraw_invest'] > withdraw_max:
                        if rw['withdraw_401k'] < rw['withdraw_invest']:
                            rw['withdraw_invest'] = rw['withdraw_invest'] - rw['withdraw_401k']
                            rw['withdraw_401k'] = 0
                            rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                        else:
                            if rw['withdraw_401k'] - rw['withdraw_invest'] < rw['contrib_invest']:
                                rw['withdraw_401k'] = rw['withdraw_401k'] - rw['withdraw_invest']
                                rw['withdraw_invest'] = 0
                                rw['contrib_invest'] = rw['contrib_invest'] - rw['withdraw_401k']
                                rw['withdraw_401k'] = 0
                                rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                            else:
                                rw['withdraw_401k'] = rw['withdraw_401k'] - rw['withdraw_invest']
                                rw['withdraw_invest'] = 0
                                rw['contrib_invest'] = 0
                                rw['withdraw_401k'] = rw['withdraw_401k'] - rw['contrib_invest']
                                rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                                if rw['withdraw_total'] == 0:
                                    rw['withdraw_total'] = -1

                if rw['withdraw_401k'] == 0 and rw['withdraw_remain_401k'] == 0:
                    rw['contrib_401k'] = rw['gain_401k']
                    if rw['gain_invest'] >= withdraw_max:
                        rw['withdraw_invest'] = withdraw_max
                        rw['contrib_invest'] = rw['gain_invest'] - withdraw_max
                        rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                    else:
                        rw['withdraw_invest'] = rw['gain_invest']
                        rw['contrib_invest'] = 0
                        rw['withdraw_total'] = rw['withdraw_remain_401k'] + rw['withdraw_invest']
                
                    if rw_month_prv is None:
                        balance_401k_cur = rw_all_start['balance_401k']
                        balance_invest_cur = rw_all_start['balance_invest']
                    else:
                        balance_401k_cur = rw_month_prv['balance_401k']
                        balance_invest_cur = rw_month_prv['balance_invest']
                    balance_401k_cur += rw['contrib_401k']
                    balance_invest_cur += rw['contrib_invest']
                    rw['balance_401k'] = balance_401k_cur
                    rw['balance_invest'] = balance_invest_cur

    if WITHDRAW_FOR_HOUSE_FROM_401K:
        if rw['age_cnt'] >= 60 and (rw['phase'] == 2 or rw['phase'] == 3):
            if SINGLE_HOUSE_NEED is not None:
                tax_withdraw = 0
                if rw['phase'] == 2:
                    tax_withdraw = WITHDRAW_TAX_RATE_EARLY_RETIRE
                if rw['phase'] == 3:
                    tax_withdraw = WITHDRAW_TAX_RATE_RETIRE
                if tax_withdraw > 0:
                    house_need = SINGLE_HOUSE_NEED / (1 - tax_withdraw)
                    if rw['balance_401k'] > MIN_401K_FOR_HOUSE + house_need:                    
                        rw['balance_401k'] = rw['balance_401k'] - house_need
                        rw['house_budget'] = rw['house_budget'] + house_need
                        rw['withdraw_401k'] = rw['withdraw_401k'] + house_need
                    
    return rw_all_start, rw_year_start, rw_year_start_prv, rw_processed, rw_month_prv, rw

def build_money_row_middle(rw_all_start, rw_year_start, rw_year_start_prv, rw_processed, rw_month_prv, rw):
    phase = rw['phase']
    balance_401k_cur = 0
    gain_401k = rw_processed['gain_401k']
    contrib_401k = rw_processed['contrib_401k']
    withdraw_401k = rw_processed['withdraw_401k']
    withdraw_remain_401k = rw_processed['withdraw_remain_401k']
    rw['gain_401k'] = gain_401k
    rw['contrib_401k'] = contrib_401k
    rw['withdraw_401k'] = withdraw_401k
    rw['withdraw_remain_401k'] = withdraw_remain_401k
    gain_invest = rw_processed['gain_invest']
    rw['gain_invest'] = gain_invest
    contrib_invest = rw_processed['contrib_invest']
    rw['contrib_invest'] = contrib_invest
    withdraw_invest = rw_processed['withdraw_invest']
    rw['withdraw_invest'] = withdraw_invest
    house_budget = rw_processed['house_budget']
    rw['house_budget'] = house_budget
    expense_invest = rw_processed['expense_invest']
    rw['expense_invest'] = expense_invest
    if rw_month_prv is None:
        balance_401k_cur = rw_all_start['balance_401k']
        balance_invest_cur = rw_all_start['balance_invest']
    else:
        balance_401k_cur = rw_month_prv['balance_401k']
        balance_invest_cur = rw_month_prv['balance_invest']

    if phase == 1:
        take_home_amount_401k = MONTH_PAY_WORK * TAKE_HOME_RATE_WORK
        contrib_amount_401k = MONTH_PAY_WORK * CONTRIB_WORK
        #rw['contrib_401k'] = contrib_amount_401k + gain_401k
        balance_401k_cur += contrib_amount_401k
        balance_invest_cur += contrib_invest
        
    if phase == 2:
        balance_401k_cur += contrib_401k
        balance_invest_cur += contrib_invest

    if phase == 3:
        balance_401k_cur += contrib_401k
        balance_invest_cur += contrib_invest

    rw['balance_401k'] = balance_401k_cur
    rw['balance_invest'] = balance_invest_cur
    
    return rw_all_start, rw_year_start, rw_year_start_prv, rw_processed, rw_month_prv, rw
    
def build_money_2():
    global MONEY_DF

    if MONEY_DF is None:
        build_money_1() 

    mdf = MONEY_DF
    rows = []
    rw_all_start = None
    rw_year_start = None
    rw_year_start_prv = None
    rw_month_prv = None
    rw_processed = {'gain_401k': 0, 'contrib_401k': 0, 'withdraw_401k': 0, 'withdraw_remain_401k': 0, 'gain_invest': 0, 'contrib_invest': 0, 'withdraw_invest': 0, 'expense_invest': 0, 'house_budget': 0}
    for ri in range(len(mdf)):
        date_cur = mdf['date'].iloc[ri]
        year_cnt = mdf['year_cnt'].iloc[ri]
        month_cnt = mdf['month_cnt'].iloc[ri]
        age_cnt = mdf['age_cnt'].iloc[ri]
        new_year = mdf['new_year'].iloc[ri]
        phase = mdf['phase'].iloc[ri]
        balance_401k = 0
        balance_invest = 0
        if ri == 0:
            balance_401k = CUR_401K_BALANCE
            balance_invest = CUR_INVEST_BALANCE
        rw = {'date': date_cur, 'year_cnt': year_cnt, 'month_cnt': month_cnt, 'age_cnt': age_cnt, 'new_year': new_year, 'phase': phase, 'balance_401k': balance_401k, 'contrib_401k': 0, 'gain_401k': 0, 'withdraw_401k': 0, 'withdraw_remain_401k': 0, 'balance_invest': balance_invest, 'contrib_invest': 0, 'gain_invest': 0, 'withdraw_invest': 0, 'expense_invest': 0, 'house_budget': 0, 'withdraw_total': 0}
        if ri == 0:
            rw_all_start = rw
        if new_year:
            rw_year_start_prv = rw_year_start
            rw_year_start = rw
            rw_all_start, rw_year_start, rw_year_start_prv, rw_processed, rw_month_prv, rw = build_money_row_start(rw_all_start, rw_year_start, rw_year_start_prv, rw_processed, rw_month_prv, rw)
        else:
            rw_all_start, rw_year_start, rw_year_start_prv, rw_processed, rw_month_prv, rw = build_money_row_middle(rw_all_start, rw_year_start, rw_year_start_prv, rw_processed, rw_month_prv, rw)
        
        rows.append(rw)
        rw_month_prv = rw
        
    mdf = pd.DataFrame(rows)
    mdf = mdf.sort_values(by=['date'], ascending=[True])
    mdf.to_csv(MONEY_FILE, index=False)
    MONEY_DF = mdf
    
#--------------------------------------------------#

build_money_2()    
#==========^^^^^==========>] OPTIONS PROCESSING [<==========^^^^^==========#

S_MONTH_PAY_WORK = to_money(MONTH_PAY_WORK)
S_MONTH_SAVING_WORK = to_money(MONTH_SAVING_WORK)
S_CUR_401K_BALANCE = to_money(CUR_401K_BALANCE)
S_CUR_INVEST_BALANCE = to_money(CUR_INVEST_BALANCE)
S_MONTHLY_GAIN_401K_WORK = "{:.2f}".format(MONTHLY_GAIN_401K_WORK * 12 * 100) + '%'
S_MONTHLY_GAIN_401K_EARLY_RETIRE = "{:.2f}".format(MONTHLY_GAIN_401K_EARLY_RETIRE * 12 * 100) + '%'
S_MONTHLY_GAIN_401K_RETIRE = "{:.2f}".format(MONTHLY_GAIN_401K_RETIRE * 12 * 100) + '%'
S_MONTHLY_GAIN_INVEST_WORK = "{:.2f}".format(MONTHLY_GAIN_INVEST_WORK * 12 * 100) + '%'
S_MONTHLY_GAIN_INVEST_EARLY_RETIRE = "{:.2f}".format(MONTHLY_GAIN_INVEST_EARLY_RETIRE * 12 * 100) + '%'
S_MONTHLY_GAIN_INVEST_RETIRE = "{:.2f}".format(MONTHLY_GAIN_INVEST_RETIRE * 12 * 100) + '%'
S_MONTH_EXPENSE_WORK = to_money(MONTH_EXPENSE_WORK)
S_MONTH_EXPENSE_EARLY_RETIRE = to_money(MONTH_EXPENSE_EARLY_RETIRE)
S_MONTH_EXPENSE_RETIRE = to_money(MONTH_EXPENSE_RETIRE)
S_YEAR_EXPENSE_WORK = to_money(YEAR_EXPENSE_WORK)
S_YEAR_EXPENSE_EARLY_RETIRE = to_money(YEAR_EXPENSE_EARLY_RETIRE)
S_YEAR_EXPENSE_RETIRE = to_money(YEAR_EXPENSE_RETIRE)
S_RELAX_EXPENSE_WORK = to_money(RELAX_EXPENSE_WORK)
S_RELAX_EXPENSE_EARLY_RETIRE = to_money(RELAX_EXPENSE_EARLY_RETIRE)
S_RELAX_EXPENSE_RETIRE = to_money(RELAX_EXPENSE_RETIRE)
S_RETURN_1Y_STOCK_401K = "{:.2f}".format(RETURN_1Y_STOCK_401K * 100) + '%'
S_RETURN_3Y_STOCK_401K = "{:.2f}".format(RETURN_3Y_STOCK_401K * 100) + '%'
S_RETURN_YTD_STOCK_401K = "{:.2f}".format(RETURN_YTD_STOCK_401K * 100) + '%'
S_RETURN_LIFE_STOCK_401K = "{:.2f}".format(RETURN_LIFE_STOCK_401K * 100) + '%'
S_NAV_STOCK_401K = to_money_2(NAV_STOCK_401K)
S_RETURN_1Y_STOCK_INVEST = "{:.2f}".format(RETURN_1Y_STOCK_INVEST * 100) + '%'
S_RETURN_3Y_STOCK_INVEST = "{:.2f}".format(RETURN_3Y_STOCK_INVEST * 100) + '%'
S_RETURN_YTD_STOCK_INVEST = "{:.2f}".format(RETURN_YTD_STOCK_INVEST * 100) + '%'
S_RETURN_LIFE_STOCK_INVEST = "{:.2f}".format(RETURN_LIFE_STOCK_INVEST * 100) + '%'
S_NAV_STOCK_INVEST = to_money_2(NAV_STOCK_INVEST)

def add_line():
    return '<tr><td colspan="2" style="background-color: gainsboro;">&nbsp;</td></tr>'
    
def add_row(name, value):
    return '<tr><td style="background-color: gainsboro;">' + name + '</td><td>' + value + '</td></tr>'

ohtml = '<table width="100%" style="max-width: 640px;"><thead><tr><th style="background-color: yellow;">Name</th><th style="background-color: yellow;">Value</th></tr></thead><tbody>'
ohtml += add_row('PERSON_CODE', f'{PERSON_CODE}')
ohtml += add_row('PERSON_NAME', f'{PERSON_NAME}')
ohtml += add_row('START_YEAR', f'{START_YEAR}')
ohtml += add_row('DATE_RUN', f'{DATE_RUN}')
ohtml += add_line()
ohtml += add_row('START_DATE', f'{START_DATE}')
ohtml += add_row('END_DATE', f'{END_DATE} ({END_AGE} years old)')
ohtml += add_row('EARLY_RETIRE_DATE', f'{EARLY_RETIRE_DATE} ({EARLY_RETIRE_AGE} years old)')
ohtml += add_row('RETIRE_DATE', f'{RETIRE_DATE} ({RETIRE_AGE} years old)')
ohtml += add_line()
ohtml += add_row('MONTH_PAY_WORK', f'{S_MONTH_PAY_WORK}')
ohtml += add_row('MONTH_SAVING_WORK', f'{S_MONTH_SAVING_WORK}')
ohtml += add_row('CUR_401K_BALANCE', f'{S_CUR_401K_BALANCE}')
ohtml += add_row('CUR_INVEST_BALANCE', f'{S_CUR_INVEST_BALANCE}')
ohtml += add_line()
ohtml += add_row('MONTH_EXPENSE_WORK', f'{S_MONTH_EXPENSE_WORK}')
ohtml += add_row('MONTH_EXPENSE_EARLY_RETIRE', f'{S_MONTH_EXPENSE_EARLY_RETIRE}')
ohtml += add_row('MONTH_EXPENSE_RETIRE', f'{S_MONTH_EXPENSE_RETIRE}')
ohtml += add_row('YEAR_EXPENSE_WORK', f'{S_YEAR_EXPENSE_WORK}')
ohtml += add_row('YEAR_EXPENSE_EARLY_RETIRE', f'{S_YEAR_EXPENSE_EARLY_RETIRE}')
ohtml += add_row('YEAR_EXPENSE_RETIRE', f'{S_YEAR_EXPENSE_RETIRE}')
ohtml += add_line()
ohtml += add_row('MONTHLY_GAIN_401K_WORK', f'{S_MONTHLY_GAIN_401K_WORK} / year')
ohtml += add_row('MONTHLY_GAIN_401K_EARLY_RETIRE', f'{S_MONTHLY_GAIN_401K_EARLY_RETIRE} / year')
ohtml += add_row('MONTHLY_GAIN_401K_RETIRE', f'{S_MONTHLY_GAIN_401K_RETIRE} / year')
ohtml += add_row('MONTHLY_GAIN_INVEST_WORK', f'{S_MONTHLY_GAIN_INVEST_WORK} / year')
ohtml += add_row('MONTHLY_GAIN_INVEST_EARLY_RETIRE', f'{S_MONTHLY_GAIN_INVEST_EARLY_RETIRE} / year')
ohtml += add_row('MONTHLY_GAIN_INVEST_RETIRE', f'{S_MONTHLY_GAIN_INVEST_RETIRE} / year')
ohtml += add_line()
ohtml += add_row('NAME_STOCK_401K', f'{NAME_STOCK_401K}')
ohtml += add_row('LINK_STOCK_401K', f'{LINK_STOCK_401K}')
ohtml += add_row('RETURN_1Y_STOCK_401K', f'{S_RETURN_1Y_STOCK_401K}')
ohtml += add_row('RETURN_3Y_STOCK_401K', f'{S_RETURN_3Y_STOCK_401K}')
ohtml += add_row('RETURN_YTD_STOCK_401K', f'{S_RETURN_YTD_STOCK_401K}')
ohtml += add_row('RETURN_LIFE_STOCK_401K', f'{S_RETURN_LIFE_STOCK_401K}')
ohtml += add_row('NAV_STOCK_401K', f'{S_NAV_STOCK_401K}')
ohtml += add_line()
ohtml += add_row('NAME_STOCK_INVEST', f'{NAME_STOCK_INVEST}')
ohtml += add_row('LINK_STOCK_INVEST', f'{LINK_STOCK_INVEST}')
ohtml += add_row('RETURN_1Y_STOCK_INVEST', f'{S_RETURN_1Y_STOCK_INVEST}')
ohtml += add_row('RETURN_3Y_STOCK_INVEST', f'{S_RETURN_3Y_STOCK_INVEST}')
ohtml += add_row('RETURN_YTD_STOCK_INVEST', f'{S_RETURN_YTD_STOCK_INVEST}')
ohtml += add_row('RETURN_LIFE_STOCK_INVEST', f'{S_RETURN_LIFE_STOCK_INVEST}')
ohtml += add_row('NAV_STOCK_INVEST', f'{S_NAV_STOCK_INVEST}')
ohtml += add_line()
ohtml += add_row('MOBILE_HOUSE_BUDGET', f'{S_MOBILE_HOUSE_BUDGET}')
ohtml += add_row('SINGLE_HOUSE_BUDGET', f'{S_SINGLE_HOUSE_BUDGET}')
ohtml += '</tbody></table>'

FINAL_HTML = '<html><head><title>' + PERSON_NAME + ' | Saving Planning Tool</title><style>a, p, div, span, table, th, td { font-family: Arial, sans-serif; font-size: 12px; } th, td { padding: 5px; }</style></head><body style="margin: 10px; padding: 0px; width: 1200px;">' + ohtml

def g_add_line():
    return '<tr><td colspan="12" style="background-color: gainsboro;">&nbsp;</td></tr>'

def g_add_notice(msg):
    return '<tr><td colspan="12" style="background-color: red; color: white">' + msg + '</td></tr>'

def g_add_sep(msg):
    return '<tr><td colspan="12" style="background-color: yellow;">' + msg + '</td></tr>'

def g_add_row(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12):
    return '<tr><td>' + v1 + '</td><td>' + v2 + '</td><td>' + v3 + '</td><td>' + v4 + '</td><td>' + v5 + '</td><td>' + v6 + '</td><td>' + v7 + '</td><td>' + v8 + '</td><td>' + v9 + '</td><td>' + v10 + '</td><td>' + v11 + '</td><td>' + v12 + '</td></tr>'

retire_notice = False
e_retire_notice = False
mobile_house_notice = False
single_house_notice = False
mdf = MONEY_DF
ohtml = '<table width="100%"><thead><tr><th style="background-color: yellow;">Date</th><th style="background-color: yellow;">Money in 401K</th><th style="background-color: yellow;">Monthly contrib of 401K</th><th style="background-color: yellow;">Monthly gain of 401K</th><th style="background-color: yellow;">Monthly withdraw of 401K</th><th style="background-color: yellow;">Monthly remain withdraw of 401K</th><th style="background-color: yellow;">Money in investment</th><th style="background-color: yellow;">Monthly contrib in investment</th><th style="background-color: yellow;">Monthly gain in investment</th><th style="background-color: yellow;">Monthly withdraw of investment</th><th style="background-color: yellow;">Total withdraw</th><th style="background-color: yellow;">Budget for house buying</th></tr></thead><tbody>'
for ri in range(len(mdf)):
    date_cur = mdf['date'].iloc[ri]
    age_cnt = mdf['age_cnt'].iloc[ri]
    year_cnt = mdf['year_cnt'].iloc[ri]
    new_year = mdf['new_year'].iloc[ri]
    phase = mdf['phase'].iloc[ri]
    
    balance_401k = mdf['balance_401k'].iloc[ri]
    gain_401k = mdf['gain_401k'].iloc[ri]
    contrib_401k = mdf['contrib_401k'].iloc[ri]
    withdraw_401k = mdf['withdraw_401k'].iloc[ri]
    withdraw_remain_401k = mdf['withdraw_remain_401k'].iloc[ri]

    balance_invest = mdf['balance_invest'].iloc[ri]
    gain_invest = mdf['gain_invest'].iloc[ri]
    contrib_invest = mdf['contrib_invest'].iloc[ri]
    withdraw_invest = mdf['withdraw_invest'].iloc[ri]

    house_budget = mdf['house_budget'].iloc[ri]

    s_balance_401k = to_money(balance_401k)
    s_balance_invest = to_money(balance_invest)

    s_gain_401k = to_money(gain_401k)
    s_gain_invest = to_money(gain_invest)

    s_contrib_401k = to_money(contrib_401k)
    s_contrib_invest = to_money(contrib_invest)

    s_withdraw_401k = to_money(withdraw_401k)
    s_withdraw_remain_401k = to_money(withdraw_remain_401k)
    s_withdraw_invest = to_money(withdraw_invest)

    s_house_budget = to_money(house_budget)

    total_withdraw = withdraw_remain_401k + withdraw_invest

    s_total_withdraw = to_money(total_withdraw)

    if new_year == 1:
        if year_cnt > 0:
            ohtml += g_add_sep(f'\n----- {year_cnt} years -----\n')

    if new_year == 1:
        if phase == 3:
            if not retire_notice:
                retire_notice = True
                ohtml += g_add_notice(f'\n=====>] Notice: Start to retire (in {year_cnt} years) [<=====\n')
        if phase == 2:
            if not e_retire_notice:
                e_retire_notice = True
                ohtml += g_add_notice(f'\n=====>] Notice: Start to retire early (in {year_cnt} years) [<=====\n')

    ohtml += g_add_row(f'{date_cur}', f'{s_balance_401k}', f'{s_contrib_401k}', f'{s_gain_401k}', f'{s_withdraw_401k}', f'{s_withdraw_remain_401k}', f'{s_balance_invest}', f'{s_contrib_invest}', f'{s_gain_invest}', f'{s_withdraw_invest}', f'{s_total_withdraw}', f'{s_house_budget}')

    if MOBILE_HOUSE_NEED is not None:
        if house_budget >= MOBILE_HOUSE_NEED / (1 - max(WITHDRAW_TAX_RATE_WORK, WITHDRAW_TAX_RATE_EARLY_RETIRE, WITHDRAW_TAX_RATE_RETIRE)) and not mobile_house_notice:
            mobile_house_notice = True
            ohtml += g_add_notice(f'\n=====>] Notice: Enough budget for mobile house (in {year_cnt} years) [<=====\n')
    if SINGLE_HOUSE_NEED is not None:
        if house_budget >= SINGLE_HOUSE_NEED / (1 - max(WITHDRAW_TAX_RATE_WORK, WITHDRAW_TAX_RATE_EARLY_RETIRE, WITHDRAW_TAX_RATE_RETIRE)) and not single_house_notice:
            single_house_notice = True
            ohtml += g_add_notice(f'\n=====>] Notice: Enough budget for single house (in {year_cnt} years) [<=====\n')

ohtml += '</tbody></table>'

FINAL_HTML += '<div style="height: 30px"></div>' + ohtml

FINAL_HTML += '</body></html>'

if HTML_FILE is not None:
    with open(HTML_FILE, 'w') as f:
        f.write(FINAL_HTML)
        


