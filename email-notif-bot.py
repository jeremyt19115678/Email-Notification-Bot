from datetime import datetime
import imaplib
import sys, json, os

#load login credentials from credentials.json
def load_credentials():
    filepath = os.path.join(os.getcwd(), './credentials.json')
    sys.stdout.write("Looking for login credentials at " + filepath + "......")
    try:
        with open(filepath) as f:
            data = json.load(f)
            if 'username' in data.keys() and 'password' in data.keys():
                username = data['username'].encode('ascii', 'replace')
                password = data['password'].encode('ascii', 'replace')
            else:
                raise Exception("Cannot find object with attribute 'username' and/or 'password' in JSON. Check credentials.json.")
            sys.stdout.write(' success.\n')
    except Exception as e:
        sys.stdout.write(' failed.\n'+ str(e)+'\n')
        sys.stdout.write('Script execution aborted.\n')
        exit()
    return (username, password)

def open_connection(username, password):
    try:
        sys.stdout.write('Logging into ' + username + '......')
        connection = imaplib.IMAP4_SSL('imap.gmail.com')
        connection.login(username, password)
    except Exception as e:
        sys.stdout.write(' failed.\n' + str(e) + '\n')
        exit()
    sys.stdout.write(' success.\nConnection established.\n')
    return connection

def main():
    #log entry prefix
    now = datetime.now()
    sys.stdout.write("\nNEW RUN STARTING ON " + str(now) + '\n')
    username, password = load_credentials()
    connection = open_connection(username, password)
    print(connection.list(pattern='*INBOX*'))
    #while True:
        #sys.stdout.flush()

if __name__ == '__main__':
    main()