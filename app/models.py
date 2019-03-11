"""
    Schemas da database
"""

from app import DB

class Forecast(DB.Model):
    """
        Previsões de temperatura e chuva associadas a uma cidade e data
    """

    id = DB.Column(DB.Integer, primary_key=True)
    city_code = DB.Column(DB.Integer, index=True)
    date = DB.Column(DB.String(10), index=True)
    max_temp = DB.Column(DB.Integer, index=True)
    min_temp = DB.Column(DB.Integer, index=True)
    rain_prob = DB.Column(DB.Integer, index=True)
    rain_vol = DB.Column(DB.Integer, index=True)

    def __repr__(self):
        return '<Forecast {}>'.format(self.date + ' - ' + str(self.city_code))

#isso tá ligeiramente hacky, se não estiver rodando o problema deve estar aqui
DB.create_all()
