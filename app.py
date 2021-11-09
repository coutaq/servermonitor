from flask import Flask, jsonify, request, abort
import psutil
import hashlib
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)
STEP = 1024
api_keys = list()

def get_keys():
    f = open("APIKEYS", "r")
    for x in f:
      if(x):
          api_keys.append( hashlib.sha256(x.strip().encode()).hexdigest())
    f.close()
    
get_keys()

@app.route("/", methods=["GET"])
def index():
    check_key(request.args.get("key"))
    return get_data()
    
@sock.route('/data')
def echo(ws):
    check_key(request.args.get("key"))
    while True:
        ws.send(get_data())
def check_key(key):
    if hashlib.sha256(str(key).strip().encode()).hexdigest() not in api_keys:
        abort(401)
def get_str(value, multiplier, accuracy, suffix):
    return str(round(value*multiplier, accuracy))+suffix

def get_data():
      return {
        "cpu": get_cpu(),
        "mem": get_mem(),
        "disks": get_disk(),
        "network": get_network(),
        "temps": get_temps()
      }
def get_cpu():
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    total_load = psutil.cpu_percent(0)
    cores_load = psutil.cpu_percent(0, percpu=True)
    return {
        "cores": cores,
        "threads":threads,
        "total_load":total_load,
        "threads_load":cores_load
    }
def get_mem():
    mem = psutil.virtual_memory()
    return {
        "total":get_str(mem[0], 1/(STEP**3), 1, " GB"),
        "available":get_str(mem[0]-mem[3], 1/(STEP**3), 1, " GB"),
        "percent": get_str(mem[2], 1, 1, "%"),
        "used": get_str(mem[3], 1/(STEP**3), 1, " GB"),
        }
    
def get_disk():
    disks = list()
    for disk in psutil.disk_partitions():
        if(disk[2]):
            storage = psutil.disk_usage(disk[1])
            if(storage[0]>0.2*(STEP**3)):
                disks.append({
                    "device": disk[0],
                    "mountpoint": disk[1],
                    "fstype": disk[2],
                    "storage":{
                        "total": get_str(storage[0], 1/(STEP**3), 1, " GB"),
                        "available": get_str(storage[2], 1/(STEP**3), 1, " GB"),
                        "percent": get_str(storage[3], 1, 1, "%"),
                        "used": get_str(storage[1], 1/(STEP**3), 1, " GB"),
                    }
                })
    return disks


def get_network():
    conns = list()
    for conn in [(k, *v) for k, v in psutil.net_if_stats().items()]:
        if(conn[1] and conn[3]>0):
            conns.append({
                "name": conn[0],
                "speed": get_str(conn[3], 1,1," MB"),
            })
    return conns


def get_temps():
    temps = list()
    # try:
    for temp in psutil.sensors_temperatures():
        t = temp._asdict()
        print(t)
        # temps.append({
        #     "name": t[0],
        #     "critical": t[1],
        #     "current": t[2],
        #     "high": t[3]
        #     })
    # except Exception:
    #     pass
    # try:
    #     sensors["fans"] = (psutil.sensors_fans())
    # except Exception:
    #     pass
    return temps