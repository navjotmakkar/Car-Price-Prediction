#!/usr/bin/python
# coding=utf-8

from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *

import pickle
import numpy as np
from datetime import date

model = pickle.load(open('car_price_pred_rf.pkl', 'rb'))
app = Flask(__name__)


def predict():
    Year = input("Enter the Model Year：", type=NUMBER)
    todays_date = date.today()
    Age = todays_date.year - Year

    Kms_Driven = input("Enter the distance it has travelled(in KMS)：", type=FLOAT)

    Fuel_Type = select('What is the Fuel Type', ['Petrol', 'Diesel','CNG'])
    if (Fuel_Type == 'Diesel'):
        Fuel_Type = 1
    else:
        Fuel_Type = 0

    Seller_Type = select('Are you a dealer or an individual', ['Dealer', 'Individual'])
    if (Seller_Type == 'Individual'):
        Seller_Type = 1
    else:
        Seller_Type = 0

    Transmission = select('Transmission Type', ['Manual Car', 'Automatic Car'])
    if (Transmission == 'Manual Car'):
        Transmission = 1
    else:
        Transmission = 0

    prediction = model.predict([[Transmission, Age, Kms_Driven, Fuel_Type, Seller_Type]])
    output = round(prediction[0], 2)

    if output < 0:
        put_text("Sorry You can't sell this Car")

    else:
        put_text('You can sell this Car at price:',output)

app.add_url_rule('/tool', 'webio_view', webio_view(predict),
            methods=['GET', 'POST', 'OPTIONS'])


#if __name__ == '__main__':
    #predict()

app.run(host='localhost', port=1025)

#visit http://localhost/tool to open the PyWebIO application.