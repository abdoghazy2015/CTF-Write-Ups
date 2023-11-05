# Quick Writeup for CyVoting Web Challenge.



#### Our goal was clear: to login as admin since the flag is in admin.php and we need admin account to access it
 <br/>

 ![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/a2445e14-5945-4b6d-9600-130e5a35474a)



<h4>

After reviewing the code We can find that login-admin.php can't be accessed from outside the localhost so, we cannot use it to login as admin
</h4>

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/824fd688-0158-4a90-ac7c-a0b52bd1b0df)
<h4>

and in login.php we can see a function that check if the username contains word "admin" in upper and lower cases and if matches it will redirect us to login-admin.php which can be accessed only from the localhost
</h4>

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/3c52ce15-0cc6-4d3d-b1b6-e01043ff0176)

> Mysql by default is case insensitive and also normalizing the Unicode chars so, we can bypass this using any unicode character from "admin" like : Àdmin
```ini
You can check my bruh1, bruh2 challenges from here
https://drive.google.com/drive/folders/1Lb28Gi13xyP5B9i3R8ra733JSEZuYw3K
```

<h4>

Then wen need to get then admin password login as admin.

There is a sqli at vote.php it takes our input from id parameter and then decrypt it then concatinating it to the sql query without any sanitizing so, we just need to find a way to encrypt our payload!
</h4>

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/6f235006-9b70-4199-ae55-e006e2f159be)

<h4>in reset.php we can find that our input is being passed to generate_secure_token function and then we can access this token from the location response header.</h4>

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/705e62cc-1bce-4b42-b07d-8d3b2cafd6be)
<h4>
this function is in crypto.php file and just passing our input to the encrypt function then put it in json format to be in this way </h4>

> {"username":"encrypted_value"}

<h4> then put it in base64 encoding format.<h4>


![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/fd9f7189-aabb-48b8-968b-d9789e97022d)

<h4> so, now it's clear we need to use reset.php to encrypt our input and inject it to the query. </h4>h4>

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/f44c5dd5-de7a-43ec-97ed-a32691a1fdfe)

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/cb30dba6-1633-4284-82bf-fce95069ee00)
![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/84ff91c7-6fd2-443b-9235-8e8497379ad3)

> vote.php also decrypting the encrypted value in name parameter and print it so, we can see our payload after decrypting

<h4> and now we successfuly did a union based sqlinjection exploit so, let's use it to get the admin password from the db by using this payload: `' union select 100,password,300,400 from users#` </h4>

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/8e923feb-93b9-4e8a-b424-7eb49abae2c4)

<h4>
then we can go to login.php and login with these creds. 

`Àdmin:Fake_P@ssw0rd`

And we can get our ecrypted flag from the html comments 
</h4>

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/1d9ec2c4-b357-4f8a-8573-a15adf14b863)

<h4> and we can use name parameter in vote.php to decrypt it. </h4>
![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/0bcc0611-354e-428e-b044-3b5033352977)

