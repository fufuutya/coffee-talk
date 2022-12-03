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

class clientMode(Enum):
    REQUEST = auto()
    SEND = auto()
    REGISTER = auto()
    LOGIN = auto()

def GetRequestMSG(senderID, Last_modified_Date)->str:
    msg= clientMode.REGISTER + "\\"
    msg+=senderID + "\\"
    msg+= Last_modified_Date
    return msg;
def GetSendMSG(receiverID, message, date)->str:
    msg = clientMode.SEND + "\\"
    msg += receiverID + "\\"
    msg += date + "\\"
    msg += message;
    
# login session
def GetRegisterMSG(senderID, receiverID, message, date)->str:
    msg = clientMode.REGISTER + "\\"
    msg += senderID + "\\"
def GetLoginMSG(senderID):
    msg = clientMode.LOGIN + "\\"
    msg += senderID + "\\"


#Server protocol
def ParseMode(msg:str):
    splitedMsg = msg.split("\\")
    return splitedMsg[0]
def ParseRequestMSG(msg:str):
    splitedMsg = msg.split("\\");
    senderID = splitedMsg[1]
    last_modified_date = splitedMsg[2];
    return senderID, last_modified_date;
def ParseSendMSG(msg:str):
    splitedMSG = msg.split("\\");
    senderID = splitedMSG[1];
    receiverID = splitedMSG[2];
    dateID = splitedMSG[3];
    message = splitedMSG[4];
    return senderID, receiverID, dateID, message;
def ParseLoginMSG(msg:str):
    splitedMSG = msg.split("\\");
    senderID = splitedMSG[1];
    return senderID;
def ParseRegisterMSG(msg:str):
    splitedMSG = msg.split("\\");
    senderID = splitedMSG[1];
    return senderID;