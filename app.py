from flask import Flask, jsonify
import psutil

app = Flask(__name__)
STEP = 1024
@app.route("/")
def index():
    return {
        "cpu": get_cpu(),
        "mem": get_mem(),
        "disks": get_disk(),
        "network": get_network(),
        "sensors": get_sensors()
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
    return {
        "total":getStr(mem[0], 1/(STEP**3), 1, " GB"),
        "available":getStr(mem[0]-mem[3], 1/(STEP**3), 1, " GB"),
        "percent": getStr(mem[2], 1, 1, "%"),
        "used": getStr(mem[3], 1/(STEP**3), 1, " GB"),
        }
    
def get_disk():
    drives = list()
    disks = list(filter(lambda d: d[2], psutil.disk_partitions()))
    for disk in disks:
        storage = psutil.disk_usage(disk[1])
        if(storage[0]>0.1*(STEP**3)):
            drives.append({
                "device": disk[0],
                "mountpoint": disk[1],
                "fstype": disk[2],
                "storage":{
                    "total": getStr(storage[0], 1/(STEP**3), 1, " GB"),
                    "available": getStr(storage[2], 1/(STEP**3), 1, " GB"),
                    "percent": getStr(storage[3], 1, 1, "%"),
                    "used": getStr(storage[1], 1/(STEP**3), 1, " GB"),
                }
            })
    return drives


def get_network():
    # conns = list(filter(lambda c: c[1],psutil.net_if_stats()))
    conns = list(filter(lambda c: c[1],[(k, *v) for k, v in psutil.net_if_stats().items()]))
    connections = list()
    for conn in conns:
        connections.append({
            "name": conn[0],
            "speed": getStr(conn[3], 1,1," MB"),
        })
    return connections


def get_sensors():
    sensors = list()
    try:
        sensors.append(psutil.sensors_temperatures())
    except Exception:
        pass
    try:
        sensors.append(psutil.sensors_fans())
    except Exception:
        pass
    return sensors