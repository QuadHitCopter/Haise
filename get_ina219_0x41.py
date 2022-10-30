from ina219 import INA219
from ina219 import DeviceRangeError
import time
from time import sleep
from picamera import PiCamera

SHUNT_OHMS = 0.1
max_AMP = 1.0
address = 0x40
ina = INA219(SHUNT_OHMS,max_AMP,address=0x40)
ina.configure(ina.RANGE_16V)
def read():
    b_v = ina.voltage()
    try:
        b_c = ina.current()
        b_p = ina.power()
    except DeviceRangeError as e:
        print(e)
    return b_v, b_c, b_p

import csv
from datetime import datetime
t = []
V_all = []
I_all = []

def measure(Dt,h):
    dat = open("./data/battery_dat.csv","w")
    writer = csv.writer(dat)
    header = ["time","voltage [V]","current [mA]", "power mW"]
    writer.writerow(header)

    for tt in range(int(Dt//h)):
        
        time.sleep(h)
    #     tim = tt*0.01
        timez = datetime.now().time()
        
    #     t.append(tim)
        a = read()
        v = a[0]
        i = a[1]
        p = a[2]
        linea = [timez,f"{v:.3f}",f"{i:.5f}",f"{p:.4f}"]
        print(linea)
        writer.writerow(linea)
    dat.close()

Dt=3 #Tiempo en segundos que quiere medir
h = 0.25 #paso de tiempo entre mediciones en segundos, minimo 0.01


camera =PiCamera()
camera.resolution = (480,480)
camera.framerate = 15
camera.start_preview()
print("Consumo con cámara")
measure(Dt,h)
camera.capture("./image2.jpg")
camera.stop_preview()
print("consumo sin cámara")
measure(Dt,h)
