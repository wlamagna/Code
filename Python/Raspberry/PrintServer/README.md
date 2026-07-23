#### Print Server with Raspberry Pi 3b

## Download the image
### Burn it into the SD
dd if=2026-04-21-raspios-trixie-arm64-full.img of=/dev/sdb

### YUopu can enable ssh
raspi-config > Interface Options > SSH > Enable

apt-get install cups
systemctl start cups

cupsctl --remote-admin --remote-any --share-printers

edit /etc/cups/cupsd.conf

This section has to look like this, with Allow @LOCAL

```
<Location />
  # Allow shared printing and remote administration...
  Order allow,deny
  Allow @LOCAL
</Location>
<Location /admin>
  AuthType Default
  Require user @SYSTEM
  # Allow remote administration...
  Order allow,deny
  Allow @LOCAL
</Location>
```

usermod --append --groups lpadmin <your user, could be pi also>
systemctl restart cups

### Now the printer can be managed with the browser
##Enable the web interface:
```
cupsctl WebInterface=yes
```
### Access with a browser:
```
Http://<ip>:631
```
### I have an Epson printer and the default drivers were not useful.
### There is this gutenprint package which is incredible recomendable and saved me !
cups-pdf printer-driver-gutenprint

### If the screen anoys to be on all the time:
```
wlr-randr --output DSI-1 --on
```

### To add it to a windows machine you select the network printer and search for http://ip/printers/EPSON_L210_Series for example
or the printer in your case

### Now one problem that i have to resolve is that the 7inch screen is inverted, i do not rememebr the cause but it is a known issue
### At the time of writing this the solution is:
```
/boot/firmware/cmdline.txt
# Add this to the line:
video=DSI-1:800x480M,rotate=180
```

### I added these two lines to rotate the mouse selection too:
```
/boot/firmware/config.txt
dtoverlay=rpi-ft5406
lcd_rotate=2
```

