from flask import Flask, render_template, request,redirect,url_for
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return redirect("/setLocation/")

@app.route("/setLocation/") 
def main():
    return render_template('setLocation.html', var = 'test')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug =True)
