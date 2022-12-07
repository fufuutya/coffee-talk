import datetime

# OPTIONAL FUNCTION
def convert_yesno_to_bool(yesno): # convert yes/no to boolean
    if yesno == 'y':
        return True
    elif yesno == 'n':
        return False
    else:
        print('Invalid input')
def agotime(days): # convert ago time to datetime 
    today = datetime.datetime.now()
    ago = today - datetime.timedelta(days=days)
    return ago.date() # return to datetime format not string or number