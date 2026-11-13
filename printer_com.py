import time
import serial

PRINTER_READ_BED_TEMP_CMD = "M105"
PRINTER_SET_TARGET_BED_TEMP_CMD = "M140 S" # add temperature in Celsius after S



def openSerial():
    serial_port = "COM3"
    serial_baude_rate = 115200

    ser = serial.Serial(parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)

    ser.baudrate = serial_baude_rate
    ser.port = serial_port

    ser.open()

    if not ser.is_open:
        print('Error: unable to connect to printer via serial interface.')
        return None

    return ser


def closeSerial(ser):
    ser.close()

def sendPrinterCmd(ser, cmd):

    # adding newlines and converting into bytes object
    #print("Sending command")
    wcmd = (cmd + "\n").encode()
    ser.write(wcmd)

def readPrinterSer(ser):
    printer_res = None
    try: 
        printer_res = ser.readline()
    except Exception as e:
        print(e)
        return None

    return printer_res


def getBedTemp(ser):
    get_bed_temp_cmd = PRINTER_READ_BED_TEMP_CMD

    # Sending request for temps
    sendPrinterCmd(ser, get_bed_temp_cmd)
    # Reading response
    printerResponse = readPrinterSer(ser)

    if printerResponse == None:
        print("Error: Failling to read printer temperatures...")
        return None

    printerResponse = printerResponse.decode("utf-8")

    if printerResponse[0:2] != "ok":
        print("Error: internal printer error")
        return None

    # extract temp from response
    # format : ok T:TEMP_BUSE/TEMP_BUSE_TARGE B:TEMP_BED/TEMP_BED_TARGET
    bed_temp = printerResponse.split(":")[-1].split("/")[0]

    return bed_temp

def getBedTempTarget(ser):
    get_bed_temp_cmd = PRINTER_READ_BED_TEMP_CMD

    # Sending request for temps
    sendPrinterCmd(ser, get_bed_temp_cmd)
    # Reading response
    printerResponse = readPrinterSer(ser)

    if printerResponse == None:
        print("Error: Failling to read printer temperatures...")
        return None

    printerResponse = printerResponse.decode("utf-8")

    if printerResponse[0:2] != "ok":
        print("Error: internal printer error")
        return None

    # extract temp from response
    # format : ok T:TEMP_BUSE/TEMP_BUSE_TARGE B:TEMP_BED/TEMP_BED_TARGET
    bed_temp_target = printerResponse.split(":")[-1].split("/")[1]

    return bed_temp_target

def setTargetBedTemp(ser, temp):
    set_bed_target_temp = PRINTER_SET_TARGET_BED_TEMP_CMD + str(temp)

    # Sending temperature target change request
    sendPrinterCmd(ser, set_bed_target_temp)

    # Reading response
    answer = readPrinterSer(ser).decode("utf-8").strip("\n")

    if answer == "ok":
        return True
    else: 
        return False

    

