import dropbox
import sqlite3 as sqlite
from pathlib import Path
from cockroach import developing_cockroach as dev

class Server:
    '''Class responsible for server calls and provision of some services, such as returning user data on the server.
     REQUIRED PARAMETERS: token (server access token. set it in .env)
                             yourLocalForlder (your data writing location. Where it will be stored)
                             link (serverlink and endpoint)
     These are the minimum parameters for script execution.
     Some parameters like:
                             viewConnectorSignal (Receives True or False. Responsible for showing the CONNECTOR sign, if it is equal to 1 or equal to 0)
                             dowloadDb (receives "n" or something different like "y" from yes and no. Responsible for handling the CONNETOR error equal to 0.)
    '''
    def __init__(self, token, yourLocalFolder, link, viewConnectorSignal = True, dowloadDb = 'n') -> None:
        self.dowloadDb = dowloadDb # parameter responsible for checking if a succession of CONNECTOR = 0 occurs, that it tries to correct such error by itself.
        self.token = token # server access token.
        self.yourLocalFolder = yourLocalFolder # your writing location.
        self.link = link # server link and endpoint.
        self.dbx = dropbox.Dropbox(self.token) # creating a dropbox object called dbx.

        self.connect = False # initializing self.connect, responsible for handling and returning some exceptions.
        self.localHost = "./app/core/data/users/data.db" # setting my recording location. (standard)
        
        if Path(r"{}".format(self.localHost)).is_file():# checking if such a file exists and returning a Boolean, True or False value and based on that making a decision.
        
            self.__cursor = sqlite.connect(self.localHost).cursor() # creating a cursor instance.
            self.connect = True 
            if viewConnectorSignal: dev.log(name = "CONNECTED", message= "CONNECTOR RETORNANDO SINAL 1")
        
        else: # if the return of the "if" condition equals False, then it will take that path.
            if self.dowloadDb != 'n':

                # if viewConnectorSignal is True, print/print connector log.
                if viewConnectorSignal: dev.log(name = "CONNECTION FAIL", message= "CONNECTOR RETORNANDO SINAL 0")  
                self.tryToDownloadTheDatabase = input("The connector returned the 0 signal, it can be the case that you do not have a " + "\033[33m{}\033[0m".format(self.localHost) + " file on your local machine with the required iformatio. To try to solve the problem, download the file to the remote server? (y/n): ")

                if self.tryToDownloadTheDatabase == "y": # If a CONNECTOR exception of 0 occurs, ask if you want to download the .db file.

                    with open(yourLocalFolder, "wb") as file:
                        metadata, res = self.dbx.files_download(path= self.link)
                        file.write(res.content)
                        dev.log('successfully downloaded.')
                else: 
                    ...
        
        
    # method responsible for getting users on the server.
    def get_users(self):

        if self.connect: # by checking the connector value first.
            users = []
            for user in self.__cursor.execute("SELECT * FROM Users").fetchall():
                users.append(user)
            return users
        else: 
            return "\nSOMETHING UNEXPECTED HAPPENED."

    # method responsible for returning the names of tables in the database.
    def get_tables(self):
        
        if self.connect: # by checking the connector first.
            tables = []
            for data in self.__cursor.execute(("SELECT name FROM sqlite_master WHERE type='table';")).fetchall():
                tables.append(data)
            return tables
        else:
            return "\nSOMETHING UNEXPECTED HAPPENED."

    # whereIsTheFile = 'upload/new_image_test.png'. File on your local machine
    # pointThePathOnTheServer = serverPath/... . Path on server. [serverLink + endPoint/nameOfYourFile.exemple]
    #method responsible for uploading some file to the server.
    def upload_allFiles(self, whereIsTheFile, pointThePathOnTheServer):
        self.dbx.files_upload(open(whereIsTheFile, 'rb').read(), pointThePathOnTheServer)
        
        return "done..."
    
# ...