# lc-hue
A simple Python script that monitors telemetry from an organization inside of LimaCharlie and adjust the Hue lightbulbs on the network according to tags in the detection telemetry.

All documnentaiton for LimaCharlie can be found here: https://doc.limacharlie.io

An evolving help center built around common tasks can be found here: https://help.limacharlie.io

Free online courses for LimaCharlie can be found here: https://edu.limacharlie.io

If you are reading this and send me an email at chris@limacharlie.io I will send you a 
t-shirt and some swag :-)

# Phue
This script leverages the Phue Python library: https://github.com/sqmk/Phue

# Hue
Before running the script you will need to generate a username.
A username can be generated using the built in web server and API test mechanism
provided by Hue on your briddge: https://developers.meethue.com/develop/get-started-2/

# venv
On my development machine this project uses venv. If you are writing Python you should be using venv (or some other virtual envirnment). More detials here: https://docs.python.org/3/library/venv.html
% source bin/activate
^ this will start the virtual env from withing the project folder
