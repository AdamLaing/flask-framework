from flask import Flask, render_template, request, redirect, flash, Blueprint, g, session, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
import functools
import numpy as np
import pandas as pd
import datetime
import statsmodels.formula.api as sm

DEBUG = True 
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


# # import requests, zipfile2, io
# # import pandas as pd
# # import quandl
# # from bokeh.plotting import figure
# # from bokeh.resources import CDN
# # from bokeh.embed import components

# # quandl.ApiConfig.api_key = "gDuZE7V4QqDbup-gRfYy"
# # #get APIs for tickers and data
# # tickers = requests.get('https://www.quandl.com/api/v3/databases/WIKI/codes'
                   # # '?api_key=gDuZE7V4QqDbup-gRfYy')

# # tickers = zipfile2.ZipFile(io.BytesIO(tickers.content))
# # tickers.extractall()
# # tickers = pd.read_csv(zipfile2.ZipFile.namelist(tickers)[0], header=None,
                      # # usecols=[0])
# # tickers = tickers[0].astype('str')
# # tickers = tickers.str.replace('WIKI/', '').tolist()

# class ReusableForm(Form):
    # name = TextField('Ticker:', validators=[validators.required()])
 

# @app.route('/')
# def index():
  # return render_template('index.html')

  
# @app.route('/close', methods=('GET', 'POST'))
# def close():
    # form = ReusableForm(request.form)

    # if request.method == 'POST':
        # tick = request.form['name']
        # error = None
        
        # if not tick:
            # error = 'Please enter a ticker.'

        # elif tick not in ['GOOG', 'AAPL']:
            # error = 'Company not found. Try another Ticker. Please use capital letters.'


        # if error is None:
            # data = quandl.get_table('WIKI/PRICES',
                        # qopts = { 'columns': ['ticker', 'date', 'close'] },
                        # ticker = [tick],
                        # date = { 'gte': '2018-01-01', 'lte': '2018-01-31' })
            # p = figure(plot_width=400, plot_height=400, x_axis_type='datetime')
  
            # # add a line renderer
            # p.line(data['date'], data['close'], line_width=2)
  
            # script, div = components(p)
            # flash('{} close price for January 2018'.format(tick))
            # return render_template('close.html', div=div, script=script, form=form)

        # flash(error)
    # return render_template('close.html', form=form)


# bp = Blueprint('kick', __name__, url_prefix='/kick')

# import jinja2

# def render_without_request(template_name, **template_vars):
    # """
    # Usage is the same as flask.render_template:

    # render_without_request('my_template.html', var1='foo', var2='bar')
    # """
    # env = jinja2.Environment(
        # loader=jinja2.PackageLoader('hello','templates')
    # )
    # template = env.get_template(template_name)
    # return template.render(**template_vars)




class KickstarterForm(Form):
    main = TextField('Main Category:', validators=[validators.required()])
    sub = TextField('Sub-category:', validators=[validators.required()])
    camp_dur = TextField('Campaign Duration (days):', validators=[validators.required()])
    launch_month = TextField('Launch Month:', validators=[validators.required()])
    goal = TextField('Goal Amount (USD):', validators=[validators.required()])
    pledges = TextField('Please enter the values of each pledge level ('
                         'including possible repeats) in USD, each separated '
                         'by a space.:', validators=[validators.required()])
    description = TextAreaField('Please enter the full text description of your campaign.\n'
							'Please separate paragraphs by an empty line. :', validators=[validators.required()])


@app.route('/')
def index():
    # Index will give options of exploring Kickstarter, Indiegogo, possibly
    # other data if I find suitable APIs, and list plots and general info
    # about the datasets.
    return render_template('index.html')

@app.route('/kickstarter', methods=('GET', 'POST'))
def kickstarter():
    form = KickstarterForm(request.form)
    if request.method == 'POST':

        kdat = pd.read_json(path_or_buf='kdat.json',
                            compression='zip')
        main = request.form['main']
        sub = request.form['sub']
        camp_dur = request.form['camp_dur']
        launch_month = request.form['launch_month']
        goal = request.form['goal']
        pledges = request.form['pledges']
        dsecription = request.form['description']
        # This will all need to be updated
        error = None

        if launch_month not in np.arange(1, 13) and launch_month != "None":
            error = 'Please enter launch month as a number from 1 to 12, ' \
                    'or enter "None".'

        elif main not in kdat.main and main != "None":
            error = 'Invalid Main Category. Please check your spelling, ' \
                    'or enter "None".'

        elif sub not in kdat.sub and sub != "None":
            error = 'Invalid Sub-category. Please check your spelling, ' \
                    'or enter "None".'

        elif not isinstance(camp_dur, int) and camp_dur != "None":
            error = 'Invalid Campaign Duration. Please enter an integer, ' \
                    'or enter "None".'

        elif not isinstance(goal, int) and goal != "None":
            error = 'Invalid Goal Amount. Please enter an integer, ' \
                    'or enter "None".'
        if error is None:
            data = kdat
            if main != "None":
                data = data.loc[data.main == main]
            if sub != "None":
                data = data.loc[data.sub == sub]
            if camp_dur != "None":
                data = data.loc[data.duration == camp_dur]
            if launch_month != "None":
                data = data.loc[data.launch_month == launch_month]
            if goal != "None":
                data = data.loc[
                    data.goal <= 1.1 * goal and data.goal >= .9 * goal]

            # Delete rows with duplicate IDs
            data = data.drop_duplicates(subset="id")

            p = figure(plot_width=400, plot_height=400)

            # add a line renderer
            # p.line(data['date'], data['close'], line_width=2)

            script, div = components(p)
            flash('[Placeholder Text')
            return render_template('kickstarter.html', div=div, script=script,
                                   form=form)

        flash(error)
    else:
        form = KickstarterForm(request.form)
    return render_template('kickstarter.html', form=form)
	
if __name__ == '__main__':
  app.run(port=33507)
