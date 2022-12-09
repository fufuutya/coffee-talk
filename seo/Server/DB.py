import pymssql
import pyodbc
import selectors
import datetime as DT

communcationTableName = "communcationList"
IDTableName = "IDList"

def stringFormatting(target:str)->str:
    return '\'' + str(target) + '\''
def valueFormatting(targets)->str:
    returnString = "values("
    for value in targets:
        returnString += stringFormatting(value) + ","
    returnString = returnString.removesuffix(',');
    returnString += ')'
    return returnString;


class Database():    
    def connectToSQLServer(self):
        hostName = ".\\CoffeeTalk"
        hostIP = "127.0.0.1"
        userName = "LAPTOP-OJISGB18\\USER"
        defaultDatabase = "CoffeeTalk"
        cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=LAPTOP-OJISGB18\COFFEETALK;"
            "Database=CoffeeTalk;"
            "UID=CoffeeTalkServer;"
            "PWD=coffee;"
            "Trusted_Connection=yes;")
        conn = pyodbc.connect(cnxn_str)
        return conn
    def __init__(self) -> None:
        self.connection = self.connectToSQLServer();
        self.cursor = self.connection.cursor();
        self.cursor.execute("use CoffeeTalk")
    def isIDExist(self, ID)->bool:
        if self.getIDInfo(ID) == None:
            return False;
        else : 
            return True;
    def getIDInfo(self,ID):
        executeStatement = '''
        SELECT *
        FROM UserList
        WHERE UserID = \'''' + ID + '\''
        self.cursor.execute(executeStatement);
        data = self.cursor.fetchall();
        if len(data) == 0:
            return None;
        else:
            IDdict = {}
            IDdict["id"] = data[0][0];
            IDdict["pass_word"] = data[0][1];
            IDdict["public_key"] = data[0][2];
            return IDdict;
    def addID(self,ID, pass_word, public_key)->bool:
        executeStatement = "INSERT INTO UserList " +\
        valueFormatting([ID, pass_word, public_key])
        print(executeStatement)
        if self.isIDExist(ID):
            return False;
        else:
            self.cursor.execute(executeStatement)
            self.connection.commit();
            return True
    def addMessage(self, senderID, receiverID, message, dateTime)->bool:
        message = message.encode('unicode_escape');
        executeStatement = "INSERT INTO communicationList (senderID, receiverID, communicationMSG, communicationDateTime) values (?,?,?,?)"
        params = (senderID, receiverID, pyodbc.Binary(message), DT.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S'))
        self.cursor.execute(executeStatement,params);
        self.connection.commit();
    def getMessageFor(self, receiverID, latestDateTimeReceived):
        executeStatement = '''
        SELECT *
        FROM communicationList
        WHERE receiverID = ''' + stringFormatting(receiverID) +\
        "and communicationDateTime >" + stringFormatting(latestDateTimeReceived)
        self.cursor.execute(executeStatement);
        data = self.cursor.fetchall()
        for letter in data:
            letter[2] = letter[2].decode('unicode_escape');
        return data;
        