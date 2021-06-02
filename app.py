import methods
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app)

@app.route('/')
def get_data():        
    return methods.get_data()

@app.route('/update')
def update_data():
    return methods.update_db()

if __name__ == "__main__":
    app.run(debug=True, port = 5000)