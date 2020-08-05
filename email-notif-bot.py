from datetime import datetime
import imaplib
import sys, json, os
import time
import email
import pygame.mixer as mixer

#load login credentials from credentials.json
def load_credentials():
    filepath = os.path.join(os.getcwd(), './config.json')
    sys.stdout.write("Looking for login credentials at " + filepath + "......")
    try:
        with open(filepath) as f:
            data = json.load(f)
            if 'credentials' in data.keys():
                credentials = data['credentials']
            else:
                raise Exception("Cannot find an object named 'credentials' in config.json.")
            if 'username' in credentials.keys() and 'password' in credentials.keys():
                username = credentials['username'].encode('ascii', 'replace')
                password = credentials['password'].encode('ascii', 'replace')
                sys.stdout.write(' success.\n')
                return (username, password)
            else:
                raise Exception("'credentials' object doesn't have attribute 'username' and/or 'password'. Check config.json.")
    except Exception as e:
        sys.stdout.write(' failed.\n'+ str(e)+'\n')
        sys.stdout.write('Script execution aborted.\n')
        exit()

#open imap connection 
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

#retrieve the body of the latest mail
def get_latest_mail_body(connection):
    try:
        sys.stdout.write('Looking into inbox......')
        connection.select('INBOX', readonly=True)
        typ, ids = connection.search(None, 'ALL') #second parametr specifies the search criterion
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
                sys.stdout.write('The text we will search through came from ' + str(search_pool_src) + ' messages.\n')
                sys.stdout.write('These texts are enclosed by the equal signs:\n=====================\n')
                sys.stdout.write(search_pool + '\n=====================\n')
                return search_pool
        raise Exception('The fetched result probably does not have a tuple in it.')
    except Exception as e:
        sys.stdout.write(' failed.\n' + str(e) + '\n')
        return None

#play some sound at top volume nonstop
def alert(iterations):
    mixer.music.load('notif.mp3')
    mixer.music.set_volume(1)
    mixer.music.play(loops=iterations)

def load_search_phrases():
    filepath = os.path.join(os.getcwd(), './config.json')
    sys.stdout.write("Looking for search phrases at " + filepath + "......")
    try:
        with open(filepath) as f:
            data = json.load(f)
            if 'search_phrases' in data.keys():
                search_phrases = data['search_phrases']
            else:
                raise Exception("Cannot find attribute 'search_phrases' in config.json.")
            if not isinstance(search_phrases, list):
                raise Exception("Attribute 'search_phrases' in the config.json is not a list.")
            elif len(search_phrases) == 0:
                raise Exception("Attribute 'search_phrases' cannot be empty. Enter a phrase to search for.")
            else:
                sys.stdout.write(' success.\n')
                return [phrase.encode('ascii', 'replace') for phrase in search_phrases]
    except Exception as e:
        sys.stdout.write(' failed.\n'+ str(e)+'\n')
        sys.stdout.write('Script execution aborted.\n')
        exit()

def load_alert_iterations():
    filepath = os.path.join(os.getcwd(), './config.json')
    sys.stdout.write("Looking for alert iterations at " + filepath + "......")
    try:
        with open(filepath) as f:
            data = json.load(f)
            if 'alert_iterations' in data.keys():
                alert_iterations = data['alert_iterations']
            else:
                raise Exception("Cannot find attribute 'alert_iterations' in config.json.")
            if not isinstance(alert_iterations, int):
                raise Exception("Attribute 'alert_iterations' in config.json is not an integer.")
            elif alert_iterations < -1:
                raise Exception("Attribute 'alert_iterations' has to be greater than -1.\nNote that setting alert_iterations to 1 plays the alert indefinitely.")
            else:
                sys.stdout.write(' success.\n')
                return alert_iterations
    except Exception as e:
        sys.stdout.write(' failed.\n'+ str(e)+'\n')
        sys.stdout.write('Script execution aborted.\n')
        exit()

def load_search_cycle():
    filepath = os.path.join(os.getcwd(), './config.json')
    sys.stdout.write("Looking for search cycle at " + filepath + "......")
    try:
        with open(filepath) as f:
            data = json.load(f)
            if 'search_cycle' in data.keys():
                search_cycle = data['search_cycle']
            else:
                raise Exception("Cannot find attribute 'search_cycle' in config.json.")
            if not isinstance(search_cycle, int):
                raise Exception("Attribute 'search_cycle' in config.json is not an integer.")
            elif search_cycle < 0:
                raise Exception("Attribute 'search_cycle' has to be greater than 0.")
            else:
                sys.stdout.write(' success.\n')
                return search_cycle
    except Exception as e:
        sys.stdout.write(' failed.\n'+ str(e)+'\n')
        sys.stdout.write('Script execution aborted.\n')
        exit()

def main():
    mixer.init() #initialize the mixer
    #log entry prefix
    now = datetime.now()
    sys.stdout.write("\nNEW RUN STARTING ON " + str(now) + '\n')
    #load things from config.json
    username, password = load_credentials()
    search_phrases = load_search_phrases()
    alert_iterations = load_alert_iterations()
    search_cycle = load_search_cycle()
    #establish connection with server using loaded credentials
    connection = open_connection(username, password)
    while True:
        #retrieve latest email's body
        search_pool = get_latest_mail_body(connection).lower()
        if isinstance(search_pool, str):
            located_phrases = ""
            for phrase in search_phrases:
                if phrase.lower() in search_pool:
                    located_phrases += phrase + ', '
            if len(located_phrases) > 0: #phrases are found
                located_phrases = located_phrases[:-2] #trim the ', '
                sys.stdout.write('Search phrase(s) ' + located_phrases + ' are found in the email body.\n')
                alert(alert_iterations)
                sys.stdout.write('Ringing alarm for ' + str(alert_iterations) + ' iterations.\n')
                while True:
                    if not mixer.music.get_busy(): #if the music stops
                        sys.stdout.write('Alarm shut down.\nTask completed. Goodbye.\n')
                        exit()
        sys.stdout.write('No search phrases found.\n')
        sys.stdout.write('Sleeping for ' + str(search_cycle) + ' seconds before next search.\n')
        time.sleep(60)


    #while True:
        #sys.stdout.flush()
        #time.sleep(60)

if __name__ == '__main__':
    main()