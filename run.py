import spidev
import logging
import numpy as np
import time
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont

class RaspberryPi:
    def __init__(self,spi, spi_freq,rst, dc, bl, bl_freq=1000,i2c=None,i2c_freq=100000):
        import Jetson.GPIO as GPIO      
        self.np=np
        self.RST_PIN= rst
        self.DC_PIN = dc
        self.BL_PIN = bl
        self.SPEED  =spi_freq
        self.BL_freq=bl_freq
        self.GPIO = GPIO
        #self.GPIO.cleanup()
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.RST_PIN,   self.GPIO.OUT)
        self.GPIO.setup(self.DC_PIN,    self.GPIO.OUT)
        self.GPIO.setup(self.BL_PIN,    self.GPIO.OUT)
        self.GPIO.output(self.BL_PIN,   self.GPIO.HIGH)        
        #Initialize SPI
        self.SPI = spi
        if self.SPI!=None :
            self.SPI.max_speed_hz = spi_freq
            self.SPI.mode = 0b00

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(pin)

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        if self.SPI!=None :
            self.SPI.writebytes(data)
    def bl_DutyCycle(self, duty):
        self._pwm.ChangeDutyCycle(duty)
        
    def bl_Frequency(self,freq):
        self._pwm.ChangeFrequency(freq)
           
    def module_init(self):
        self.GPIO.setup(self.RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.DC_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.BL_PIN, self.GPIO.OUT)
        self._pwm=self.GPIO.PWM(self.BL_PIN,self.BL_freq)
        self._pwm.start(100)
        if self.SPI!=None :
            self.SPI.max_speed_hz = self.SPEED        
            self.SPI.mode = 0b00     
        return 0

    def module_exit(self):
        logging.debug("spi end")
        if self.SPI!=None :
            self.SPI.close()
        
        logging.debug("gpio cleanup...")
        self.GPIO.output(self.RST_PIN, 1)
        self.GPIO.output(self.DC_PIN, 0)        
        self._pwm.stop()
        time.sleep(0.001)
        self.GPIO.output(self.BL_PIN, 1)
        #self.GPIO.cleanup()



'''
if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    implementation = RaspberryPi()

for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))
'''

### END OF FILE ###


class LCD_1inch69(RaspberryPi):
    width = 240
    height = 280 
    
    def command(self, cmd):
        self.digital_write(self.DC_PIN, False)
        self.spi_writebyte([cmd])   
        
    def data(self, val):
        self.digital_write(self.DC_PIN, True)
        self.spi_writebyte([val])   
        
    def reset(self):
        """Reset the display"""
        self.digital_write(self.RST_PIN,True)
        time.sleep(0.01)
        self.digital_write(self.RST_PIN,False)
        time.sleep(0.01)
        self.digital_write(self.RST_PIN,True)
        time.sleep(0.01)
        
    def Init(self):
        """Initialize dispaly"""  
        self.module_init()
        self.reset()

        self.command(0x36)
        self.data(0x00)

        self.command(0x3A) 
        self.data(0x05)

        self.command(0xB2)
        self.data(0x0B)
        self.data(0x0B)
        self.data(0x00)
        self.data(0x33)
        self.data(0x35)

        self.command(0xB7)
        self.data(0x11) 

        self.command(0xBB)
        self.data(0x35)

        self.command(0xC0)
        self.data(0x2C)

        self.command(0xC2)
        self.data(0x01)

        self.command(0xC3)
        self.data(0x0D)   

        self.command(0xC4)
        self.data(0x20) # VDV, 0x20: 0V

        self.command(0xC6)
        self.data(0x13) # 0x13: 60Hz 

        self.command(0xD0)
        self.data(0xA4)
        self.data(0xA1)

        self.command(0xD6)
        self.data(0xA1)

        self.command(0xE0)
        self.data(0xF0)
        self.data(0x06)
        self.data(0x0B)
        self.data(0x0A)
        self.data(0x09)
        self.data(0x26)
        self.data(0x29)
        self.data(0x33)
        self.data(0x41)
        self.data(0x18)
        self.data(0x16)
        self.data(0x15)
        self.data(0x29)
        self.data(0x2D)

        self.command(0xE1)
        self.data(0xF0)
        self.data(0x04)
        self.data(0x08)
        self.data(0x08)
        self.data(0x07)
        self.data(0x03)
        self.data(0x28)
        self.data(0x32)
        self.data(0x40)
        self.data(0x3B)
        self.data(0x19)
        self.data(0x18)
        self.data(0x2A)
        self.data(0x2E)
        
        self.command(0xE4)
        self.data(0x25)
        self.data(0x00)
        self.data(0x00)

        self.command(0x21)

        self.command(0x11)

        time.sleep(0.1)

        self.command(0x29)
  
    def SetWindows(self, Xstart, Ystart, Xend, Yend, horizontal = 0):
        if horizontal:  
            #set the X coordinates
            self.command(0x2A)
            self.data(Xstart+20>>8)         #Set the horizontal starting point to the high octet
            self.data(Xstart+20 & 0xff)     #Set the horizontal starting point to the low octet
            self.data(Xend+20-1>>8)         #Set the horizontal end to the high octet
            self.data((Xend+20-1) & 0xff)   #Set the horizontal end to the low octet 
            #set the Y coordinates
            self.command(0x2B)
            self.data(Ystart>>8)
            self.data((Ystart & 0xff))
            self.data(Yend-1>>8)
            self.data((Yend-1) & 0xff)
            self.command(0x2C)
        else:
            #set the X coordinates
            self.command(0x2A)
            self.data(Xstart>>8)        #Set the horizontal starting point to the high octet
            self.data(Xstart & 0xff)    #Set the horizontal starting point to the low octet
            self.data(Xend-1>>8)        #Set the horizontal end to the high octet
            self.data((Xend-1) & 0xff)  #Set the horizontal end to the low octet 
            #set the Y coordinates
            self.command(0x2B)
            self.data(Ystart+20>>8)
            self.data((Ystart+20 & 0xff))
            self.data(Yend+20-1>>8)
            self.data((Yend+20-1) & 0xff)
            self.command(0x2C)    


    def ShowImage(self, Image):
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""
        imwidth, imheight = Image.size
        if imwidth == self.height and imheight ==  self.width:
            print("Landscape screen")
            img = self.np.asarray(Image)
            pix = self.np.zeros((self.width, self.height,2), dtype = self.np.uint8)
            #RGB888 >> RGB565
            pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
            pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0), self.np.right_shift(img[...,[2]],3))
            pix = pix.flatten().tolist()
            
            self.command(0x36)
            self.data(0x70)
            self.SetWindows(0, 0, self.height,self.width, 1)
            self.digital_write(self.DC_PIN,True)
            for i in range(0,len(pix),4096):
                self.spi_writebyte(pix[i:i+4096])
        else :
            print("Portrait screen")
            img = self.np.asarray(Image)
            pix = self.np.zeros((imheight,imwidth , 2), dtype = self.np.uint8)
            
            pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
            pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0), self.np.right_shift(img[...,[2]],3))
            pix = pix.flatten().tolist()
            
            self.command(0x36)
            self.data(0x00)
            self.SetWindows(0, 0, self.width, self.height, 0)
            self.digital_write(self.DC_PIN,True)
        for i in range(0, len(pix), 4096):
            self.spi_writebyte(pix[i: i+4096])
        

    def clear(self):
        """Clear contents of image buffer"""
        _buffer = [0xff] * (self.width*self.height*2)
        self.SetWindows(0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN,True)
        for i in range(0, len(_buffer), 4096):
            self.spi_writebyte(_buffer[i: i+4096])
        
# Raspberry Pi pin configuration:
RST = 6
DC = 25
BL = 12
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG)

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    disp = LCD_1inch69(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    # disp2 = LCD_1inch69(spi=SPI.SpiDev(bus, 1), spi_freq=10000000, rst=RST, dc)
    # disp = LCD_1inch69()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)

    Font1 = ImageFont.truetype("./Font/Font01.ttf", 25)
    Font2 = ImageFont.truetype("./Font/Font01.ttf", 35)
    Font3 = ImageFont.truetype("./Font/Font02.ttf", 32)

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width, disp.height ), "WHITE")
    draw = ImageDraw.Draw(image1)
    disp.ShowImage(image1)
    time.sleep(2)

    logging.info("draw point")
    draw.rectangle((25, 10, 26, 11), fill = "BLACK")
    draw.rectangle((25, 25, 27, 27), fill = "BLACK")
    draw.rectangle((25, 40, 28, 43), fill = "BLACK")
    draw.rectangle((25, 55, 29, 59), fill = "BLACK")
    disp.ShowImage(image1)
    time.sleep(2)

    logging.info("draw rectangle")
    draw.rectangle([(40, 10), (90, 60)], fill = "WHITE", outline="BLUE")
    draw.rectangle([(105, 10), (150, 60)], fill = "BLUE")
    disp.ShowImage(image1)
    time.sleep(2)

    logging.info("draw line")
    draw.line([(40, 10), (90, 60)], fill = "RED", width = 1)
    draw.line([(90, 10), (40, 60)], fill = "RED", width = 1)
    draw.line([(130, 65), (130, 115)], fill = "RED", width = 1)
    draw.line([(105, 90), (155, 90)], fill = "RED", width = 1)
    disp.ShowImage(image1)
    time.sleep(2)

    logging.info("draw circle")
    draw.arc((105, 65, 155, 115), 0, 360, fill =(0, 255, 0))
    draw.ellipse((40, 65, 90, 115), fill = (0, 255, 0))
    disp.ShowImage(image1)
    time.sleep(2)

    logging.info("draw text")
    draw.rectangle([(20, 120), (160, 153)], fill = "BLUE")
    draw.text((25, 120), 'Hello world', fill = "RED", font=Font1)
    draw.rectangle([(20,155), (192, 195)], fill = "RED")
    draw.text((21, 155), 'WaveShare', fill = "WHITE", font=Font2)
    draw.text((25, 190), '1234567890', fill = "GREEN", font=Font3)
    text= u"微雪电子"
    draw.text((25, 230),text, fill = "BLUE", font=Font3)
    image1=image1.rotate(0)
    disp.ShowImage(image1)
    time.sleep(2)
    
    image2 = Image.new("RGB", (disp.height,disp.width ), "WHITE")
    draw = ImageDraw.Draw(image2)
    draw.text((60, 2), u"题龙阳县青草湖", fill = 808000, font=Font3)
    draw.text((100, 42), u"元  唐珙", fill = 808080, font=Font3)
    draw.text((60, 82), u"西风吹老洞庭波，", fill = "BLUE", font=Font3)
    draw.text((60, 122), u"一夜湘君白发多。", fill = "RED", font=Font3)
    draw.text((60, 162), u"醉后不知天在水，", fill = "GREEN", font=Font3)
    draw.text((60, 202), u"满船清梦压星河。", fill = "BLACK", font=Font3)
    image2=image2.rotate(0)
    disp.ShowImage(image2)
    time.sleep(2)   
    
    logging.info("show image")
    ImagePath = ["./pic/LCD_1inch69_4.jpg", "./pic/LCD_1inch69_5.jpg", "./pic/LCD_1inch69_6.jpg"]
    for i in range(0, 3):
        image = Image.open(ImagePath[i])	
        # image = image.rotate(0)
        disp.ShowImage(image)
        time.sleep(2)
    disp.module_exit()
    logging.info("quit:")
    
except IOError as e:
    logging.info(e)    
    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()