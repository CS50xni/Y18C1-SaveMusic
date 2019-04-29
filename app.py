from flask import Flask, render_template as render, redirect, url_for, request, Markup

app = Flask(__name__)

@app.route('/')
def index():
    return render('index.html')