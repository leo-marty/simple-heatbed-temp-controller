import serial
import sys
import printer_com
import time

serial_port = "COM3"
serial_baude_rate = 115200

ser = printer_com.openSerial()

if not ser.is_open:
    print('Error: unable to connect to printer via serial interface.')
    sys.exit()

# Connection OK
print(f"Serial interface opened on port {ser.port} @ {ser.baudrate} bauds")
print("Trying to read bed temp...")

interact = True
while interact:
    i = input(">>> ")

    if i == "q":
        interact = False
    elif i == "g":
        temp_target = printer_com.getBedTempTarget(ser)
        print("Temperature target: ", temp_target)
    elif i != "":
        temp_target = 0
        try:
            temp_target = int(i)
        except Exception:
            print("Error: temperature target is not an integer.")
            temp_target = 0

        if temp_target >= 60:
            print("Error: temperature target too high (>= 60°C)")
            temp_target = 0

        print(f"Setting target temperature to {temp_target}")    
        res = printer_com.setTargetBedTemp(ser, str(temp_target))

        if not res:
            print("Error: cannot update bed temperature target.")

    
        #print(f"Printer actual temp target: {printer_com.getBedTempTarget(ser)}")
        
    else: 
        print("Reading bed temperature : ")
        bed_temp = printer_com.getBedTemp(ser)
        print(bed_temp, "°C")


printer_com.closeSerial(ser)