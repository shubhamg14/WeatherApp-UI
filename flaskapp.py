import csv
import datetime
from random import randint
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

class Weather:
    def __init__(self, date, tmax, tmin):
        self.DATE = date
        self.TMAX = tmax
        self.TMIN = tmin

    def serialize(self):
        return {
            "DATE": self.DATE,
            "TMAX": self.TMAX,
            "TMIN": self.TMIN
        }

def read_weather_data():
    result = []
    with open('dailyweather.csv', 'r') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            weather_info = Weather(row[0], row[1], row[2])
            result.append(weather_info)

    return result

weather_info_list = read_weather_data()




@app.route('/')
def hello_world():
    return render_template('home.html')




@app.route('/about')
def about():
    return render_template('about.html')




@app.route('/add')
def add():
    return render_template('add.html')




@app.route('/delete')
def delete():
    return render_template('delete.html')




@app.route('/forecast')
def forecast():
    return render_template('forecast.html')


@app.route('/openweatherui')
def openweatherui():
    return render_template('openweather.html')




@app.route('/weatherinfo')
@app.route('/weatherinfo/')
def weatherinfo():
    eqtls = [e.serialize() for e in weather_info_list]
    return jsonify(eqtls)






@app.route('/historical')
@app.route('/historical/')
def get_historical_dates():
    result = []
    for weather_info in weather_info_list:
        result.append({"DATE": weather_info.DATE})

    return jsonify(result)






@app.route('/historical', methods=['POST'])
@app.route('/historical/', methods=['POST'])
def save_historical_info():
    DATE = request.json['DATE']
    TMAX = request.json['TMAX']
    TMIN = request.json['TMIN']

    weather_info = Weather(DATE, TMAX, TMIN)

    for i in range(len(weather_info_list)):
        if DATE == weather_info_list[i].DATE:
            del weather_info_list[i]
            break

    weather_info_list.append(weather_info)

    return jsonify({"DATE": DATE}), 201





@app.route('/historical/<string:date>/', methods=['DELETE'])
@app.route('/historical/<string:date>', methods=['DELETE'])
def delete_historical_data(date):
    for i in range(0, len(weather_info_list)):
        weather_info = weather_info_list[i]

        if weather_info.DATE == date:
            del weather_info_list[i]
            return jsonify("Value successfully deleted"), 204

    return jsonify("Value not found"), 404





@app.route('/historical/<string:date>')
@app.route('/historical/<string:date>/')
def historical_data_for_data(date):
    for weather_info in weather_info_list:
        if weather_info.DATE == date:
            return jsonify(weather_info.serialize())

    return jsonify(text="No result found."), 404





@app.route('/forecast/<string:date>')
@app.route('/forecast/<string:date>/')
def forecast_data_for_data(date):
    index_of_date = -1

    forecast_list = []

    date_time_obj = datetime.datetime.strptime(date, '%Y%m%d')

    for i in range(len(weather_info_list)):
        if str(date) == str(weather_info_list[i].DATE):
            index_of_date = i
            break

    if -1 < index_of_date < len(weather_info_list)-7:

        forecast_list = weather_info_list[index_of_date:index_of_date+7]
        eqtls = [e.serialize() for e in forecast_list]
        return jsonify(eqtls)

    else:
        for i in range(365):
            length_of_list = len(weather_info_list)
            sublist = weather_info_list[length_of_list-365:length_of_list]
            avg_max_temperature = 0.0
            avg_min_temperature = 0.0
            for item in sublist:
                avg_max_temperature += float(item.TMAX)
                avg_min_temperature += float(item.TMIN)

            avg_max_temperature /= 365
            avg_min_temperature /= 365

            forecast_date = (date_time_obj + datetime.timedelta(days=i)).strftime("%Y%m%d")

            forecast = Weather(forecast_date, avg_max_temperature - randint(0, 7), avg_min_temperature - randint(0, 7))

            weather_info_list.append(forecast)

            forecast_list.append(forecast)

        eqtls = [e.serialize() for e in forecast_list]
        return jsonify(eqtls[0:7])





#Adding third party API call
@app.route('/openweather')
@app.route('/openweather/')
def openweather():
    open_weather_forecast = []
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip=45220&appid=61f13efb9bdd28d13e8d1bea8f429ee3')
    json_object = r.json()
    for item in json_object['list']:
        if item["dt_txt"][11:19] == '00:00:00':
            open_date = item["dt_txt"][0:10].replace('-', '')
            open_temp_max = (float(item['main']['temp_max']) - 273.15) * 1.8 + 32
            open_temp_min = (float(item['main']['temp_min']) - 273.15) * 1.8 + 32
            open_weather_forecast.append({"DATE": str(open_date), "TMAX": str("{0:.2f}".format(open_temp_max)), "TMIN": str("{0:.2f}".format(open_temp_min))})
    return jsonify(open_weather_forecast)


if __name__ == '__main__':
    app.run()


