from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route("/")
def index():
    load = get_load()
    return {
        "cpu": load[0],
        "mem": load[1],
    }

def get_load():
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(1)
    return(cpu,mem)