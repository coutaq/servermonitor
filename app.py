from flask import Flask, jsonify
import psutil

app = Flask(__name__)
STEP = 1024
@app.route("/")
def index():
    return {
        "cpu": get_cpu(),
        "mem": get_mem(),
    }

def getStr(value, multiplier, accuracy, suffix):
    return str(round(value*multiplier, accuracy))+suffix
def get_cpu():
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    total_load = psutil.cpu_percent(1)
    cores_load = psutil.cpu_percent(1, percpu=True)
    return {
        "cores": cores,
        "threads":threads,
        "total_load":total_load,
        "cores_load":cores_load
    }
def get_mem():
    mem = psutil.virtual_memory()
    print(mem)
    return {
        "total":getStr(mem[0], 1/(STEP**3), 1, " GB"),
        "available":getStr(mem[1], 1/(STEP**3), 1, " GB"),
        "percent": getStr(mem[2], 1, 1, "%"),
        "used": getStr(mem[3], 1/(STEP**3), 1, " GB"),
        "free":getStr(mem[4], 1/(STEP**3), 1, " GB")
        }