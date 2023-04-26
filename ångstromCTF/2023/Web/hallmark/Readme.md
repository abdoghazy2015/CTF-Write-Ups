![image](https://user-images.githubusercontent.com/64314534/234540425-1f4a28ba-cf8c-4fdc-8bf0-30444beb81d6.png)

<br>

### From the description we can guess it's a Xss Challenge and we had the source code also, so let's try to see the challenge first then try to understand the source code 

<br>

![image](https://user-images.githubusercontent.com/64314534/234540812-325aac3c-d36d-4656-bb61-247bdcf54dda.png)

<br>

### The challenge takes an input from us so, let's try simple payload like : `<h1> test </h1>` in the `content` input

<br>

![image](https://user-images.githubusercontent.com/64314534/234541362-4aee29de-8707-434c-b597-87892d6b6109.png)

<br>

### After click on `Send Card` button, it  will redirect us to `/card?id=uuid_of_the_card` 
<br>

![image](https://user-images.githubusercontent.com/64314534/234541248-74e056e8-1652-4ec6-b21e-7b743d2069aa.png)

<br>

### But as you see, it's filtered so i tried to see the request at burp suite 

<br>

![image](https://user-images.githubusercontent.com/64314534/234542524-911c12ea-4bc3-4b40-86e2-344358107ff7.png)

<br>

### There are two parameters one called `svg` and another one called `content` so i sent the request and redirected to the card 

<br>

![image](https://user-images.githubusercontent.com/64314534/234542840-f29e5a0c-c23f-4b38-8687-612f4050371c.png)

<br>

### As you can see the content is not filtered but the browser didn't parse the Html content because the `Content-Type` response header is set to `text/plain; charset=utf-8` so, the browser will handle it as a normal text  but i got noticed that's a parameter called `svg` in the request and as we know can get xss using svg so, let's back to the index page to see how this svg handeled.

<br>


![image](https://user-images.githubusercontent.com/64314534/234547113-ef4d455a-47c4-471a-b473-8e040c3c6424.png)

<br>

![image](https://user-images.githubusercontent.com/64314534/234547211-017ba358-d1ed-4c8e-aaea-c3ee5b57f867.png)

<br>

### You can see from the previous imgs that you can choose some shapes from the type list like [Heart,Cake,...etc]. and you can enter text only id you choosed `Custom Text`

<br><br>

# Enough blindly testing and let's start reviewing the App code (nodejs)

<br>

### We had many files but we only need to review `index.js`

<br>

![image](https://user-images.githubusercontent.com/64314534/234550939-aa8d92a5-f2a5-4d2f-86d3-78d450f5eb0b.png)

<br>

![image](https://user-images.githubusercontent.com/64314534/234551998-46020b78-1d87-42e6-b5e6-04e114091357.png)

<br>

### From the first part of the code you can see some interested things like 
 -  `app.use(bodyParser.urlencoded({ extended: true }));` that will allow the application to accept objects in request parameters 
 -  IMAGES Object that many files you can access is based on the key like : `IMAGES[heart]` will return the svg image : `./static/heart.svg`
 -  The IMAGES Object is freezed so no one can edit or append anything to it
 -  Initate Cards  Object   

<br>

![image](https://user-images.githubusercontent.com/64314534/234554067-9fd25163-f06a-4309-be49-8cf67a596f15.png)

<br>

### The application following the REST api workflow :
- GET  : view something
- POST : add something
- PUT  : edit something
- Delete : remove something
<br>

### We will explain each part 
<br>

![image](https://user-images.githubusercontent.com/64314534/234554993-cf3fa6e4-ce3c-4b10-a1ac-87d98933c490.png)

<br>

### The GET part will do the following :
- Check if the user provides `id` parameter `/card?id=`
- Check if the Cards Object had this id in it's keys 
- IF this card id exist it will return it's type as a `Content-Type` response header and it's content as a response body
- IF this card id is not exist it will send "bad id" as a response body

<br>
![image](https://user-images.githubusercontent.com/64314534/234556298-03ae4936-2d30-429c-b630-4ccb787e21fc.png)

<br>

### The POST part will do the follwing :
- Will take svg,content variables from the request body   `svg=&content` // same as the data we saw in the add card request
- Declare the type variabe to be `text/plain` and id variable to had a UUID v4 value
- 

