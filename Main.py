import pigpio
import requests
from time import sleep, strftime
from datetime import datetime


pi = pigpio.pi()

stripOneRed = 16
stripOneGreen = 20
stripOneBlue = 21

stripTwoRed = 13
stripTwoGreen = 19
stripTwoBlue = 26

nextBin = "None"
bin_colors = {
        "brownBin": (150, 75, 0),
        "greenBin": (0, 255, 0),
        "blueBin": (0, 0, 255),
        "purpleBin": (255, 0, 255)
    }

def allOff():
    pi.set_PWM_dutycycle(stripOneRed, 0)
    pi.set_PWM_dutycycle(stripOneGreen, 0)
    pi.set_PWM_dutycycle(stripOneBlue, 0)
    pi.set_PWM_dutycycle(stripTwoRed, 0)
    pi.set_PWM_dutycycle(stripTwoGreen, 0)
    pi.set_PWM_dutycycle(stripTwoBlue, 0)

def setError(e):
    log_exception(e)
    pi.set_PWM_dutycycle(stripOneRed, 255)
    pi.set_PWM_dutycycle(stripOneGreen, 0)
    pi.set_PWM_dutycycle(stripOneBlue, 0)
    pi.set_PWM_dutycycle(stripTwoRed, 255)
    pi.set_PWM_dutycycle(stripTwoGreen, 0)
    pi.set_PWM_dutycycle(stripTwoBlue, 0)

def EOM():    
    pi.set_PWM_dutycycle(stripOneRed, 255)
    pi.set_PWM_dutycycle(stripOneGreen, 255)
    pi.set_PWM_dutycycle(stripOneBlue, 0)
    pi.set_PWM_dutycycle(stripTwoRed, 255)
    pi.set_PWM_dutycycle(stripTwoGreen, 255)
    pi.set_PWM_dutycycle(stripTwoBlue, 0)

def setSingle(bin):

    if bin in bin_colors:
        red_value, green_value, blue_value = bin_colors[bin]
    else:
      raise ValueError('setSingle - getBin() Returned unexpected value: '+ bin)
        
    pi.set_PWM_dutycycle(stripOneRed, red_value)
    pi.set_PWM_dutycycle(stripOneGreen, green_value)
    pi.set_PWM_dutycycle(stripOneBlue, blue_value)
        
    pi.set_PWM_dutycycle(stripTwoRed, red_value)
    pi.set_PWM_dutycycle(stripTwoGreen, green_value)
    pi.set_PWM_dutycycle(stripTwoBlue, blue_value)
                
def setDouble(bins):
    bin1 = bins.split(",")[0]
    bin2 = bins.split(",")[1]    
    
        
    if bin1 in bin_colors:
        red_value, green_value, blue_value = bin_colors[bin1]
    else:
      raise ValueError('setDouble - getBin() Returned unexpected value: '+ bin1)
        
    pi.set_PWM_dutycycle(stripOneRed, red_value)
    pi.set_PWM_dutycycle(stripOneGreen, green_value)
    pi.set_PWM_dutycycle(stripOneBlue, blue_value)

    if bin2 in bin_colors:
        red_value, green_value, blue_value = bin_colors[bin2]
    else:
      raise ValueError('setDouble - getBin() Returned unexpected value: '+ bin2)
        
    pi.set_PWM_dutycycle(stripTwoRed, red_value)
    pi.set_PWM_dutycycle(stripTwoGreen, green_value)
    pi.set_PWM_dutycycle(stripTwoBlue, blue_value)
    
def setup():  
    print ('Start setup')  
    #GPIO.setmode(GPIO.BOARD)         # use PHYSICAL GPIO Numbering        
    print ('End setup')  

def destroy():
    allOff()
    pi.stop()
    #GPIO.cleanup()  # Release GPIO resource          

def log_exception(e):
    with open("exceptions.log", "a") as f:
        f.write(f"{datetime.now()}: {e}\n")     

def get_api_response(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "Error: API returned status code {}".format(response.status_code)
    except requests.exceptions.RequestException as e:
        setError(e)
        return "Error: {}".format(str(e))

if __name__ == '__main__':     # Program entrance    
    setup()
                    
    try:
        while True:
            try:
                allOff()
                sleep(5)
                nextBins = get_api_response("https://biny.cerint.org/Biny?UPRN=906700527049")                                                
                if(len(nextBins.split(",")) == 1):
                    setSingle(nextBins)
                elif(len(nextBins.split(",")) == 2):
                    setDouble(nextBins)
                else:
                    raise ValueError('getBin() Returned unexpected value')
            except Exception as e:                                                
                setError(e)

            print ('Runned -pausing for 3h')  
            sleep(10800)
            pass
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        log_exception("Terminated By User")
        destroy()
