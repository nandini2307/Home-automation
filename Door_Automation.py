from time import *
from physical import *
from gpio import *
from environment import Environment
from ioeclient import IoEClient

ENVIRONMENTS = [&quot;Argon&quot;, &quot;CO&quot;, &quot;CO2&quot;, &quot;Hydrogen&quot;, &quot;Helium&quot;, &quot;Methane&quot;,
&quot;Nitrogen&quot;, &quot;O2&quot;, &quot;Ozone&quot;, &quot;Propane&quot;, &quot;Smoke&quot;]
ENVIRONMENT_MAX_IMPACT = -0.02 # 2% max when door opens
TEMPERATURE_TRANSFERENCE_MULTIPLIER = 1.25 # increase speed 25% when door
open
HUMIDITY_TRANSFERENCE_MULTIPLIER = 1.25
GASES_TRANSFERENCE_MULTIPLIER = 2

doorState = 0 # 0 is closed, 1 is opened
lockState = 0 # 0 is unlocked, 1 is locked

def on_event_detect_0 () :
processData(customRead(0), False)

def on_input_receive(input) :
processData(input, True)

def setup ():
IoEClient.setup({
&quot;type&quot;: &quot;Door&quot;,
&quot;states&quot;: [{
&quot;name&quot;: &quot;Open&quot;,
&quot;type&quot;: &quot;bool&quot;
},
{
&quot;name&quot;: &quot;Lock&quot;,
&quot;type&quot;: &quot;options&quot;,
&quot;options&quot;: {
0: &quot;Unlock&quot;,
1: &quot;Lock&quot;
},
&quot;controllable&quot;: True
}]
})

IoEClient.onInputReceive(on_input_receive)

add_event_detect(0, on_event_detect_0)

setDoorState(doorState)
setLockState(lockState)

def mouseEvent (pressed, x, y, firstPress):

if firstPress:
if isPointInRectangle(x, y, 10,40,5,10) :
if lockState == 0 :
setLockState(1)
else:
setLockState(0)
else:
if doorState == 0 :
openDoor()
else:
closeDoor()

def processData (data, bIsRemote):
if len(data) &lt; 1 :
return

print data

data = data.split(&quot;,&quot;)
doorStateData = int(data[0])
lockStateData = int(data[1])
if lockStateData &gt; -1 :
setLockState(lockStateData)

if doorStateData &gt; -1 and not bIsRemote :
if doorStateData == 0 :
closeDoor()
else:
openDoor()

def sendReport ():
report = str(doorState)+&quot;,&quot;+str(lockState) # comma seperated states
customWrite(0, report)

IoEClient.reportStates(report)
setDeviceProperty(getName(), &quot;door state&quot;, doorState)
setDeviceProperty(getName(), &quot;lock state&quot;, lockState)

def closeDoor ():
setDoorState(0)
updateEnvironment()

def openDoor ():
if lockState == 0 :
setDoorState(1)
updateEnvironment()
else:
print &quot;can&#39;t open locked door&quot;

def setDoorState (state):
global doorState
if state == 0:
digitalWrite(1, LOW)
setComponentOpacity(&quot;led&quot;, 1) # show the led
else:
digitalWrite(1, HIGH)

setComponentOpacity(&quot;led&quot;, 0) # hide the led

doorState = state
sendReport()

def setLockState (state):
global lockState
if state == 0 :
digitalWrite(2, LOW)
else:
digitalWrite(2, HIGH)

lockState = state
sendReport()

def updateEnvironment ():
rate, emax = 0, 0
if doorState == 1:
for e in ENVIRONMENTS:
emax = Environment.get(e) * ENVIRONMENT_MAX_IMPACT
# the emax is reached in an hour, so we divide by 3600 to get
seconds
# then this rate is also based on 100,000 cubic meters (approx.
coporate office size)
rate = emax / 3600 * 100000 / Environment.getVolume()
Environment.setContribution(e, rate, emax, True)
Environment.setTransferenceMultiplier(e,
GASES_TRANSFERENCE_MULTIPLIER)

Environment.setTransferenceMultiplier(&quot;Ambient Temperature&quot;,
TEMPERATURE_TRANSFERENCE_MULTIPLIER)
Environment.setTransferenceMultiplier(&quot;Humidity&quot;,
HUMIDITY_TRANSFERENCE_MULTIPLIER)
else:
for e in ENVIRONMENTS:
Environment.setContribution(e, 0, 0, True)
Environment.removeCumulativeContribution(e)
Environment.setTransferenceMultiplier(e, 1)

Environment.setTransferenceMultiplier(&quot;Ambient Temperature&quot;, 1)
Environment.setTransferenceMultiplier(&quot;Humidity&quot;, 1)

def isPointInRectangle (x,y, rx, ry, width, height):
if width &lt;= 0 or height &lt;= 0:
return False
return (x &gt;= rx and x &lt;= rx + width and y &gt;= ry and y &lt;= ry + height)

if __name__ == &quot;__main__&quot;:
setup()
while True:
sleep(0)
