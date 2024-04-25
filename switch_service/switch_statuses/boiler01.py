import datetime

def get_switch_status(weather_service, electricity_price_service):
    date = datetime.datetime.now()
    weather_data = weather_service.get_weather_data_after_date(date)
    print(weather_data)
    if weather_data[0][3] > 3:
        return 'ON'
    else:
        return 'OFF'
