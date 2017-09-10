#!/usr/bin/python
import os, errno, time, subprocess, sys, json, struct, shutil
import json, base64
import tempfile
import zipfile

def main(cmd):
    
    json_message = json.loads(get_message())
    
    output_file_content = base64.b64decode(json_message["output_file"])
    output_file_extension = json_message["output_file_extension"]
    
    output_archive_content = base64.b64decode(json_message["output_archive"])
    output_archive_extension = json_message["output_archive_extension"]
    
    device = json_message["device"]
    application_name = json_message["application_name"]
    
    try:
        path = tempfile.gettempdir() + "/riotam/"
        create_directories(path)
        
        with open(path + application_name + "." + output_file_extension, "wb") as executable:
            executable.write(output_file_content)
            
        # handle archive
        zip_path = path + "testarchive/"
        create_directories(zip_path)
        
        zip_file_path = zip_path + "test" + "." + output_archive_extension
        
        """with open(zip_file_path, "wb") as archive:
            archive.write(output_archive_content)"""
            
        #shutil.unpack_archive(zip_path)
        """zip_ref = zipfile.ZipFile(zip_file_path, 'r')
        zip_ref.extractall(zip_path + "tester/")
        zip_ref.close()"""
        
        #os.chdir(path + "testarchive/generated_by_riotam/test")
        #proc = subprocess.Popen(["make", "build.py",  arguments], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        proc = subprocess.Popen(["gnome-terminal -e './flash " + device + " " + path + "testarchive/tester/generated_by_riotam/test" + "'"], shell=True)
        
    except Exception as e:
        print e
    
    #proc = subprocess.Popen(["gnome-terminal -e './flash " + device + " " + path + "testarchive/" + "'"], shell=True)
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