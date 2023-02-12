# Chelsea checkout bot

1. ./requirements.txt - Install all the requirements from the file (I recommend using pycharm for this)
2. ./main.py - Add your supporter numbers as ints for example: supporter_numbers = [111111, 222222] in this array, get them from  here https://chelseafc.3ddigitalvenue.com/friends-family
3. ./resources/login_details.json - Update your username and password (email and password)
4. ./main.py - Set the number of checkouts you want to make per stand in the num_of_attempts, currently defaulted to 1
5./main.py - Set the event id, you can find this in the https://chelseafc.3ddigitalvenue.com/buy-tickets when the event appears in the URL e.g. 1115 is for Chelsea vs Dortmund
