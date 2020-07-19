from flask import Flask, render_template, request 
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import numpy as np
import seaborn
import matplotlib 
matplotlib.axes.Axes.pie 
matplotlib.pyplot.pie
from covid import Covid 

app = Flask(__name__)
covidHopkins = Covid(source="john_hopkins") #johns hppkins API to get data

def showChart(country1, country2, info1, info2, title, saveAs):
    sizes = [info1, info2]
    explode = (0, 0)  
    labels = [country1, country2]
    if(info1>info2):
        colors = ["red","green"]
    else:
        colors = ["green","red"]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%', startangle=90)
    ax1.axis("equal") 
    plt.title(title, bbox={"facecolor":"0.8", "pad":5}, loc="left")
    imageName = saveAs + ".jpg"
    fig1.savefig(imageName)

def showGraph(country1, country2, info1, info2, yLabel, title, saveAs):
    objects = (country1, country2)
    y_pos = np.arange(len(objects))
    performance = [info1, info2]
    plt2.bar(y_pos, performance, align="center", alpha=0.5)
    plt2.xticks(y_pos, objects)
    plt2.ylabel(yLabel)
    plt2.title(title)
    imageName = saveAs + ".jpg"    
    plt2.savefig(imageName)
    
@app.route("/")
def home(): 
    return render_template("home.html")

@app.route("/data")
def data():
     country1 = request.args["country1"]
     country2 = request.args["country2"]
     country1Info = covidHopkins.get_status_by_country_name(country1)
     country2Info = covidHopkins.get_status_by_country_name(country2)
     country1List = [country1Info["confirmed"],country1Info["active"],country1Info["deaths"],country1Info["recovered"]]
     country2List = [country2Info["confirmed"],country2Info["active"],country2Info["deaths"],country2Info["recovered"]]
     titleOrder = ["Confirmed Cases", "Active Cases", "Deaths", "Recovered"]
     showChart(country1, country2, country1List[2], country2List[2], "Death Ratio", "deathChart")
     showChart(country1, country2, country1List[3], country2List[3], "Cases Ratio", "caseChart")
     #showGraph(country1, country2, country1List[2], country2List[2], "Deaths", "Death Counts", "deathGraph")
     #showGraph(country1, country2, country1List[3], country2List[3], "Cases", "Cases Counts", "caseGraph")
     return render_template("data.html", country1=country1, country2=country2, country1List=country1List, country2List=country2List, titleOrder=titleOrder)
     
@app.route("/visuals")
def chart():
    return render_template("visuals.html")

app.run(host="localhost", debug=True)

# maybe try returing the image in showChart and render it in the template