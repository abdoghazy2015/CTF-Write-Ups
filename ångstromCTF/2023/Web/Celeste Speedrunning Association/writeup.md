![image](https://user-images.githubusercontent.com/64314534/234530041-cda6bfd0-2ad6-474a-86c0-3093167856f4.png)



<br>


### This challenge is tooo ez when you enter you will find something like a scoreboard and to solve the challenge you had to beat them
<br>

![image](https://user-images.githubusercontent.com/64314534/234530290-7a5547ab-7058-43a9-abde-bc3a40a3410b.png)
<br>

### That seems the challenge is about race condition or something like that but as you can see in records the first place got 0 seconds so, it's weired but let's go to /play
<br>


![image](https://user-images.githubusercontent.com/64314534/234531966-7a9ac9b4-101e-4030-be56-6f5a0aa001d8.png)

<br>

### As you can see it's a button and if you clicked it you will be redirected to /submit with this result
<br>

![image](https://user-images.githubusercontent.com/64314534/234532129-b7919157-e023-457c-86f6-bf67fd54f193.png)
<br>

### So, let's click the button and intercept the request with burp suite 
<br>

![image](https://user-images.githubusercontent.com/64314534/234533712-44d9b4e0-22e7-470f-a7c1-9bbd077c0c7d.png)

<br>

### As you can see it sends the parameter called `start` which had something like a unix time so, you can use cyberchef to convert it to the actual time
<br>

![image](https://user-images.githubusercontent.com/64314534/234534932-d5a6cad5-351b-41c9-8a6d-c76bd7baa852.png)

<br>


### It's the time when i clicked the button and it seems that's calculate the diffrence between this time and it's time and it should less then zero to win and got the flag so, i give it a future time like this :
<br>

![image](https://user-images.githubusercontent.com/64314534/234535558-56c1560b-4c87-4d1c-ad4e-6457032e2981.png)

<br>

### And then we can got the flag 

<br>

![image](https://user-images.githubusercontent.com/64314534/234535952-466c3926-1c24-4afa-b9da-ec99c64ac869.png)


