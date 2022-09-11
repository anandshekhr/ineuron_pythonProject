import mysql.connector as conn


class mysqlConnection:
    """
    Class for mysql query selection, table creation, table schema
    
    Keyword arguments:
    hostname -- hostname of mysql
    username -- username of mysql user
    password -- password"""
    
    def __init__(self,hostname: str,username: str, password: str):
        self.hostname = hostname
        self.username = username
        self.password = password
        
    def mydbConnect(self):
        """
        Connection to MySQL Database
        Return: connection string to console
        """
        try:
            self.mydb = conn.connect(host= self.hostname,user= self.username,passwd = self.password)
            return self.mydb
        except:
            return "Not connected"
        
    def createdatabase(self,dbname: str):
        """
        Create new Database in MySQL, if does not exists previously in mysql. No two databases can have one name. 
        
        Keyword arguments:
        dbname -- as unique name for the database
        Return: True if success(if created a new database)
                Existed,True (if database not created because it existed previously, use given database if existed)
        """
        
        
        try:
            self.cursor = self.mydb.cursor()
            self.cursor.execute("create database IF NOT EXISTS {}".format(dbname))
            self.cursor.execute('use {}'.format(dbname))
            return True
        
        except:
            self.cursor.execute('use {}'.format(dbname))
            return ("Existed",True)
        
    
    def createtablewithschema(self,args,tablename):
        """
        Create Table in the database with given schemas as arguments
        
        Keyword arguments:
        args  = Schemas for table enclosed in parenthesis as single string
        tablename  = tablename
        Return: True if success
        """
        try:
            self.cursor.execute('create table {} {}'.format(tablename,args))
            self.mydb.commit()
            return True
        except:
            return ("something went wrong in MySQL")
    
    def drop(self,dbname = None,tname = None):
        """
        Drop extra table or Database created. 
        
        Keyword arguments:
        dbname -- Name of the Database to be deleted (Optional)
        tname -- Name of the Table to be deleted (Optional)
        Return: True if success
        """
        
        if dbname is not None:
            try:
                self.cursor.execute("drop database {}".format(dbname))
                return True
            except:
                return "Database does not exists"
        
        elif tname is not None:
            try:
                self.cursor.execute("drop table IF EXISTS {} RESTRICT".format(tname))
                return True
            except:
                return "Table does not exists"
        else:
            pass
        
    def insertintotable(self,tablename,values):
        """
        insert values into table, keep values as single string enclosed with parentheses
        
        Keyword arguments:
        tablename -- as table name
        values -- as values to be inserted for single row
        Return: True if success
        """
        try:
            self.cursor.execute("insert into {} values {}".format(tablename,values))
            self.mydb.commit()
            return True
        
        except:
            return ("something went wrong in MySQL")
    
    def mysqlcommands(self,command: str):
        """
        for any other command used in mysql, just enter the command string format 
        
        Keyword arguments:
        command -- mysql command in single string 
        Return: values returned
        """
        try:
            self.cursor.execute(command)
            self.mydb.commit()
            return True
        
        except:
            return ("something went wrong in MySQL")