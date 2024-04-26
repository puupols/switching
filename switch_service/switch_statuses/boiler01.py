import datetime

def get_switch_status(weather_service, electricity_price_service):
    date = datetime.datetime.now()
    weather_data = weather_service.get_weather_data_after_date(date)
    electricity_price = electricity_price_service.get_electricity_price_data_after_date(date)
    print(electricity_price)
    if weather_data[0][3] > 3 and electricity_price[0][1] < 74:
        return 'ON'
    else:
        return 'OFF'
