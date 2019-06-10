import Adafruit_WS2801
try:
    import RPi.GPIO as GPIO
except:
    import FakeRPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import time
import colorsys
import random

class Effects():
    def __init__(self, vars):
        self.vars = vars
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.vars.PIXEL_COUNT, spi=SPI.SpiDev(self.vars.SPI_PORT, self.vars.SPI_DEVICE), gpio=GPIO)
    
    def cleaning(self):
        self.pixels.clear()
        self.pixels.show()
        self.vars.running_effect = True

    def name_to_rgb(self, colorname):
            #its rbg
        if colorname == "blue":
            return [0, 255 , 0]
        elif colorname == "red":
            return [255 , 0 , 0]
        elif colorname == "green":
            return [0, 0, 255]
        elif colorname == "white":
            return [255,255,255]
        elif colorname == "purple":
            return [255,255, 0]
        elif colorname == "yellow":
            return [255, 0, 255]
        elif colorname == "cyan":
            return [0, 255, 255]
        elif colorname == "clear":
            return [0, 0, 0]
        else:
            return [0 , 0 , 0]

    def maximizer(self, rgblist):
        #Attribute 1 just in case
        multiplier = 1

        #Find the biggest one and get multiplier to maximize
        if rgblist[0] > rgblist[1] and rgblist[0] > rgblist[2]:
            multiplier = 255/rgblist[0]
        if rgblist[1] > rgblist[0] and rgblist[1] > rgblist[2]:
            multiplier = 255/rgblist[1]
        if rgblist[2] > rgblist[0] and rgblist[2] > rgblist[1]:
            multiplier = 255/rgblist[2]

        #return floats
        return [rgblist[0]*multiplier, rgblist[1]*multiplier, rgblist[2]*multiplier]

    def calibration(self, rgblist, maxer= True):
        #Multiply for calibration
        templist = []
        rgblist[0] = rgblist[0]*self.vars.redcal
        rgblist[1] = rgblist[1]*self.vars.bluecal
        rgblist[2] = rgblist[2]*self.vars.greencal
        #set colour sequence RGB, RBG...
        for let in self.vars.RGB_ORDER:
            #Get Letter by letter and order.
            #RED
            if let == "R":
                templist.append(rgblist[0])
            #BLUE
            elif let == "B":
                templist.append(rgblist[1])
            #Green
            else:
                templist.append(rgblist[2])

        rgblist = templist

        #Maximize colors to 255 in the biggest one if required (self.maximize)
        if maxer:
            if self.vars.maximize:
                rgblist = self.maximizer(rgblist)

        #Get luminosity and/or convert to int
        if self.vars.luminosity < 1:
            for i in range(3):
                rgblist[i] = int(rgblist[i]*self.vars.luminosity)
        else:
            for i in range(3):
                rgblist[i] = int(rgblist[i])


        return rgblist

    def static_effect(self):
        # Unique Colour
        while self.vars.running_effect:
            rgbcolor = self.name_to_rgb(self.vars.color)
            rgbcolor = self.calibration(rgbcolor)
            #Refresh color everytime to avoid interferences in some situations and descoloration
            for p in range(self.vars.PIXEL_COUNT):
                self.pixels.set_pixel_rgb(p, rgbcolor[0], rgbcolor[1], rgbcolor[2])
            self.pixels.show()
            time.sleep(0.1)


    def rainbow_effect(self):
        #How much it increses everytime. Calculated to make it efficient
        step = 0.0013
        while self.vars.running_effect:
            #For that divides 1 by steps to change one color at the time
            for c in range(int(1/step)):
                #Convert HSV( easier to use) to RGB
                hsv_rgb = colorsys.hsv_to_rgb(c*step, 1, 1 )
                #Converts 1 to 255
                rgbcolor= [hsv_rgb[0]*255, hsv_rgb[2]*255, hsv_rgb[1]*255]
                #Calibrate color (checks if maximize or not, and multiplies by calibration values)
                rgbcolor = self.calibration(rgbcolor)
                #Apply to each pixel
                for p in range(self.vars.PIXEL_COUNT):
                    self.pixels.set_pixel_rgb(p, rgbcolor[0], rgbcolor[1], rgbcolor[2])
                self.pixels.show()
                time.sleep(0.1)
                if self.vars.running_effect == False:
                    break

    def random_group_effect(self):
        
        listapixels = []
        #To avoid some colours being more powerfull than others and overlap them
        maxer = False
        #Create a groups of number of sequences
        for i in range(int(self.vars.PIXEL_COUNT/self.vars.sequences)):
            listapixels.append(-2)

        

        ###### TODO 
        #
        #   The script is adding without limits so all ranges can be on all the time 5 groups 5 different colours possible 
        #   Must reduce the amount of light at the same time, because otherwise wil be a mesh of 
        #   lights and only white would be seen. 
        #
        #Test code procede with care!!!!

        number_of_groups = self.vars.PIXEL_COUNT/self.vars.sequences
        middle_of_groups = round(number_of_groups/2)
        while len(listapixels)>middle_of_groups:
            del listapixels[0]



        while self.vars.running_effect == True:
            #Get pixel
            rled = random.randint(0, self.vars.PIXEL_COUNT/self.vars.sequences - 1 )
            #Get a Random RGB color from a HSV
            rcolor = colorsys.hsv_to_rgb(random.random(), 1, 1)
            rgbcolor = []
            #Get 255 values of colour
            for c in rcolor:
                rgbcolor.append(c*255)
            rgbcolor = self.calibration(rgbcolor, maxer)

            #Decrease intensity
            if rled in listapixels:
                #dled = dimm led
                dled = rled
                #remove that led from list to add it later
                listapixels.remove(rled)
                listapixels.append(rled)
            else:
                #give oldest led value to dled
                dled = listapixels[0]
                #remove oldest led
                del listapixels[0]
                listapixels.append(rled)
            
            #Dimm

            try:
                for l in range(80,0,-1):
                    ll = 80/l
                    rgbtodim = self.pixels.get_pixel_rgb( dled * self.vars.sequences )
                    for i in range(self.vars.sequences):
                        self.pixels.set_pixel_rgb(dled * self.vars.sequences + i, int(rgbtodim[0]/ll), int(rgbtodim[1]/ll), int(rgbtodim[2]/ll))
                        self.pixels.show()
                    time.sleep(0.05)
                for i in range(self.vars.sequences):
                    self.pixels.set_pixel_rgb( dled * self.vars.sequences +i, 0, 0, 0)
            except:
                pass
            
            #light
            for l in range(1,81):
                ll = 80/l
                for i in range(self.vars.sequences):
                    self.pixels.set_pixel_rgb(rled * self.vars.sequences + i, int(rgbcolor[0]/ll), int(rgbcolor[1]/ll), int(rgbcolor[2]/ll))
                self.pixels.show()
                time.sleep(0.05)
            #Wait
            for i in range(10):
                if self.vars.running_effect == False:
                    break
                else:
                    time.sleep(0.5)

    def rainbow_swirl(self):
        #Because some colours would be brighter than others
        maxer = False
        step = 1/self.vars.PIXEL_COUNT

        for p in range(self.vars.PIXEL_COUNT):
            ncolor = colorsys.hsv_to_rgb(step*p, 1, 1)
            rgbcolor = []
            #Get 255 values of colour
            for c in ncolor:
                rgbcolor.append(c*255)

            rgbcolor = self.calibration(rgbcolor, maxer)
            
            self.pixels.set_pixel_rgb(p, int(rgbcolor[0]), int(rgbcolor[1]), int(rgbcolor[2]))

            self.pixels.show()
        while self.vars.running_effect:
            for c in range(self.vars.PIXEL_COUNT):
                for p in range(self.vars.PIXEL_COUNT):
                    rgbtogive = self.pixels.get_pixel_rgb((p+1)%self.vars.PIXEL_COUNT)
                    self.pixels.set_pixel_rgb(p, rgbtogive[0], rgbtogive[1], rgbtogive[2])
                self.pixels.show()

                for i in range(2):
                    if self.vars.running_effect == False:
                        break
                    else:
                        time.sleep(0.05)