"""
Gerbil - Copyright (c) 2015 Michael Franzl

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import time
import socket
import threading
from queue import Queue

from time import sleep


class SocketInterface:
    """Implements opening, closing, writing and threaded reading from a remote socket. Read data are put into a Thread Queue.
    """
    
    def __init__(self, name, host, port=23):
        """Straightforward initialization tasks.
        
        @param name
        An informal name of the instance. Useful if you are running
        several instances to control several serial ports at once.
        It is only used for logging output and UI messages.
        
        @param host
        The host to connect to.
        
        @param port
        The port to connect to.
        """
        
        self.name = name
        self.host = host
        self.port = port
        self.queue = None
        self.logger = logging.getLogger("gerbil.interface")
        
        self._buf_receive = ""
        self._do_receive = False
        
    def start(self, queue):
        """
        Open the socket and start a Thread for reading.
        
        @param queue
        An instance of Python3's `Queue()` class.
        """
        self.queue = queue
        
        self.logger.info("%s: connecting to %s:%i", self.name, self.host, self.port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self._do_receive = True
        self.socket_thread = threading.Thread(target=self._receiving)
        self.socket_thread.start()
        
    def stop(self):
        """
        Close the device node and shut down the reading Thread.
        """
        self._do_receive = False
        self.logger.info("%s: stop()", self.name)
        self.socket_thread.join()
        self.logger.info("%s: JOINED thread", self.name)
        self.logger.info("%s: Closing socket", self.name)
        self.socket.close()
        
    def write(self, data):
        """
        Write `data` to the socket. If data is empty, no write is performed. The number of written characters is returned.
        """
        if len(data) > 0:
            num_written = self.socket.send(bytes(data,"ascii"))
            return num_written
        else:
            self.logger.debug("%s: nothing to write", self.name)


    def _receiving(self):
        while self._do_receive == True:
            data = self.socket.recv(1)
            self._handle_data(data)

    def _handle_data(self, data):
        try:
            asci = data.decode("ascii")
        except UnicodeDecodeError:
            self.logger.info("%s: Received a non-ascii byte. Probably junk. Dropping it.", self.name)
            asci = ""
            
        for i in range(0, len(asci)):
            char = asci[i]
            self._buf_receive += char
            # not all received lines are complete (end with \n)
            if char == "\n":
                self.queue.put(self._buf_receive.strip())
                self._buf_receive = ""

#q = Queue()
#si = SocketInterface("foo", "10.1.1.5", 23)
#si.start(q)
#sleep(5)
#si.write("?\n")
#while True:
#    data = q.get()
#    print(data)
