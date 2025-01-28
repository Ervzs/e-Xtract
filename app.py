from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/disposal-sites')
def disposal_sites():
    return render_template('disposal_sites.html')

@app.route('/extract')
def extract():
    return render_template('extract.html')

@app.route('/get-started')
def get_started():
    return render_template('get_started.html')

if __name__ == '__main__':
    app.run()