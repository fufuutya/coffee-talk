from datetime import datetime, timedelta

# OPTIONAL FUNCTION
def convert_yesno_to_bool(yesno): # convert yes/no to boolean
    if yesno == 'y':
        return True
    elif yesno == 'n':
        return False
    else:
        print('Invalid input')
def agotime(days): # convert ago time to datetime 
    today = datetime.now()
    ago = today - timedelta(days=days)
    ago = ago.date()
    return ago.strftime('%Y-%m-%d') # return date to string
def convert_string_to_date(string): # convert string to date
    return datetime.strptime(string, '%Y-%m-%d').date()