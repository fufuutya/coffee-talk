import pymssql
import pyodbc
import selectors

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
        executeStatement = '''
        SELECT COUNT(1)
        FROM UserList
        WHERE UserID = \'''' + ID + '\''
        self.cursor.execute(executeStatement);
        data = self.cursor.fetchall();
        if data[0][0] == 0:
            return False;
        else:
            return True
    def addID(self,ID, UserName)->bool:
        executeStatement = "INSERT INTO UserList " +\
        valueFormatting([UserName, ID])
        print(executeStatement)
        if self.isIDExist(ID):
            return False;
        else:
            self.cursor.execute(executeStatement)
            self.connection.commit();
            return True
    def addMessage(self, senderID, receiverID, message, dateTime)->bool:
        executeStatement = "INSERT INTO communicationList " +\
        valueFormatting([senderID,receiverID, message, dateTime]);
        self.cursor.execute(executeStatement);
        self.connection.commit();
    def getMessageFor(self, receiverID, latestDateTimeReceived):
        executeStatement = '''
        SELECT *
        FROM communicationList
        WHERE receiverID = ''' + stringFormatting(receiverID) +\
        "WHERE communicationDate >=" + stringFormatting(latestDateTimeReceived)
        data = self.cursor.fetchall()
        return data;
        