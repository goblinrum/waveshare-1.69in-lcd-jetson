# Running 1.69in Waveshare LCD (ST7789v2) on Jetson Nano

You may need to install these packages:

```
Jetson.GPIO
adafruit-circuitpython-busdevice
spidev
adafruit-blinka-displayio
adafruit-circuitpython-rgb-display
adafruit-circuitpython-st7789
Pillow
```

You also will need to enable `spi1` and `spi3` on `jetson-io`. Launch that by running 
```
sudo /opt/nvidia/jetson-io/jetson-io.py
```
and then select "Configure pins manually" for the 40-pin header. Once you've configured it, make sure to reboot to save your changes to the device tree.

Make sure to load the `spidev` driver by running 
```
sudo modprobe spidev
```

Run the test program by running
```
python3 run.py
```

