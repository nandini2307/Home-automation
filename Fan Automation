from gpio import *
from time import *
from ioeclient import *
from physical import *
from environment import *
import math
FAN_SPEED_LOW = 0.4; # kph
FAN_SPEED_HIGH = 0.8; # kph
COOLING_RATE = float(-1)/3600; # -1C/hour
HUMDITY_REDUCTION_RATE = float(-1)/3600; # -1%/hour

VOLUME_AT_RATE = 100000; # the given rates are based on this volume

state = 0; # 0 off, 1 low, 2 high
level = 0

def main():
global state
IoEClient.setup({
&quot;type&quot;: &quot;Ceiling Fan&quot;,
&quot;states&quot;: [
{
&quot;name&quot;: &quot;Status&quot;,
&quot;type&quot;: &quot;options&quot;,
&quot;options&quot;: {

&quot;0&quot;: &quot;Off&quot;,
&quot;1&quot;: &quot;Low&quot;,
&quot;2&quot;: &quot;High&quot;
},
&quot;controllable&quot;: True
}
]
})

IoEClient.onInputReceive(onInputReceiveDone)
add_event_detect(0, detect)
state = restoreProperty(&quot;state&quot;, 0)
setState(state)
while True:
delay(1000)

def onInputReceiveDone(data):
processData(data, True)

def detect():
processData(customRead(0), False)

def restoreProperty(propertyName, defaultValue):
value = getDeviceProperty(getName(), propertyName)
if not (value is &quot;&quot; or value is None):
if type(defaultValue) is int :
value = int(value)

setDeviceProperty(getName(), propertyName, value)
return value

return defaultValue

def mouseEvent(pressed, x, y, firstPress):
if firstPress:
toggleState()

def processData(data, bIsRemote):
if len(data) &lt;= 0 :
return
data = data.split(&quot;,&quot;)
setState(int(data[0]))

def sendReport():
global state
global report
report = state # comma seperated states
customWrite(0, report)
IoEClient.reportStates(report)
setDeviceProperty(getName(), &quot;state&quot;, state)

def setState(newState):
global state
analogWrite(A1, newState)
state = newState

sendReport()
updateEnvironment()

def toggleState():
global state
state += 1
if int(state) &gt;= 3:
state = 0

setState(state)

def updateEnvironment():
global VOLUME_AT_RATE
global FAN_SPEED_LOW
global COOLING_RATE
global HUMDITY_REDUCTION_RATE
global FAN_SPEED_HIGH
global state
volumeRatio = float(VOLUME_AT_RATE) / Environment.getVolume()

if int(state) == 0:
Environment.setContribution(&quot;Wind Speed&quot;, 0, 0, True)
Environment.setContribution(&quot;Ambient Temperature&quot;, 0, 0, True)
Environment.setContribution(&quot;Humidity&quot;, 0,0, True)

elif int(state) == 1:
Environment.setContribution(&quot;Wind Speed&quot;, FAN_SPEED_LOW,
FAN_SPEED_LOW, False)

# everytime the fan restarts, it can do another -100C
Environment.setContribution(&quot;Ambient Temperature&quot;,
float(COOLING_RATE)/2*volumeRatio,
Environment.getCumulativeContribution(&quot;Ambient Temperature&quot;)-100, True)

Environment.setContribution(&quot;Humidity&quot;,
float(HUMDITY_REDUCTION_RATE)/2*volumeRatio,
Environment.getCumulativeContribution(&quot;Humidity&quot;)-100, True)
elif int(state) == 2:
Environment.setContribution(&quot;Wind Speed&quot;, FAN_SPEED_HIGH,
FAN_SPEED_HIGH, False)

Environment.setContribution(&quot;Ambient Temperature&quot;,
float(COOLING_RATE)/2*volumeRatio,
Environment.getCumulativeContribution(&quot;Ambient Temperature&quot;)-100, True)

Environment.setContribution(&quot;Humidity&quot;,
HUMDITY_REDUCTION_RATE*volumeRatio,
Environment.getCumulativeContribution(&quot;Humidity&quot;)-100, True)

if __name__ == &quot;__main__&quot;:
main()
