#!/bin/sh

# Reply texted message
from=$SMS_1_NUMBER
message=$SMS_1_TEXT
reply="Message Send $message"
echo "$reply" | gammu-smsd-inject TEXT "$from"

# Store to logs
log=/home/pi/createlabz-public-raspberry-pi/usb_modem_dongle_huwaei_e173/gammu/receive/
date >> $log
echo $from >> $log
echo $message >> $log