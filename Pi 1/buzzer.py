#Libraries
import RPi.GPIO as GPIO
from time import sleep
#Disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BCM)
#Set buzzer - pin 16 as output
buzzer=23
GPIO.setup(buzzer,GPIO.OUT)
#Run forever loop

while True:
	file1 = open("buzzerData.txt","r")
	kt = file1.read()
	if kt == "1":
		GPIO.output(buzzer,GPIO.HIGH)
		print ("Beep")
		sleep(0.5) # Delay in seconds
	elif kt == "0":
		GPIO.output(buzzer,GPIO.LOW)
		print ("No Beep")
		sleep(0.5)
	#file1.close()
