from datetime import datetime
import sys, json

def main():
    #log entry prefix
    now = datetime.now()
    sys.stdout.write("\nNEW RUN STARTING ON " + str(now) + '\n')
    while True:
        sys.stdout.flush()

if __name__ == '__main__':
    main()