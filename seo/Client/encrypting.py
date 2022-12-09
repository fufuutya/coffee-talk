import rsa
import chatMsgList
def encryptMSG(msg: str, targetID):
    message = msg.encode('utf8');
    message = rsa.encrypt(message, chatMsgList.idList[targetID]);
    message = message.decode('unicode_escape')
    return message
def decryptReceiveMsg(msg:str, senderID):
    message = msg.encode('ISO-8859-1');
    message = rsa.decrypt(message, chatMsgList.private_key);
    message = message.decode('utf8')
    return message
def key2string(key):
    return key.save_pkcs1().decode('utf8');
def string2pirvatKey(string):
    byteForm = bytes(string, 'utf-8')
    return rsa.PrivateKey.load_pkcs1(byteForm);
def string2PublicKey(string):
    byteForm = bytes(string, 'utf-8')
    return rsa.PublicKey.load_pkcs1(byteForm);
    