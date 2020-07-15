This is a bot that will continuously check an email account for a new email whose title or content contains specific key words. Upon locating the email, the program will play some notification sound for a specified length before it exits.

BEFORE YOU START, NOTE:
This is developed with Python 2.7.16
This does not work with an email that uses MFA (like UCLA Mail).
This can be bypassed by setting the email account up in such a way that all incoming email are automatically forwarded to another account that you have access to without providing MFA.
The email account you wish to access has to allow less secure app access. You can do that by checking the ON option here:
https://myaccount.google.com/lesssecureapps?pli=1
The email account also needs to enable IMAP access. Do that by going to Gmail Settings -> Forwarding and POP/IMAP -> IMAP Access and click "Enable IMAP". Make sure to click Save Changes.

HOW TO USE:
The credentials.json contains a Javascript object that contains two attributes: "username" and "password". Simply input the email account's username and password in the respective fields.
Since this script will check for the email continously, it is designed with the idea that it will be running in the background using nohup.
Simply do 
    $ nohup python path/to/this/script/email-notif-bot.py &
The output from the script will be insert into a file called nohup.out located in the current directory.
The output from this command would look something like this:
    [1] 20372
    appending output to nohup.out
In this case, 20372 is the PID of the script. This is important for later on.

To see if the script is running still, do
    $ ps -ef | grep email-notif-bot.py
If this outputs a line that contains /path/to/python/on/your/machine email-notif-bot.py, the process is running.
This script can also reveal the PID of the script if you forgot what it was. The second number of the aforementioned line is the PID.

To stop the script, do 
    $kill pid
where pid is the PID of the script.