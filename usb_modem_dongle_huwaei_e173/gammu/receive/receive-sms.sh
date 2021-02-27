#!/bin/sh

# Send texted message
from=$SMS_1_NUMBER
message=$SMS_1_TEXT
reply="Message Send $message"

echo "$reply" | gammu-smsd-inject TEXT "$from"

# Store to logs
log=/home/pi/bin/sms/log_sms.txt
date >> $log
echo $from >> $log
echo $message >> $log