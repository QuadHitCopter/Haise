from ina219 import INA219
from ina219 import DeviceRangeError
import time
from time import sleep
import sys
import csv
from datetime import datetime



def read():
    global ina
    b_v = ina.voltage()
    try:
        b_c = ina.current()
        b_p = ina.power()
    except DeviceRangeError as e:
        print(e)
    return b_v, b_c, b_p

def measure(Dt,h,name,mode,address=0x40):
    global ina
    SHUNT_OHMS = 0.1
    max_AMP = 1.0
    ina = INA219(SHUNT_OHMS,max_AMP,address=address)
    ina.configure(ina.RANGE_16V)
    dat = open(f"./data/power_data_{name}",mode)
    writer = csv.writer(dat)
    if mode == "w":
        header = ["time","voltage [V]","current [mA]", "power mW"]
        writer.writerow(header)

    t = []
    V_all = []
    I_all = []

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

def camera_shoot():
    from picamera import PiCamera
    
    camera =PiCamera()
    camera.resolution = (144,144)
    camera.framerate = 10
    camera.start_preview()
    print("Consumo con cámara")
    name = "ALL"
    Dt = 3
    h = 0.5
    measure(Dt,h,name,"w",address=0x40)
    tim = datetime.now().time()
    
    camera.annotate_text = f"{datetime.now().time()}"
    camera.annotate_text_size = 10
    camera.capture("./SS_now.jpg")
    camera.stop_preview()
    del PiCamera
    
    print("Consumo IDLE")
    
    measure(Dt,h,name,"a",address=0x40)
    



