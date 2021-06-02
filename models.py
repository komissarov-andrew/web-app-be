from app import db

class Metals(db.Model):
    __tablename__ = 'metals'
    date = db.Column(db.Date())
    code = db.Column(db.Integer())
    name = db.Column(db.String())
    buy = db.Column(db.Float())
    sell = db.Column(db.Float())

    def __init__(self, date, code, name, buy, sell):
        self.date = date
        self.code = code
        self.name = name
        self.buy = buy
        self.sell = sell

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'date': self.date,
            'code': self.code,
            'name':self.name,
            'buy':self.buy,
            'sell':self.sell
        }