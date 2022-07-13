## Description
Simple botnet server created with python and socket module where you can switch between controlling multiple targets at once and single chosen target, the other features are:

* Target script will try to connect every 20 second to our server until the connection occurs
* Taking realtime screenshot(s) from infected device
* Executing cmd commands and receiving returned data if occurred
* Downloading and uploading files
* Keylogger that deletes the files after sending the data to our server
* Stealing wi-fi passwords from target network using cmd commands and regex to extract the data
* Getting target user location using https://ipinfo.io
* Script copies itself to windows catalog called appdata and updates registry to run the script every time machine is starting.
