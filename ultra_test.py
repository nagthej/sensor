import time
import paho.mqtt.client as paho
import ultra_test
import subprocess 
import os
import RPi.GPIO as GPIO                    #Import GPIO library
                                            #Import time library
GPIO.setmode(GPIO.BOARD)                     #Set GPIO pin numbering 
LED = 12
TRIG = 10                                  #Associate pin 23 to TRIG
ECHO = 24 
print "Distance measurement in progress"
GPIO.setup(LED,GPIO.OUT)                  #Set pin as GPIO out

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in
                                 #Associate pin 24 to ECHO
def read_sensor(): 
         GPIO.output(LED, True) 
         GPIO.output(TRIG, False)                 #Set TRIG as LOW
         time.sleep(1)
                               #Delay of 2 seconds

         GPIO.output(TRIG, True)
                                            #Set TRIG as HIGH
         time.sleep(0.00001)                      #Delay of 0.00001 seconds
         GPIO.output(TRIG, False)                 #Set TRIG as LOW

         while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
                 pulse_start = time.time()
                  #Saves the last known time of LOW pulse

         while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
                 pulse_end = time.time()                #Saves the last known time of HIGH pulse 

         pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

         distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
         distance = round(distance, 2)            #Round to two decimal points

         if distance > 2 and distance < 400:      #Check whether the distance is within range
                 print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
         else:
                 print "Out Of Range"                   #display out of range
         GPIO.output(LED, False) 
         return distance-0.5




broker="ec2-18-221-47-29.us-east-2.compute.amazonaws.com"
#define callback
def on_message(client, userdata, message):
	time.sleep(1)
	print("Received URL to Dockerhub =",str(message.payload.decode("utf-8")))
        url=str(message.payload.decode("utf-8"))
        #subprocess.call("docker pull url",shell=True)
        subprocess.call("docker stop $(docker ps -a -q)",shell=True)
        subprocess.call("docker rm $(docker ps -a -q)",shell=True)
        subprocess.call("docker image rm $(docker image ls -a -q)",shell=True)
        subprocess.call("docker run -t --privileged url",shell=True)
        

              
 # subprocess.call("docker run",shell=True)


client= paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
######Bind function to callback
client.on_message=on_message
print("connecting to broker ",broker)
client.connect(broker) #connect
client.loop_start() #start loop to process received messages
client.subscribe("URL_hub") #subscribe
time.sleep(2)
while True: 
        data=read_sensor()
	client.publish("sensor_data",str(data)) #publish
        time.sleep(1)

client.loop_forever()
