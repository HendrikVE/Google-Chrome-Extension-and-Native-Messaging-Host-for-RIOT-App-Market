#!/usr/bin/python
import os, errno, time, subprocess, sys, json, struct
import json, base64

def main(cmd):
    
    json_message = json.loads(get_message())
    output_file_content = base64.b64decode(json_message["output_file"])
    device = json_message["device"]
    application_name = json_message["application_name"]
    
    try:
        create_directories("/tmp/riotam/")
        
        with open("/tmp/riotam/" + application_name + ".elf", "wb") as executable:
            executable.write(output_file_content)
            
    except Exception as e:
        print e
    
    proc = subprocess.Popen(["gnome-terminal -e './flash " + device + "'"], shell=True)
    #build_result["cmd_output"] += proc.communicate()[0].replace("\n", "<br>")
    
def create_directories(path):
    
    try:
        os.makedirs(path)

    except OSError as e:

        if e.errno != errno.EEXIST:
            raise
    
# https://chromium.googlesource.com/chromium/src/+/master/chrome/common/extensions/docs/examples/api/nativeMessaging/host/native-messaging-example-host
def get_message():
    
    # Read the message length (first 4 bytes).
    text_length_bytes = sys.stdin.read(4)
    if len(text_length_bytes) == 0:
        sys.exit(0)

    # Unpack message length as 4 byte integer.
    text_length = struct.unpack('i', text_length_bytes)[0]

    # Read the text (JSON object) of the message.
    text = sys.stdin.read(text_length).decode('utf-8')
    
    return text
    
if __name__ == "__main__":
    
    main(sys.argv[0])