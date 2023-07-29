# Hello everyone, this is my writeup for my Ez DFIR challenge " Revenge I " in CAT CTF 23

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/c28e1ae6-d48a-4ea3-b470-1a1aed1fce32)


### Since our target is to get some info (attacker_name & group name) so, let's  analyze this xlsx file !

### After openning the file we will see one column hold the names of some companies and seems to be the target for this group !

### Since the description said there is no osint required so, let's unzip the xlsx file to analyze it .

### To get the username of the attacker we need to know the user that created this file by reading this file : 

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/0521c8ee-9a8a-4336-ae98-1d24a4c12d97)

### So, our attacker is `Th3-0b3l1sk`  #Answer 1

### After that we can get the Group name by getting the path that this file has been saved when created by reading this file :

![image](https://github.com/abdoghazy2015/CTF-Write-Ups/assets/64314534/4cb6f540-2447-4a0c-a539-10cedb0db526)

### Our flag  : CATF{Th3-0b3l1sk_n!NjaTur7l5}



