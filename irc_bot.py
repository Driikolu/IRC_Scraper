#!/usr/bin/python3

import socket
import time

class IRCbot:
    '''
    A simple IRC bot that connects to a given server (NO SSL for the moment)

    Attributes :
        server: A string representing server address (IP or DNS)
        port: An integer representing the server port
    '''

    def __init__(self, server="127.0.0.1", port=6666, botname="irc_scrapper_bot"):
        '''
        The IRC bot constructor
        By default the server will be 127.0.0.1:6666

        Return an IRCbot object with server *server* and port *port*
        '''
        self._server = server
        self._port = port
        self._name = botname
        self._socket = None


    def set_server(self, server):
        '''
        Set the IRCbot server

        Attributes :
            server: A string representing server adress (IP or DNS)
        '''
        self._server = server


    def get_server(self):
        '''
        Give the IRCbot server

        Return a String
        '''
        return self._server


    def set_port(self, port):
        '''
        Set the IRCbot port

        Attributes :
            port: An integer representing the server port
        '''
        self._port = port

    
    def get_port(self):
        '''
        Give the IRCbot server port

        Return an integer
        '''
        return self._port

    
    def set_botname(self, name):
        '''
        Set the IRCbot name

        Attributes :
            name: A string representing the botname
        '''
        self._name = name


    def get_botname(self):
        '''
        Give the IRCbot name

        Return a string
        '''
        return self._name


    def send(self, message):
        '''
        Send a given message through the socket

        Attributes:
            message: A string
        '''
        self._socket.send((message+"\n").encode())

    
    def read(self, size=2048):
        '''
        Read *size* byte in the socket

        Attributes:
            size: An integer

        Return a string
        '''
        return self._socket.recv(size).decode()

    def connect_server(self):
        '''
        Connect the IRCbot to its attached server
        '''
        self._socket = socket.socket()
        try:
            self._socket.connect((self.get_server(), self.get_port()))
            self.send("PASS foo")
            self.send("NICK %s" % self.get_botname() )
            self.send("USER IRC_Scrapper  %s foo bar" % self.get_server() )
            time.sleep(1)
            output=self.read(4096) #Nothing to do with that for the moment
            
            print(output) #Debug
            
            if "PING" in output:
                ping_value = output.split("PING :")[1].split('\n')[0]
                self.send("PONG :%s" % ping_value)
                time.sleep(1)
                output = self.read(4096) #Still nothing to do

            print(output) #Debug again

            print("The bot %s is connected to the server %s" % (self.get_botname(), self.get_server()))

        except ConnectionRefusedError as e:
            print("The connection of the bot %s to %s on port %d as failed" % (self.get_botname(), self.get_server(), self.get_port()))
            raise e



    def disconnect(self):
        '''
        Disconnect the IRCbot of the server
        '''
        self._socket.close()
        self._socket = None


    def is_up(self):
        '''
        Check if socket is set

        Return a Boolean
        '''
        if self._socket==None:
            return False
        else:
            return True


    def join_chan(self,chan="#testbotscraper"):
        '''
        Join the given channel

        Attributes :
            chan: A String ( e.g. "#Help" )
        '''
        if not self.is_up():
            raise Exception("The IRCbot isn't connected to its server")

        else:
            try:
                self.send("JOIN %s" % chan)
                
                output = self.read()

                while "End of /NAMES list." not in output: #Usual message after joining a chan
                    output = self.read()

            except Exception as e:
                print("The bot %s can't connect to the channel %s" % (self.get_botname(), chan))
                raise e


    def scrap(self,keyword_lst):
        '''
        Look for a given list of keyword

        Attributes:
            keyword_lst: A list of string
        '''
        while True:
            
            output = self.read()
            
            for kw in keyword_lst:
                if kw in output:
                    print("A message with the keyword %s has been read ! Look at this :\n%s" % (kw, output))
