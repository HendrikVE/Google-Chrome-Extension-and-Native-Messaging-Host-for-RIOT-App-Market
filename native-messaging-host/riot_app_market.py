#!/usr/bin/python
import time, subprocess, sys, json, struct

def main(cmd):
    
    proc = subprocess.Popen(["gnome-terminal -e './flash pba-d-01-kw2x'"], shell=True)
    #build_result["cmd_output"] += proc.communicate()[0].replace("\n", "<br>")
   
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