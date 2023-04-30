## Blackbox

<br>
  
![image](https://user-images.githubusercontent.com/64314534/235363758-3c94f31a-10c9-4f6e-b120-d869bc9a695d.png)

<br>

This should be a black box challenge but after some directory bruteforcing using `dirsearch` tool we found `.git` so, we used `git-dumper` tool to dump the source code

<br>


![image](https://user-images.githubusercontent.com/64314534/235364168-d5ea64e6-ad41-4de4-8ff0-1637a8d66791.png)

<br>

There are too many files but the only important are : index.php,admin.php,util.php,config.php,site-data.db


## Code Analysis:

### index.php

<br>

![image](https://user-images.githubusercontent.com/64314534/235364383-dac45006-2a4a-4031-bf41-1c4bceccfe08.png)

<br>

We can see that there is a limited Local File Inclusion vulnerability //since it's append .php to our input 

<br>

### admin.php

<br>

![image](https://user-images.githubusercontent.com/64314534/235364521-f509432e-0c37-44b2-8828-3d9b7e1578ba.png)


<br>

We can see that this page had the flag but to access it , we need to had cookie called `auth_token` and this cookie will passed into `is_admin` function and if it returned false the application will redirect us to the index page without viewing the page content.

So, our goal is clear now ! we need to forge this cookie to make the `is_admin` function returns true and then we can get the flag.

<br>

### util.php

<br>

![image](https://user-images.githubusercontent.com/64314534/235367099-3b378d93-917f-4fdb-8911-3bd142e1658b.png)

<br>

This file had many functions but we only need to review is `is_admin` function and any functions used by it . 

<br>

![image](https://user-images.githubusercontent.com/64314534/235367672-2b120719-7d2e-4cc9-8f44-1eb0cebb107b.png)

<br>

The is_admin function is doing the following : 

- Pass the token to `verify_token` function and if ok it will continue 
- Decode the token from base64 encoding and then from json 
- Get username,userkey,admin from the json data
- Select data that related to these username,userkey from db but in a secure way ( no sql injection here) 
- If the db had values for these username,userkey and admin==true the function will return true


## Exploit : 

- We need to make the `verify_token` function return true by getting the secret key from `config.php` file using LFI bug and php wrapper

<br>

![image](https://user-images.githubusercontent.com/64314534/235368134-91d38167-e7fd-40d8-a1fd-8175f5c09ba3.png)

<br>
- We will use `generate_admin_token` function to generate a new admin token 
<br>

![image](https://user-images.githubusercontent.com/64314534/235368259-1476c5f3-9f75-4b60-9e97-9486158bb815.png)

<br>

- To generate a new admin token we need username and user_key and we can get them from the db file

<br>

![image](https://user-images.githubusercontent.com/64314534/235368321-8deca14d-61f3-4ab5-bd4d-4bdc34e320ea.png)


<br>

- Now we had username, user_key, functions that generate the valid users so, let's try to make the exploit 

```php

<?php

const SECRET_KEY = 'JYOFGX6w5ylmYXyHuMM2Rm7neHXLrBd2V0f5No3NlP8';

function generate_admin_token(string $username, string $user_key) {
  $data = array('username'=>$username, 'user_key'=>$user_key, 'admin'=>true);
  return generate_token($data);
}

function generate_token(array $data) {
  $b64json = base64_encode(json_encode($data));
  $hmac = hash('md5', SECRET_KEY . $b64json);

  return $b64json . '.' . $hmac;
}


echo generate_admin_token('admin','26ceb685f46e6d22');

?>
```

and after running this file and send this request with the generated token we can get the flag : ) 

<br>

![image](https://user-images.githubusercontent.com/64314534/235368660-ffd9f0f1-706a-466a-83e7-9db740e2509c.png)
