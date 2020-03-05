from gpio import *
from time import *
from physical import *
from ioeclient import *

from environment import *

ENVIRONMENT_IMPACT_DIM = 10
VOLUME_AT_RATE = 100000

state = 0; # 0 off, 1 low, 2 high
lastTimeInSeconds = 0

def main():
setup()
while True:
loop()

def setup():

IoEClient.setup({
&quot;type&quot;: &quot;Light&quot;,
&quot;states&quot;: [
{
&quot;name&quot;: &quot;Status&quot;,
&quot;type&quot;: &quot;options&quot;,
&quot;options&quot;: {
&quot;0&quot;: &quot;Off&quot;,
&quot;1&quot;: &quot;Dim&quot;,
&quot;2&quot;: &quot;On&quot;
},
&quot;controllable&quot;: True
}

]
})

IoEClient.onInputReceive(onInputReceiveDone)
global state
add_event_detect(0, detect)
state = restoreProperty(&quot;state&quot;, 0)
setState(state)

def detect():
processData(customRead(0), False)

def onInputReceiveDone(analogInput):
processData(analogInput, True)

def restoreProperty(propertyName, defaultValue):
value = getDeviceProperty(getName(), propertyName)
if not (value is &quot;&quot; or value is None):
if type(defaultValue) is int :
value = int(value)

setDeviceProperty(getName(), propertyName, value)
return value
return defaultValue

def mouseEvent(pressed, x, y, firstPress):
global state
if firstPress:
setState(state+1)

def loop():
updateEnvironment()
sleep(1)

def processData(data, bIsRemote):
if len(data) &lt;= 0 :
return
setState(int(data))

def setState(newState):
global state
if newState &gt;= 3 :
newState = 0
state = newState

analogWrite(A1, state)
customWrite(0, state)
IoEClient.reportStates(state)
setDeviceProperty(getName(), &quot;state&quot;, state)

def updateEnvironment():
global VOLUME_AT_RATE
global ENVIRONMENT_IMPACT_DIM
volumeRatio = float(VOLUME_AT_RATE) / Environment.getVolume()
if state is 0 :
Environment.setContribution(&quot;Visible Light&quot;, 0,0, True)
elif state is 1:

Environment.setContribution(&quot;Visible Light&quot;,
ENVIRONMENT_IMPACT_DIM*volumeRatio, ENVIRONMENT_IMPACT_DIM*volumeRatio,
False)
elif state is 2 :
Environment.setContribution(&quot;Visible Light&quot;,
ENVIRONMENT_IMPACT_DIM*2*volumeRatio, ENVIRONMENT_IMPACT_DIM*2*volumeRatio,
False)

if __name__ == &quot;__main__&quot;:
main()
