"""
    Acessa o banco de dados e a API para, por finalidade
    entregar os dados necessários no formato adequado
"""

import json
from app import DB, models, api, date_util

Forecast = models.Forecast

def transaction(cd, start, end):
    """
        High-level que engloba todas as regras de negócio
    """

    today = date_util.today()
    date_off_limits = date_util.days_diff(today, start) > 7 or \
        date_util.days_diff(today, end) > 7
    crossed_ends = date_util.days_diff(start, end) < 0
    
    off_limits_obj = {'error': "date off limits"}
    crossed_obj = {'error': "limit dates are crossed"}
    error_dump = ""
    
    if date_off_limits:
        error_dump = json.dumps(off_limits_obj)
    elif crossed_ends:
        error_dump = json.dumps(crossed_obj)
    error = date_off_limits or crossed_ends

    return error_dump if error else data_in_timespan(cd, start, end)

def data_in_timespan(cd, start, end):
    """
        Retorna os dados dentro do período de tempo requisitado
        Procura no banco de dados e, caso não haja
        chama update() para falar com a API e atualizar o banco de dados
    """
    
    forecasts = Forecast.query.filter_by(city_code=cd)

    timespan = abs(date_util.days_diff(start, end))
    entries = []

    for cast in forecasts:
        dt = cast.date
        if (date_util.is_between(dt, start, end)): 
            entries.append(cast)
            print(len(entries))

    print(timespan)
    if len(entries) != timespan + 1:
        entries = update(cd, start, end)

    return filter_data(entries)

def update(cd, start, end):
    """
        Requisita dados via a API, armazena no banco e retorna as
        entradas dentro do timespan
    """
    data = api.get_request(cd)
    forecasts = data["data"]
    entries = []

    for i in range(7):
        cast = forecasts[i]
        dt = cast["date"]
        
        max_t = cast["temperature"]["max"]
        min_t = cast["temperature"]["min"]
        prob = cast["rain"]["probability"]
        vol = cast["rain"]["precipitation"]

        modeled_cast = Forecast(city_code=cd, date=dt, max_temp=max_t, min_temp=min_t, \
            rain_prob=prob, rain_vol=vol)

        if date_util.is_between(dt, start, end):
            entries.append(modeled_cast)

        #tinha q mudar isso daqui
        query = Forecast.query.filter_by(city_code=cd, date=dt)
        if len(query.all()) == 0: 
            DB.session.add(modeled_cast)
    DB.session.commit()

    return entries

def filter_data(entries):
    """
        Percorre as listas e encontra as datas com maior temperatura,
        menor temperatura e maior probabilidade de chuva
    """
    max_t = 0
    min_t = 0
    prob = 0
    vol = 0
    date_max = '0000-00-00'
    date_min = '0000-00-00'
    date_prob = '0000-00-00'
        
    for entry in entries:
        if (entry.max_temp > max_t or date_max == '0000-00-00'):
            max_t = entry.max_temp
            date_max = entry.date
            
        if (entry.min_temp < min_t or date_min == '0000-00-00'):
            min_t = entry.min_temp
            date_min = entry.date
            
        if (entry.rain_prob > prob or date_prob == '0000-00-00'):
            prob = entry.rain_prob
            vol = entry.rain_vol
            date_prob = entry.date
    
    data_obj = { 'date_max': date_max, 'max_t': max_t, 'date_min': date_min, \
        'min_t': min_t, 'date_prob': date_prob, 'vol': vol}
    return json.dumps(data_obj)
