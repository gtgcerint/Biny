# Biny

Are you tierd of forgetting what bin you need to put out every week? Biny is the project for you. Bellow you will find steps, guides and links to materials for creating a small discrete bin that will glow with the colour of the appropriate bin. 

## Materials
Here is the list of materials you will need. You are not limited to these exact list but if you are not comfortable with electronics and this is your first project keep to the list for optimal results.

### Tools
Soldering Iron / Solder
https://www.amazon.co.uk/Adjustable-Temperature-Soldering-Iron-Desoldering-Screwdriver/dp/B077GB7CSZ/ref=sr_1_3 

Wire cutter
https://www.amazon.co.uk/dp/B0777F3CNC 

### Electronics
Power Jacks:
https://www.amazon.co.uk/dp/B0106GV3SU?psc=1&ref=ppx_yo2ov_dt_b_product_details

Mosfets:
https://www.amazon.co.uk/dp/B0893WBH6H 

Led Strips:
https://www.amazon.co.uk/dp/B0B87B6BYT 

Raspberry Pi Zero W:
https://www.raspberrypi.com/products/raspberry-pi-zero-w/

Step Down Converter:
https://www.amazon.co.uk/dp/B0BJQ2DF5R 

Cables / Wires:
https://www.amazon.co.uk/AZDelivery-MB-102-Breadboard-Kit/dp/B07K8PVKBP/ref=sr_1_9 
https://www.amazon.co.uk/AZDelivery-MB-102-Breadboard-Kit/dp/B07KYHBVR7/ref=sr_1_4 

Connectors:
https://www.amazon.co.uk/ZFYQ-Connectors-Connector-Terminal-Stranded/dp/B093BK9DFS/ref=sr_1_8

### Optional
Soldering Station:
https://www.amazon.co.uk/YIHUA-926LED-IV-EVO-110W-Soldering-Station-90-480°C-Soldering-Kit-Extra-Soldering-Tips-Lead-Free-Solder-Wire/dp/B0BJ21NRSY/

Solder:
https://www.amazon.co.uk/Solder-Sn99-3-Electrical-Soldering-Weight/dp/B07RD9GG52/ref=pd_bxgy_sccl_1/258-6808322-0682658

Flux:
https://www.amazon.co.uk/Tinner-Solder-Paste-Clean-Formulation/dp/B077T15STS/ref=pd_bxgy_sccl_2/258-6808322-0682658


## Connection
!!Attention!! we are going to be using the power supply that comes with the ledstrips to power both the RasPi and the strips. This is not a good idea. You should use a different power supply for each.

Lets start with the mosfets. 
Looking at the (IRLZ34N) MOSFET from the front, then:
  First pin from the left is the Gate pin
  Second pin is the Drain pin
  Third pin is the Source pin

Since in Glasgow you may have up to 2 bins to be picked up in a day you will need 3 mosfets and 1 strip per bin. So get 6 mosfets and solder a black abled to the far right pin (ground).
![image](https://user-images.githubusercontent.com/63113549/226122561-6bd39d21-73c8-4abd-bef7-2ef9d3e33c21.png)

Next connect a wire to the middle pin. The midle pin will be then connected to the strip so choose a color for each R/G/B.
"Photos will follow soon"

Last with do the same to the left pin. Those will be connected to the RasPi so keep the color sceme the same. 
"Photos will follow soon"

And now for the tricky bit. From the big spool of the LED strip cut 2 pieces. You then need to Connect the cables from the midle pin of each mosfet to each R, G & B pad on the strip. The last pad 24v+ should also get a cable soldered as it will be then connected to the power. 
"Photos will follow soon"

Do the same again for the other 3 mosfets and strip.

Now onto the RasPi. Pick 6 pins on the pi and connect the left pin of each mosfet to them. You shound be carefull not to connect the ground of the mosfets to them.
"Photos will follow soon"

Now twist together the grounds of the mosfets in pairs of 3 and use a 5 port wire connector to clamp them in.
"Photos will follow soon"

Use another black cable to connect one of the ground pins on the RasPi to the 5 port wire connector
"Photos will follow soon"

Now also connect the black cable from the step down psu to the 5 port wire connector
"Photos will follow soon"

Time for the power cables. 
Twist together the 24v+ cable from the strips. 
"Photos will follow soon"

Get a 3 port wire connector and use one of the ports for the twisted pair form the strips
"Photos will follow soon"

Connect the red cable from the step down psu to the 3 pin wire connector
"Photos will follow soon"

Now to the dangerous bit. 
Locate the compatible power supply jack and use the 2 ports to connect a red and black cable to the (+) & (-) ports respectively
"Photos will follow soon"

Now the 2 wire connectos should have only one port free. connect the black wire from the power supply to the 5 port one and the red wire from the power supply to the 3port one
"Photos will follow soon"

## RasPi Install and Config.
Install the raspi os lite on a SD card. 
Insert it to you RasPi and connect it to a power supply only for the RasPi until you get it ready. 
Once booter connect with putty and:
1) Update / Upgrade
2) Install pigpio http://abyz.me.uk/rpi/pigpio/download.html

## Have the script and pingpi start on reboot:
connect to raspi and run: crontab -e 
and on the end add:
@reboot sudo pigpiod
@reboot sudo python3 /home/biny/Projects/Biny/Main.py <- path to the python file








