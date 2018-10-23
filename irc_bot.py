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


    def connect_server(self):
        '''
        Connect the IRCbot to its attached server
        '''
        self._socket = socket.socket()
        try:
            self._socket.connect((self.get_server(), self.get_port()))
            self._socket.send( b"PASS foo\n" )
            self._socket.send( ( "NICK %s\n" % self.get_botname() ).encode() )
            self._socket.send( ( "USER IRC_Scrapper  %s foo bar\n" % self.get_server() ).encode() )
            time.sleep(1)
            self._socket.recv(2048).decode()
            
            print("The bot %s is connected to the server %s" % (self.get_botname(), self.get_server()))
            
        except ConnectionRefusedError as e:
            print("The connection of the bot %s to %s on port %d as failed" % (self._name, self._server, self._port))



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


    def join_chan(self,chan="#help"):
        '''
        Join the given channel

        Attributes :
            chan: A String ( e.g. "#Help" )
        '''
        if not self.is_up():
            raise Exception("The IRCbot isn't connected to its server")

        else:
            pass
