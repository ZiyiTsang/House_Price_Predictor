from flask import Flask
from flask import render_template
from flask import request
from autogluon.tabular import TabularPredictor
import pandas as pd

app = Flask(__name__)
predictor = TabularPredictor.load('ModelSave/', require_py_version_match=False)
data = pd.read_csv(
    'listing_preProcessing.csv')
data = data.drop(columns=['price', 'Unnamed: 0'])


@app.route("/", methods=['GET'])
def intro():
    return render_template('input.html')


@app.route("/result", methods=['POST'])
def result():
    price_ = predict(request.form)
    price_ = str(price_)[0:5]
    # print(request.form)
    # print(predictPrice([8, 3], ['latitude', 'bedrooms']))
    return render_template('result.html', price=price_)


def predict(form):
    value = []
    columns = []
    model = ''
    for item in form:
        # print(item)
        if item == 'model':
            model = form[item]
            continue
        if item == 'neighborhood' or item =="bed_type" or item =="room_type":
            select_name = form[item]
            if select_name== 'auto':
                continue
            columns.append(select_name)
            value.append(1)
            continue
        columns.append(item)
        number = form[item]
        try:
            number = float(number)
        except:
            number = number
        finally:
            value.append(number)
    print(value)
    print(columns)
    return predictPrice(value, columns, model_=model)


def predictPrice(value, columnsName, model_='auto'):

    global data
    data = data[0:0]
    df = pd.DataFrame([value],
                      columns=columnsName)
    df.loc[0:1, 'host_since'] = 1
    new_data = pd.concat([df, data])
    if model_ == 'auto':
        price = predictor.predict(new_data)
    else:
        price = predictor.predict(new_data, model=model_)
    return float(price[0])
