import PySimpleGUI as sg
import time
import printer_com
import icons

BED_MAX_TEMPERATURE = 60 # °C
TARGET_TEMP_UPDATE_DELAY = 1000 # us
TEMP_MES_DELAY = 1 # s
temp_target  = 0
current_temp = 0

temp_target_txt    = sg.Text(str(temp_target) + " °C")
current_temp_txt   = sg.Text(str(current_temp)  + " °C")
update_btn         = sg.Button("", size = (4,2), disabled = True, button_color="#660000", image_filename="btn_update_icon.png")
target_temp_slider = sg.Slider((0, BED_MAX_TEMPERATURE), orientation='horizontal', enable_events = True)

f_temp_slider    = [[target_temp_slider]]
f_target_temps   = [[temp_target_txt]]
f_current_temps  = [[current_temp_txt]]

layout = [[sg.Frame("Temperature target :", f_temp_slider)], 
          [sg.Frame("Target : ", f_target_temps), sg.Frame("Current : ", f_current_temps), update_btn]]

window = sg.Window('TempControl', layout, no_titlebar=False, auto_save_location=True, icon=icons.THERMOMETER)

def get_actual_temp_target(ser):
    actual_target = printer_com.getBedTempTarget(ser)
    temp_target_txt.update(value = str(int(actual_target))  + " °C")

def update_target_temp(nt,ser):
    printer_com.setTargetBedTemp(ser, int(nt))

    # validated by getting actual temp target
    get_actual_temp_target(ser)


def get_current_temp(ser):
    return printer_com.getBedTemp(ser)

def connected(ser):
    bedt = printer_com.getBedTemp(ser)
    if bedt != None:
        return True
    return False

# init connection
ser = printer_com.openSerial()

t1 = int(time.time() * 1000)
while True:    
    
    event, values = window.read(timeout=1000)

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if connected(ser):
        update_btn.update(disabled=False, button_color="#2D962D")

    # acquiring current temp every second
    t2 = int(time.time() * 1000)
    if t2 - t1 >= TEMP_MES_DELAY * 1000:
        current_temp = get_current_temp(ser)
        current_temp_txt.update(value = str(int(current_temp)) + " °C")
        get_actual_temp_target(ser)
        t1 = int(time.time() * 1000)

    if event in update_btn.key:
        temp_target = values[target_temp_slider.key]     
        update_target_temp(temp_target, ser)


printer_com.closeSerial(ser)
window.close()