from flask import Flask, render_template, request, redirect, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

DEBUG = True 
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


import requests, zipfile2, io
import pandas as pd
import quandl
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

quandl.ApiConfig.api_key = "gDuZE7V4QqDbup-gRfYy"
#get APIs for tickers and data
tickers = requests.get('https://www.quandl.com/api/v3/databases/WIKI/codes'
                   '?api_key=gDuZE7V4QqDbup-gRfYy')

tickers = zipfile2.ZipFile(io.BytesIO(tickers.content))
tickers.extractall()
tickers = pd.read_csv(zipfile2.ZipFile.namelist(tickers)[0], header=None,
                      usecols=[0])
tickers = tickers[0].astype('str')
tickers = tickers.str.replace('WIKI/', '').tolist()

class ReusableForm(Form):
    name = TextField('Ticker:', validators=[validators.required()])
 

@app.route('/')
def index():
  return render_template('index.html')

  
@app.route('/close', methods=('GET', 'POST'))
def close():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        tick = request.form['name']
        error = None
        
        if not tick:
            error = 'Please enter a ticker.'

        elif tick not in tickers:
            error = 'Company not found. Try another Ticker. Please use capital letters.'


        if error is None:
            data = quandl.get_table('WIKI/PRICES',
                        qopts = { 'columns': ['ticker', 'date', 'close'] },
                        ticker = [tick],
                        date = { 'gte': '2018-01-01', 'lte': '2018-01-31' })
            p = figure(plot_width=400, plot_height=400, x_axis_type='datetime')
  
            # add a line renderer
            p.line(data['date'], data['close'], line_width=2)
  
            script, div = components(p)
			flash('{} close price for January 2018'.format(tick))
            return render_template('close.html', div=div, script=script, form=form)

        flash(error)
    return render_template('close.html', form=form)
    
if __name__ == '__main__':
  app.run(port=33507)
