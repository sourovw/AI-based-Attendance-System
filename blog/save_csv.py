import os
import pandas as pd
from flask_login import current_user
from datetime import datetime
from flask import flash


def write_attendance():
    user = current_user.username
    path = "./generated_files/" + user + '/'

    if not os.path.exists(path):
        os.makedirs(path)

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    ym = now.strftime("%Y-%m")
    fn = path + user + '-' + ym + '.csv'

    if not os.path.exists(fn):
        df = pd.DataFrame(columns=['Reg. No.', 'Date', 'Time'])
        df.to_csv(fn, index=False)
    
    df = pd.read_csv(fn)
    lst = df['Date'].tolist()

    if date in lst:
        flash('Today you have already gave your attendance.', 'warning')
        print('Today you have already gave your attendance.')
    else:
        df.loc[len(df)] = [user, date, time]
        df.to_csv(fn, index=False)
        flash('Your attendance has been updated.', 'success')
        print('Your attendance has been updated.')
