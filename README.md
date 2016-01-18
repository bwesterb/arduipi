Example of domotics using Arduino connected to rPi
--------------------------------------------------

Using an breadboard connected to an [Arduino](https://www.arduino.cc)
connected to a [Raspberry Pi](https://www.raspberrypi.org),

 * I can switch my lights (which are connected
   with [KlikAanKlikUit](http://www.klikaanklikuit.nl) *and*
 * read the temperature

via a webinterface.

This is all tailored to the hardware I have, but hopefully it is also
helpful as an example.

Contents

 * In the `/arduino` folder you can find the code that runs on the arduino.
   It listens on the serial port for commands from the rPi, which are
   send by the web-interface.
 * The `/webapp` folder is the home of the webapplication written in
   Python with [Flask](http://flask.pocoo.org).
