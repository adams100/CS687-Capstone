from machine import Pin
import time
import network
import utime
import machine
import urequests

def connect():
    led = machine.Pin("LED", machine.Pin.OUT)
    led.on()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    with open("wirelesscreds", "r") as file:
        creds = file.read()
        name = creds.split(":")[0]
        psswd = creds.split(":")[1]
    wlan.connect(name, psswd)
    while wlan.status() < 3:
        pass
    print("connected!")
    led.off()


def send_data():
    pin = Pin(28, Pin.IN)
    currentState = pin.value()
    currentState = 0
    now = utime.localtime()
    formatted_time = "{:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5])
    formatted_date = "{:04d}:{:02d}:{:02d}".format(now[0], now[1], now[2])
    t = formatted_date + "T" + formatted_time
    
    if currentState == 1:  # Check if the pin is HIGH
        status = "BIN EMPTY"
    else:
        status = "BIN FULL"
    data = {"sampleTime": t, "targetindex": "waste", "Current State": status, "IntStatus": currentState}
    try:
        r = urequests.post("http://192.168.0.230:30983", timeout=1, json=data)
        r.close()
        print(r.status_code, "sent!")
    except OSError as e:
        print(e)
        pass

    

if __name__ == "__main__":
    

    connect()
    while True:
        send_data()
        
        time.sleep(1)
