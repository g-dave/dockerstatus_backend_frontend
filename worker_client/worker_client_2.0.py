import os
import requests
import json
import datetime


def ps_a_command_on_terminal(handedoverdestinationsrv):
    if handedoverdestinationsrv == "":
        destinationsrv = 'http://127.0.0.1:5000/'
    else:
        destinationsrv = handedoverdestinationsrv
    
    try:
        os.system("""docker ps -a --format "{{.ID}} {{.Names}} {{.State}} {{.Image}}" > ps-a.txt""")
        hostname_stream = os.popen('hostname')
        hostname = hostname_stream.read()
        hostname = str.rstrip(hostname)

        #first action delete all container information on backend from from this node
        send_response = requests.delete(destinationsrv+'nodes/'+hostname)
 
        current_timestamp = str(datetime.datetime.now())
        execinformation = "yes"
        file_array = []
        filename = "ps-a.txt"
        try:
            filepointer = open(filename, 'r')
            file_array = filepointer.readlines() #list element by line

        except:
            print("some error while loading:", filename)

        if len(file_array) > 0:
            for line in file_array:
                element = line.split(" ")
                try:
                    json={"containerid": element[0], "name": element[1], "status": element[2], "node": hostname, "timestamp": current_timestamp}

                    send_response = requests.post(destinationsrv+'containers', json={"containerid": element[0], "name": element[1], "status": element[2], "node": hostname, "timestamp": current_timestamp})

                except:
                    print("something went wrong by requests call ")
        else:
            print("no content in file?!?")
    except:
        return None
    return execinformation

psatxt = ps_a_command_on_terminal("")