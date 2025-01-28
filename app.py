from flask import Flask
from blueprints.views.views import views
from blueprints.routing.routing import dispose
from blueprints.models.extract import extract

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(dispose, url_prefix='/')
app.register_blueprint(extract, url_prefix='/')

if __name__ == '__main__':
    app.run()