def get_switch_status():
    date = datetime.datetime.now()
    weather_data = get_weather_data_after_date(date)
    electricity_price = get_electricity_price_data_after_date(date)
    print(weather_data[0].temperature)
    print(electricity_price[0].price)
    if weather_data[0].temperature > 3 and electricity_price[0].price < 74:
        return 'ON'
    else:
        return 'OFF'
