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
                username = data['username']
                password = data['password']
            else:
                raise Exception("Cannot find object with attribute 'username' and/or 'password' in JSON. Check credentials.json.")
            sys.stdout.write(' success.\nLogging in as ' + username + '.\n')
    except Exception as e:
        sys.stdout.write(' failed.\n'+ str(e)+'\n')
        sys.stdout.write('Script execution aborted.\n')
        exit()

def main():
    #log entry prefix
    now = datetime.now()
    sys.stdout.write("\nNEW RUN STARTING ON " + str(now) + '\n')
    load_credentials()
    while True:
        sys.stdout.flush()

if __name__ == '__main__':
    main()