import urllib.request
import pigpio
import asyncio
from bs4 import BeautifulSoup

from time import sleep, strftime
from datetime import datetime
from pyppeteer import launch


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

def getBin():      
    print ('Start getBin')   
    url = "https://www.glasgow.gov.uk/forms/refuseandrecyclingcalendar/CollectionsCalendar.aspx?UPRN=906700527049"
    
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf8")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Application_Calendar") # find the table by id
    td = table.find("td", title=lambda t: t and "today" in t.lower()) # find the td by style
    imgs = td.find_all("img")
        
    tryNext = True
    while len(imgs) == 0:
        td = td.next_sibling
        if(td == None and tryNext):
            soup = click_a_tag_and_parse_updated_html(url)
            table = soup.find(id="Application_Calendar") # find the table by id
            td = table.find("td", class_=lambda t: t and "CalendarTodayDayStyle CalendarDayStyle" in t) # find the td by style 
            tryNext = False      

        imgs = td.find_all("img")

    words = ["greenBin", "blueBin", "brownBin", "purpleBin"] # list of words to check
    nextBin = ",".join([word for img in imgs for word in words if word in img["src"]]) # join the words that are in the src attribute of each image    
    print ('End getBin: ' + nextBin)  
    return nextBin


        

def click_a_tag_and_parse_updated_html(pageUrl):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(pageUrl)

    # Find the <a> tag with the specified title
    a_tag = await page.querySelector("a[title='Go to the next month']")

    # Click the <a> tag
    await a_tag.click()

    # Wait for the page to update (you may need to adjust the time depending on the page)
    await asyncio.sleep(3)

    # Get the updated HTML content
    updated_html = await page.content()

    # Parse the updated HTML content with BeautifulSoup
    soup = BeautifulSoup(updated_html, 'html.parser')

    # Close the browser
    await browser.close()

    return soup

def destroy():
    allOff()
    pi.stop()
    #GPIO.cleanup()  # Release GPIO resource          

def log_exception(e):
    with open("exceptions.log", "a") as f:
        f.write(f"{datetime.now()}: {e}\n")     

if __name__ == '__main__':     # Program entrance    
    setup()
                    
    try:
        while True:
            try:
                allOff()
                sleep(5)

                nextBins = getBin()
                if(len(nextBins.split(",")) == 1):
                    setSingle(nextBins)
                elif(len(nextBins.split(",")) == 2):
                    setDouble(nextBins)
                else:
                    raise ValueError('getBin() Returned unexpected value')
            except Exception as e:                
                setError(e)

            print ('Runned -pausing for 1h')  
            sleep(3600)
            pass
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        log_exception("Terminated By User")
        destroy()
