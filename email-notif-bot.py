from datetime import datetime
import imaplib
import sys, json, os
import time
import email

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

def get_latest_mail_body(connection):
    try:
        sys.stdout.write('Looking into inbox......')
        connection.select('INBOX', readonly=True)
        typ, ids = connection.search(None, '(FROM "Jeremy")') #second parametr specifies the search criterion
        email_ids = ids[0].split()
        if len(email_ids) > 0:
            sys.stdout.write('\nEmail(s) with ID ')
            id_string = ""
            for iden in email_ids:
                id_string += iden + ', '
            id_string = id_string[:-2]
            sys.stdout.write(id_string + ' fit the criteria.\n')
            sys.stdout.write('Examining email with ID ' + str(email_ids[-1]) + '.\n')
            latest_email_id = email_ids[-1] #get the latest email 
        else:
            raise Exception("Couldn't find any emails that satisfy the search requirement.")
        typ, msg_data = connection.fetch(latest_email_id, '(RFC822)') # first parameter specifies the ID from the search
        search_pool_src = 0
        search_pool = ""
        for response_part in msg_data: #because the response part contains only two parts, a string and a tuple
            if isinstance(response_part, tuple): #the other part is a string ')' that signals the end of the response
                msg = email.message_from_string(response_part[1]) #response_part[0] is irrelevant
                #take care of multipart emails
                messages = []
                messages.append(msg)
                 #look through all the messages and all the sub-messages
                while messages: #messages is empty
                    if messages[0].is_multipart(): #would return a list of messages
                        for parts in messages[0].get_payload():
                            messages.append(parts)
                    else: #payload is a string object as per doc
                        search_pool_src += 1
                        search_pool += messages[0].get_payload(decode=True)
                    messages.pop(0) #because we processed the first message in the messages list
                return search_pool_src, search_pool
    except Exception as e:
        sys.stdout.write(' failed.\n' + str(e) + '\n')
        return None, None

#play some sound at top volume nonstop
def alert():
    pass

def main():
    #log entry prefix
    now = datetime.now()
    sys.stdout.write("\nNEW RUN STARTING ON " + str(now) + '\n')
    username, password = load_credentials()
    connection = open_connection(username, password)
    count, search_pool = get_latest_mail_body(connection)
    print(count)
    print(search_pool)

    #print(connection.list(pattern='*INBOX*'))

    #while True:
        #sys.stdout.flush()
        #time.sleep(60)

if __name__ == '__main__':
    main()