import pandas as pd
import datetime as dt
import itertools


def dateToDateNum(month, day):
    return (dt.datetime(2021, month, day) - dt.datetime(2020, 12, 31)).days


def prep_data():
    df = pd.read_excel('holidays2021.xlsx')
    df.dropna(how='all', inplace=True)
    birthdays = [
        ['Dad', dt.datetime(2021, 2, 24)],
        ['Mom', dt.date(2021, 5, 18)],
        ['Becky', dt.date(2021, 8, 31)],
        ['Joe', dt.date(2021, 10, 31)],
        ['Mike', dt.date(2021, 9, 12)],
        ['Jeff', dt.date(2021, 12, 17)],
        ['Angie', dt.date(2021, 6, 6)],
        ['Missy', dt.date(2021, 3, 20)],
        ['Jaye', dt.date(2021, 6, 2)]
    ]
    temp_df = pd.DataFrame(birthdays, columns=['name', 'date'])
    temp_df['name'] = temp_df['name'].apply(lambda x: x + "'s Birthday")
    df = pd.concat([df, temp_df], axis=0).reset_index()
    df['dayNum'] = (df['date'] - dt.datetime(2020, 12, 31)).dt.days
    df = df.loc[~df['name'].str.contains('Day off'), :]

    a = df[['dayNum', 'name']].to_numpy()
    dayNum_list = a[:, 0]
    # holidayName_list = a[:, 1]
    holiday_dict = dict(a)

    combos = list(itertools.combinations(dayNum_list, r=4))
    results_df = pd.DataFrame(combos, columns=list('abcd'))
    results_series = (results_df['a'] + results_df['b'] - results_df['c'] - results_df['d'])
    results_df['result'] = results_series
    results_df = results_df.loc[(results_df['result'] > 0) & (results_df['result'] < 366), :]
    
    return results_df, holiday_dict


def getGreeting(df, holiday_dict, dayNum):
    '''
    1. Randomly choose from the 'result' column based on DayNum.
    2. Then randomly shuffle the order of the response.
    
    '''
    import random as r
    filtered_df = df.loc[df['result']==dayNum, :].reset_index()
    # Choose randomly which result to use
    rand_n = r.randint(0, len(filtered_df))
    result_list = filtered_df.loc[rand_n, ['a','b','c','d']].to_list()
    holiday_list = [holiday_dict[x] for x in result_list]
    operators_list = ['+', '+', '-', '-']
    res = list(zip(operators_list, holiday_list))
    
    # Randomize the order
    r.shuffle(res)
    # Ensure that the first holiday is not a "subtraction"
    if res[0][0]=='-' and res[1][0]=='-':
        res[:] = res[::-1]
    elif res[0][0]=='-' and res[1][0]=='+':
        res[0:2] = res[1::-1]
    
    return f"Happy {res[0][1]} {res[1][0]} {res[1][1]} {res[2][0]} {res[2][1]} {res[3][0]} {res[3][1]}!"


def holidayMath(month, day, results_df, holiday_dict):
    dayNum = dateToDateNum(month, day)
    greeting = getGreeting(
        df=results_df, 
        holiday_dict=holiday_dict, 
        dayNum=dayNum
    )
    return greeting


# results_df, holiday_dict = prep_data()
# print(holidayMath(5, 5, results_df, holiday_dict))