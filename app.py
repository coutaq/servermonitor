from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route("/")
def index():
    return {
        "cpu": get_cpu(),
        "mem": get_mem(),
    }

def get_cpu():
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    total_load = psutil.cpu_percent(1)
    cores_load = psutil.cpu_percent(1, percpu=True)
    return {
        cores,
        threads,
        total_load,
        cores_load
    }
def get_mem():
    mem = psutil.virtual_memory()
    return mem