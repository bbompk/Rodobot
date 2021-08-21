from flask import Flask
from threading import Thread

app = Flask('')

port=8080
@app.route('/')
def home():
    return "Server is currently running"

def run():
  app.run(host='0.0.0.0',port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()