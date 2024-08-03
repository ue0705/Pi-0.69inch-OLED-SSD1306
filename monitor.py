import time
import board
import busio
#xxx, import digitalio
import psutil as PS #xxx, 
from datetime import datetime #xxx, 

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess


# Define the Reset Pin
#xxx, oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C) #xxx, , reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = oled.width
height = oled.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# swap memory/disk space display
dis_flag = 0
dis_cnt = 0
        
# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# Icons website: https://icons8.com/line-awesome
font = ImageFont.truetype('PixelOperator.ttf', 16)
icon_font= ImageFont.truetype('lineawesome-webfont.ttf', 18)

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw a filled white rectangle as the background
    draw.rectangle((0,0,width,height), outline=255, fill=255)

    # Define border size for an inner rectangle
    BORDER = 1
    # Draw a smaller black rectangle inside the larger one
    draw.rectangle(
        (BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
        outline=0,
        fill=0,
    )

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell = True )
    now = datetime.now()
    TIME = now.strftime("%H:%M:%S")

    #cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
    #xxx, CPU = subprocess.check_output(cmd, shell = True )
    CPU = "{:.1f}%".format(round(PS.cpu_percent(),1))

    cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"    
    MemUsage = subprocess.check_output(cmd, shell = True )
    
    cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
    Disk = subprocess.check_output(cmd, shell = True )
    
    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    Temperature = subprocess.check_output(cmd, shell = True )

    # Icons, x=0,65; y=5,25,45
    # Icon clock=61463, stopwatch=62194
    draw.text((x, top+5), chr(62194),  font=icon_font, fill=255)
    # Icon battery
    draw.text((x+70, top+5), chr(62016),  font=icon_font, fill=255)
    # Icon cpu(microchip)=62171, laptop=61705, fire-alt=63460
    draw.text((x, top+25), chr(61705), font=icon_font, fill=255)
    if dis_flag == 0:  
        # Icon temperature(thermometer)=62609, fire-alt=63460
        draw.text((x+70, top+25), chr(63460),  font=icon_font, fill=255)
    elif dis_flag == 1:
        # Icon memory
        draw.text((x+70, top+25), chr(62776),  font=icon_font, fill=255)
    else:
        # Icon disk(sd-card)
        draw.text((x+70, top+25), chr(63426),  font=icon_font, fill=255)
    # Icon wifi=61931, broadcast-tower=62745
    draw.text((x, top+45), chr(62745),  font=icon_font, fill=255)
    # Icon microphone
    draw.text((x+110, top+45), chr(61744),  font=icon_font, fill=255)

    # Text
    # Text Time
    draw.text((x+18, top+5), str(TIME),  font=font, fill=255)
    # Text battery
    draw.text((x+89, top+5), "85.8%",  font=font, fill=255)
    # Text cpu usage
    draw.text((x+20, top+25) , CPU, font=font, fill=255) #xxx, str(CPU,'utf-8')
    if dis_flag == 0: 
        # Text temperature
        draw.text((x+87, top+25), str(Temperature,'utf-8'),  font=font, fill=255)
    elif dis_flag == 1:
        # Text memory usage
        draw.text((x+87, top+25), str(MemUsage,'utf-8'),  font=font, fill=255)
    else:
        # Text Disk usage
        draw.text((x+87, top+25), str(Disk,'utf-8'),  font=font, fill=255)
    # Text IP address
    draw.text((x+19, top+45), str(IP,'utf-8'),  font=font, fill=255)

    # every 3sec add flag onces
    dis_cnt += 1
    if dis_cnt == 3:
        dis_flag = (dis_flag + 1) % 3
        dis_cnt = 0
    
   # Display image.
    oled.image(image)
    oled.show()
    time.sleep(LOOPTIME)
