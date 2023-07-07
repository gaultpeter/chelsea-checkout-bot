# Chelsea checkout bot

1. ./requirements.txt - Install all the requirements from the file
2. ./main.py - Add your supporter numbers as INTEGERS for example: supporter_numbers = [111111, 222222] in this array, get them from  here https://chelseafc.3ddigitalvenue.com/friends-family
3. ./resources/login_details.json - Update your username and password (email and password)
4. ./main.py - Set the number of checkouts you want to make per stand in the num_of_attempts, currently defaulted to 1, dont use greater than 2/3 you will time your account out.
5. ./main.py - Set the event id as a STRING, you can find this in the https://chelseafc.3ddigitalvenue.com/buy-tickets when the event appears in the URL e.g. 1115 is for Chelsea vs Dortmund
6. ./main.py - Set the on sale time, you can either run manually or have this set 1 second before they go on sale. Setting this in the past will start automatically.