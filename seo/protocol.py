from enum import Enum, auto

# update!!!
#Client protocol
#  data = {
#     'mode': 'login',
#     'client_id': 'client1',
#     'logined': True,
#     'requested': True,
#     'sent': True, #there is receiverID in customer list
#     'receiver_id': 'client2',
#     'messages': 'date\\text\\hello | date\\<type of msg, image, text, video>\\hi...',
# }
# send_msg = json.dumps(data) # convert dict to str by json
# read data by json.loads()