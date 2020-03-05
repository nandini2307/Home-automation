from cli import *

from gui import *
import json
import mqttbroker
from time import *

def guiEvent(type, args):
data = json.loads(args)

if type == &quot;state&quot;:
GUI.update(&quot;state&quot;, json.dumps(mqttbroker.state()))
mqttbroker.update_authorized_users_table()
mqttbroker.update_clients_table()
mqttbroker.update_subscriptions_table()
elif type == &quot;enable_service&quot;:
mqttbroker.enable_service()
elif type == &quot;disable_service&quot;:
mqttbroker.disable_service()
elif type == &quot;add_user&quot;:
if mqttbroker.add_user(data[&quot;username&quot;], data[&quot;password&quot;]):
GUI.update(&quot;add_user_success&quot;, json.dumps({&quot;username&quot;:

data[&quot;username&quot;], &quot;password&quot;: data[&quot;password&quot;]}))

else:
GUI.update(&quot;add_user_fail&quot;, json.dumps({&quot;username&quot;:

data[&quot;username&quot;], &quot;password&quot;: data[&quot;password&quot;]}))
elif type == &quot;remove_user&quot;:
if mqttbroker.remove_user(data[&quot;username&quot;]):
GUI.update(&quot;remove_user_success&quot;, json.dumps({&quot;username&quot;:

data[&quot;username&quot;]}))
else:
GUI.update(&quot;remove_user_fail&quot;, json.dumps({&quot;username&quot;:

data[&quot;username&quot;]}))

def cliEvent(type, args):
if type == &quot;invoked&quot; and args[0] == &quot;mqttbroker&quot;:
if len(args) == 1 or len(args) == 2 and args[1] == &quot;-?&quot; or

args[1] == &quot;/?&quot;:

print_cli_usage()
CLI.exit()
elif len(args) &gt; 1 and args[1] != &quot;-?&quot; and args[1] != &quot;/?&quot;:
if len(args) == 2 and args[1] == &quot;enable-service&quot;:
mqttbroker.enable_service()
print &quot;Success: MQTT broker service enabled.&quot;
print &quot;&quot;
CLI.exit()
elif len(args) == 2 and args[1] == &quot;disable-service&quot;:
mqttbroker.disable_service()
print &quot;Success: MQTT broker service disabled.&quot;
print &quot;&quot;
CLI.exit()
elif len(args) &gt; 2 and len(args) &lt; 5 and args[1] == &quot;add-

user&quot;:

password = &quot;&quot;

if len(args) == 4:
password = args[3]

if mqttbroker.add_user(args[2], password):
GUI.update(&quot;add_user_success&quot;,
json.dumps({&quot;username&quot;: args[2], &quot;password&quot;: password}))

print &quot;Success: added new user &quot; + args[2] +

&quot;.&quot;

else:
GUI.update(&quot;add_user_fail&quot;,
json.dumps({&quot;username&quot;: args[2], &quot;password&quot;: password}))

print &quot;Error: could not add new user &quot; +

args[2] + &quot;.&quot;

print &quot;&quot;
CLI.exit()
elif len(args) == 3 and args[1] == &quot;remove-user&quot;:
if mqttbroker.remove_user(args[2]):
GUI.update(&quot;remove_user_success&quot;,

json.dumps({&quot;username&quot;: args[2]}))

print &quot;Success: removed user &quot; + args[2] +

&quot;.&quot;

else:
GUI.update(&quot;remove_user_fail&quot;,

json.dumps({&quot;username&quot;: args[2]}))

print &quot;Error: could not remove user &quot; +

args[2] + &quot;.&quot;

print &quot;&quot;
CLI.exit()
elif len(args) == 2 and args[1] == &quot;display-last-event&quot;:
events = mqttbroker.state()[&quot;events&quot;]

if len(events) &gt; 0:
print events[-1]

print &quot;&quot;
CLI.exit()
elif len(args) == 2 and args[1] == &quot;display-all-events&quot;:
events = mqttbroker.state()[&quot;events&quot;]

for event in events:
print event

print &quot;&quot;
CLI.exit()
else:
print_cli_usage()
CLI.exit()
elif type == &quot;interrupted&quot;:
CLI.exit()

def print_cli_usage():
print &quot;MQTT Broker&quot;
print &quot;&quot;
print &quot;Usage:&quot;
print &quot;mqttbroker enable-service&quot;
print &quot;mqttbroker disable-service&quot;
print &quot;mqttbroker add-user &lt;username&gt; [password]&quot;
print &quot;mqttbroker remove-user &lt;username&gt;&quot;
print &quot;mqttbroker display-last-event&quot;
print &quot;mqttbroker display-all-events&quot;
print &quot;&quot;

def on_gui_update(msg, data):
GUI.update(msg, data)

def main():
GUI.setup()
CLI.setup()
mqttbroker.init()
mqttbroker.onGUIUpdate(on_gui_update)

while True:
delay(60000)

if __name__ == &quot;__main__&quot;:
main()
