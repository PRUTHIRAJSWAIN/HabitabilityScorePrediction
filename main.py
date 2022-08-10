from flask import Flask, render_template,request,url_for
from wtforms import StringField,PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

import pickle
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
model=pickle.load(open('regress.pkl','rb'))

#create flask app
app=Flask(__name__)



class features():
    temp=[]
    AreaValid=True
    TrafficValid=True
    AirValid=True
    NebValid=True
    Property_Type = ['Container Home', 'Apartment', 'Pension', 'Single-family home', 'Bungalow']
    Number_of_Windows=[0,1,2,3,4,5,6]
    Number_of_Doors=[1,2,3,4,5,6]
    Furnishing = ['Unfurnished', 'Semi Furnished', 'Fully Furnished']
    Number_of_Powercuts=[0,1,2,3]
    Water_supply = ['Once in a two days', 'Once in a day - Evening', 'Once in a day - Morning', 'All time']
    crime_rate = ['High', 'Above average', 'Below average', 'Low']
    dustAndnoise = ['High', 'Medium', 'Low']
    ScoreAvailable=False
    ans=0
    def validcheck(self):
        if self.temp[1].isnumeric():
            AreaValid=True
        else :
            AreaValid=False
        if self.temp[8].isnumeric():
            TrafficValid=True
        else :
            TrafficValid=False
        if self.temp[11].isnumeric():
            AirValid=True
        else :
            AirValid=False
        if self.temp[12].isnumeric():
            NebValid=True
        else :
            NebValid=False
        return (AreaValid & TrafficValid & NebValid & AirValid)

feature=features()
@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html', features=feature)

@app.route('/predict',methods=['POST'])
def pr():

    feature.temp.append(feature.Property_Type.index(request.form.get('p')))
    feature.temp.append(request.form.get('a'))
    feature.temp.append(int(request.form.get('nw')))
    feature.temp.append(int(request.form.get('nd')))
    feature.temp.append(feature.Furnishing.index(request.form.get('f')))
    feature.temp.append(int(request.form.get('pc')))
    feature.temp.append(1 if request.form.get('pb') == 'on' else 0)
    feature.temp.append(feature.Water_supply.index(request.form.get('w')))
    feature.temp.append(request.form.get('t'))
    feature.temp.append(feature.crime_rate.index(request.form.get('c')))
    feature.temp.append(feature.dustAndnoise.index(request.form.get('dust')))
    feature.temp.append(request.form.get('air'))
    feature.temp.append(request.form.get('n'))
    print(feature.temp)
    #if feature.validcheck():
    data = np.array([feature.temp])
    result = model.predict(data)
    feature.ans = result
    feature.ScoreAvailable = True
    return render_template('index.html', features=feature,ans=feature.ans)
    # else:
    #     text=""
    #     if feature.AirValid:
    #         text+='Air Quality Index'
    #     if feature.NebValid:
    #         text+='Neighborhood review'
    #     if feature.TrafficValid:
    #         text += 'Traffic Density score'
    #     if feature.AreaValid:
    #         text += 'Area'
    #     if not True:
    #         text+='Hula'
    #     text='Enter Valid value for '+text
    #     return render_template('index.html', features=feature,ans=text)

if __name__=='__main__':
    app.run(debug=True)