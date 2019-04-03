from flask import Flask, render_template
from flask_restful import Api

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

api = Api(app)

import views, models, resources

api.add_resource(resources.DownloadPackage, '/packages')
api.add_resource(resources.GetPackageCount, '/package/count')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
