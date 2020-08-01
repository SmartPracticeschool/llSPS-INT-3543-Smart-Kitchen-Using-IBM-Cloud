import time
import sys
import ibmiotf.application
import ibmiotf.device
import requests
url = "https://www.fast2sms.com/dev/bulk"

#ibm credentials
organisation="qpqk20"
deviceType="raspberrypi"
deviceId="123456"
authMethod="token"
authToken="12345678"

def myCommandCallback(cmd):
    print("Command received : %s" % cmd.data)

try:
    deviceOptions={"org":organisation,"type":deviceType,"id": deviceId,"auth-method":authMethod,"auth-token":authToken}
    deviceCli=ibmiotf.device.Client(deviceOptions)
except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()
    
deviceCli.connect()

#assuming capacity of jar to be 2000gm and weight of gas in cylinder to be 15 kg
jar_weight=2000
cylinder_weight=15
#there is no leakage is the beginning
fan="OFF"
leak="OFF"
leakage=0


cylinder_empty=0
jar_empty=0

while True:
    #cylinder is used 0.05 kg in per usage
    cylinder_weight=cylinder_weight-0.05
    #jar is used 15 gm in per usage
    jar_weight=jar_weight-15

    if (cylinder_weight>0 and cylinder_weight<=5):
        cylinder_status="LOW"
    elif(cylinder_weight>5 and cylinder_weight<=10):
        cylinder_status="MODERATE"
    elif (cylinder_weight>10 and cylinder_weight<=15):
        cylinder_status="HIGH"
    else:
        cylinder_weight=0
        cylinder_status="EMPTY!!"

        if (cylinder_empty==0):
            #SMS is send to user
            r=requests.get('https://www.fast2sms.com/dev/bulk?authorization=jskXG7URxi8oIeWLKD9nYVNMaHCtmgZqvfdr4JO2lbE6zTS5pAFv93mURQGb2tWV8gkTdAl4osLpOXIC&sender_id=FSTSMS&message=The%20cylinder%20is%20empty&language=english&route=p&numbers=8130383672')
            print(r.status_code)
            print("the cylinder is empty")
            cylinder_empty=1  


    if(jar_weight<300 and jar_weight>=0):
        jar_status="LOW"
    elif (jar_weight>=300 and jar_weight<1100):
        jar_status="MODERATE"
    elif (jar_weight>=1100 and jar_weight<=2000):
        jar_status="HIGH"
    else:
        jar_weight=0
        jar_status="EMPTY!!"
        if (jar_empty==0):
            print("The jar is empty!!")
            #SMS is send to user
            r=requests.get('https://www.fast2sms.com/dev/bulk?authorization=jskXG7URxi8oIeWLKD9nYVNMaHCtmgZqvfdr4JO2lbE6zTS5pAFv93mURQGb2tWV8gkTdAl4osLpOXIC&sender_id=FSTSMS&message=The%20jar%20is%20empty&language=english&route=p&numbers=8130383672')
            print(r.status_code) 
            jar_empty=1

            
    #leakage is increasing
    leakage=leakage+1
    if(leakage==100):
        print(" ALERT!!! GAS LEAKAGE in your kitchen. ")
        #SMS is send to user
        r=requests.get('https://www.fast2sms.com/dev/bulk?authorization=jskXG7URxi8oIeWLKD9nYVNMaHCtmgZqvfdr4JO2lbE6zTS5pAFv93mURQGb2tWV8gkTdAl4osLpOXIC&sender_id=FSTSMS&message=There%20is%20gas%20leakage%20Check%20NOW&language=english&route=p&numbers=8130383672')
        print(r.status_code)
        fan="ON"
        leak="ON"

        
    data={ 'cylinder_weight' :round(cylinder_weight,2), 'cylinder_status': cylinder_status, 'jar_weight':jar_weight, 'jar_status':jar_status, 'leak': leak, 'fan':fan}

    def myOnPublishCallback():
        print("published cylinder_weight= %s" %round(cylinder_weight,2), "cylinder_status= %s" %cylinder_status , "jar_weight= %s" %jar_weight,"jar_Status= %s" %jar_status,"leakage= %s" %leak,"fan= %s" %fan)
    success =deviceCli.publishEvent("Smart Kitchen","json",data,qos=0,on_publish=myOnPublishCallback)

    if not success:
        print("not coonected to IoTF")
        time.sleep(0.5)
        device.ClicommandCallback=myCommandCallback
    time.sleep(0.2)
        
deviceCli.disconnect()
        
        
        

