import time
import sys
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import subprocess
from datetime import datetime  
import os                         

interface = meshtastic.serial_interface.SerialInterface()
username = os.environ.get("USER", "Unknown")
ops_dir = f"/home/{username}/MeshShell"
os.makedirs(f'{ops_dir}', exist_ok=True)
logfile = f"{ops_dir}/logfile.log"
cmd_execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


art=r'''
 _____ ______   _______   ________  ___  ___  ________  ___  ___  _______   ___       ___          
|\   _ \  _   \|\  ___ \ |\   ____\|\  \|\  \|\   ____\|\  \|\  \|\  ___ \ |\  \     |\  \         
\ \  \\\__\ \  \ \   __/|\ \  \___|\ \  \\\  \ \  \___|\ \  \\\  \ \   __/|\ \  \    \ \  \        
 \ \  \\|__| \  \ \  \_|/_\ \_____  \ \   __  \ \_____  \ \   __  \ \  \_|/_\ \  \    \ \  \       
  \ \  \    \ \  \ \  \_|\ \|____|\  \ \  \ \  \|____|\  \ \  \ \  \ \  \_|\ \ \  \____\ \  \____  
   \ \__\    \ \__\ \_______\____\_\  \ \__\ \__\____\_\  \ \__\ \__\ \_______\ \_______\ \_______\
    \|__|     \|__|\|_______|\_________\|__|\|__|\_________\|__|\|__|\|_______|\|_______|\|_______|
                            \|_________|        \|_________|                                       
                                                                                                   
                                                                                                   
'''
def onReceive(packet): 

    try:
        if packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message = packet['decoded']['payload'].decode('utf-8')
            if message.startswith("Master"):
                cmd_output = receive(message)
        pass  
    except UnicodeDecodeError:
        pass  


def receive(message_in):

    if message_in.startswith("Master"):
        cmd = message_in.removeprefix("Master").strip().lstrip()  
        
        try:
            run_cmd = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if run_cmd.returncode == 0:
                cmd_output = (run_cmd.stdout)
                write_to_log(f"Date/Time: {cmd_execution_time} Command: {cmd} Return Code: {run_cmd.returncode}")
                sendmsg(f"SUCCESS: Command: {cmd} Completed")
                write_to_file(cmd, cmd_output)

            else:
                print(f"ERROR With Exit Status Code: {run_cmd.returncode}")
                write_to_log(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\tCommand: {cmd}\tReturn Code: {run_cmd.returncode}")
                sendmsg(f"ERROR With Exit Status Code: {run_cmd.returncode}") 
        
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("There is a problem somewhere with something")


def sendmsg(status_msg):
    interface.sendText(status_msg, wantAck = True)


def logfile_setup():
    try:
        with open(f"{logfile}", "x") as file:
            file.write("Date/Time\tCommand\tReturn Code\n")
            print("Logfile Created")
    except FileExistsError:
        print("Logfile Exists")


def write_to_log(msg_to_write):
    with open(f"{logfile}", 'a') as file:
        file.write(f"{msg_to_write}\n")


def write_to_file(cmd_to_save, cmd_output_to_save):
    with open(f"{ops_dir}/{cmd_to_save} {cmd_execution_time}", "x") as file:
        file.write(cmd_output_to_save)


def main():
    print(art)

    pub.subscribe(onReceive, "meshtastic.receive")
    print("Subscribed to meshtastic.receive")
    logfile_setup()

    try:
        while True:
            sys.stdout.flush()
            time.sleep(1)  
    except KeyboardInterrupt:
        print("Script terminated by user")
        interface.close()

if __name__ == "__main__":
    main()

