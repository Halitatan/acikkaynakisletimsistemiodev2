from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Cars(Resource):
    def get(self):
        data = pd.read_csv('otomobilfiyatlari.csv')

        result = data[['marka', 'model', 'donanim', 'motor', 'yakit', 'vites', 'fiyat', 'websitesi']].to_dict('records')
        return {'data' : result}, 200

    def post(self):
        marka = request.args['marka']
        model  = request.args['model']
        donanim = request.args['donanim']
        motor = request.args['motor']
        yakit = request.args['yakit']
        vites = request.args['vites']
        fiyat = request.args['fiyat']
        websitesi = request.args['websitesi']

        req_data = pd.DataFrame({
            'marka': [marka],
            'model': [model],
            'donanim': [donanim],
            'motor': [motor],
            'yakit': [yakit],
            'vites': [vites],
            'fiyat': [fiyat],
            'websitesi': [websitesi]
        })

        data = pd.read_csv('otomobilfiyatlari.csv')
        data = data.append(req_data, ignore_index=True)
        data.to_csv('otomobilfiyatlari.csv', index=False)

        return {'message' : 'Record successfully added.'}, 200

class CarName(Resource):
    def get(self, name):
        data = pd.read_csv('otomobilfiyatlari.csv')
        data = data.to_dict('records')

        for entry in data:
            if entry['marka'] == name:
                return {'data' : entry}, 200

        return {'message' : f"No entry found with this car brand: {name}."}, 404

class CarWebsites(Resource):
    def get(self):
        data = pd.read_csv('otomobilfiyatlari.csv', usecols=['websitesi'])
        data = data.to_dict('records')
        return {'data' : data}, 200

api.add_resource(Cars, '/cars')
api.add_resource(CarWebsites, '/carwebsites')
api.add_resource(CarName, '/cars/<string:name>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6767)

