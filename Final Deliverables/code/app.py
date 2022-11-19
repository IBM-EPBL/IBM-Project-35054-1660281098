import re
import ibm_db
from flask_mail import Mail, Message
from newsapi.newsapi_client import NewsApiClient
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

mail = Mail(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "********@gmail.com"
app.config["MAIL_PASSWORD"] = "*******"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)

app.secret_key = "a"

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dqw60999;PWD=ICZKlklYL4gstwFO", "", "")

global newsresource

@app.route("/")

def home():

        return render_template("login.html")

@app.route("/signup")

def signup():

        return render_template("signup.html")

@app.route("/dashboard")

def dashboard():

        if(session["loggedin"] == True):

                return render_template("dashboard.html")
        
        return render_template("login.html")

@app.route("/login", methods = ["GET", "POST"])

def login():

        global userid

        msg = " "

        if request.method == "POST":

                username = request.form["username"]
                password = request.form["password"]
                
                usr_lst = []
                pass_lst = []

                data = ibm_db.exec_immediate(conn, "SELECT \"USERNAME\", \"PASSWORD\" FROM \"DQW60999\".\"USERDETAILS\";")

                while ibm_db.fetch_row(data) != False:

                        usr_lst.append(ibm_db.result(data, 0).replace(" ", ""))
                        pass_lst.append(ibm_db.result(data, 1).replace(" ", ""))
 
                if (username in usr_lst and password in pass_lst):
 
                        session["loggedin"] = True

                        msg = "Logged in successfully !"
 
                        return render_template("dashboard.html")
 
                else:
 
                        msg = "Incorrect username / password !"
 
                        return render_template("login.html", msg = msg)

@app.route("/register", methods = ["GET", "POST"])

def register():

        if request.method == "POST":

                fullname = request.form["fullname"]
                email = request.form["email"]
                username = request.form["username"]
                password = request.form["password"]

                insert = ibm_db.exec_immediate(conn, "INSERT INTO \"DQW60999\".\"USERDETAILS\" VALUES ('{}', '{}', '{}', '{}');".format(fullname, email, username, password))

                return render_template("newaccount.html")
        
@app.route("/news", methods = ["GET", "POST"])

def news():

        f = open("./api.txt", "r")

        newsapi = NewsApiClient(api_key = f.read())

        if request.method == "POST":

                if(request.form["newsresource"] == "google"):

                        newsresource = "google-news-in"
                        
                        msg = "GOOGLE NEWS"

                elif(request.form["newsresource"] == "bbc"):

                        newsresource = "bbc-news"

                        msg = "BBC NEWS"

                elif(request.form["newsresource"] == "toi"):

                        newsresource = "the-times-of-india"

                        msg = "Times of India"

                elif(request.form["newsresource"] == "abc"):

                        newsresource = "abc-news"

                        msg = "ABC NEWS"

        topheadlines = newsapi.get_top_headlines(sources=newsresource) 

        articles = topheadlines["articles"] 

        news = []
        author = []
        publishedAt = []
        desc = []
        img = []
        content = []
        url = []

        for i in range(len(articles)):

                myarticles = articles[i]
                news.append(myarticles["title"])
                author.append(myarticles["author"])
                publishedAt.append(myarticles["publishedAt"])
                desc.append(myarticles["description"])
                img.append(myarticles["urlToImage"])
                content.append(myarticles["content"])
                url.append(myarticles["url"])
                mylist = zip(news, author, publishedAt, desc,img, content, url)

        return render_template("news.html", context = mylist)

@app.route("/logout")

def logout():

        session["loggedin"] = False

        msg = "Logged out successfully......"

        return render_template("login.html", msg = msg)

if __name__ == "__main__":

    app.run(host = "0.0.0.0", port = 5000, debug = True, threaded = True)