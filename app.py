from flask import Flask, render_template, request
import os
import pandas as pd
import datetime as dt
import itertools
import pickle
from holiday_math import *

# Importing previous calculations
results_df = pd.read_csv('holidayMath_results_df.csv')
with open('pickled_holiday_dict.pkl', 'rb') as pickle_file:
    holiday_dict = pickle.load(pickle_file)

month_lookup_dict = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12     
}

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def calculate():
    greeting = ''
    month_input = ''
    day_input = ''
    if request.method == 'POST' and 'month' in request.form and 'day' in request.form:
        month_input = request.form.get('month')
        month = month_lookup_dict[month_input]
        day_input = request.form.get('day')

        if day_input == '':
            day = 0
        else:
            day = int(day_input)

        if day < 1 or day > 31:
            greeting = 'Happy !.... uh, double-check your day.'
        else:
            try:
                greeting = holidayMath(month, day, results_df, holiday_dict)
            except:
                greeting = "That day doesn't exist in 2021."

    return render_template('index.html', greeting=greeting, month_input=month_input, day_input=day_input)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)