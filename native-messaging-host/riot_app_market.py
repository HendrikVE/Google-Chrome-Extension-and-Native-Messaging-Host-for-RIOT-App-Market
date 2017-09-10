#!/usr/bin/python
import os, errno, time, subprocess, sys, json, struct
import json, base64
from shutil import rmtree
import tarfile

def main(cmd):
    
    json_message = json.loads(get_message())
    
    output_file_content = base64.b64decode(json_message["output_file"])
    output_file_extension = json_message["output_file_extension"]
    
    output_archive_content = base64.b64decode(json_message["output_archive"])
    output_archive_extension = json_message["output_archive_extension"]
    
    device = json_message["device"]
    application_name = json_message["application_name"]
    
    try:
        path = "tmp/"
        
        archieve_file_path = path + application_name + "." + output_archive_extension
        
        with open(archieve_file_path, "wb") as archive:
            archive.write(output_archive_content)
            
        dest_path = path + application_name + "/"
        create_directories(dest_path)
        
        tar = tarfile.open(archieve_file_path, "r:gz")
        for tarinfo in tar:
            tar.extract(tarinfo, dest_path)
            
        tar.close()
        
        path_to_makefile = dest_path + "generated_by_riotam/" + application_name + "/"
        proc = subprocess.Popen(["gnome-terminal -e './flash " + device + " " + path_to_makefile + "'"], shell=True)
        
        # rmtree(path)
        
    except Exception as e:
        print e
    
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