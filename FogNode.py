import socketserver
import threading
import re
import pickle
import struct
import socket
import sys

import nltk
nltk.download("stopwords")

from nltk.corpus import stopwords

from collections import Counter
from settings import FOG_HOST, EDGEPORTS, CLOUD_HOST, FOG_PORT


def wordcount(text):
    """
    The functions counts the occurrences of each word in the text

    :param text: text to process
    :return: a list with pairs composed by (word, occurrences)
    """
    complete_text = " ".join(text)
    for c in ".,;-_!?()/%$'£*+#@":
        complete_text = complete_text.replace(c, " ")

    complete_text = re.sub("\s\s+", " ", complete_text)
    complete_text = complete_text.lower()
    words = complete_text.split(" ")

    filtered_text = [word for word in words if word not in stopwords.words('english')]

    res = Counter(filtered_text)
    return res


def send_counts(counts):
    """
    The function opens a connection with the CLOUD_HOST and sends to it the list with the words and their occurrences.

    :param counts: list with the pairs (word, occurrences)
    """
    cloudSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cloudSocket.connect((CLOUD_HOST, FOG_PORT))

    data = pickle.dumps(counts)
    message = struct.pack("L", len(data)) + data

    cloudSocket.sendall(message)
    print("I'm sending to " + CLOUD_HOST + " on port " + str(FOG_PORT))

    cloudSocket.shutdown(1)
    cloudSocket.close()


class EdgeToFogServer(socketserver.BaseRequestHandler):
    """
    The EdgeToFogServer is the server that handles the connection with the EdgeNodes.
    It receives from an edge a list of texts, processes it and calls the functions to count the occurrences of each
    word in the text and the function that sends the message to the CloudHost.
    """
    def setup(self):
        pass

    def handle(self):
        text = None

        data = b""
        payload_size = struct.calcsize("L")
        while True:
            break_stream = False
            while len(data) < payload_size:
                tmp = self.request.recv(4096)
                if not tmp:
                    break_stream = True
                    break
                data += tmp
            if break_stream:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.request.recv(4096)
            print("Reading message from " + str(self.client_address))
            text_data = data[:msg_size]
            data = data[msg_size:]

            text = pickle.loads(text_data)

        if text:
            counts = wordcount(text)
            send_counts(counts)

    def finish(self):
        print("All text received. Connection ended.")


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def fog_main():
    try:
        global TDC_servers
        global TDC_server_threads

        TDC_servers = []
        TDC_server_threads = []

        found = False
        for i in range(len(EDGEPORTS)):
            try:
                EDGE_PORT = EDGEPORTS[i]
                print("Trying to connect at port: " + str(EDGE_PORT))
                TDC_servers.append(ThreadedServer((FOG_HOST, EDGE_PORT), EdgeToFogServer))
                found = True
                break
            except:
                continue

        if not found:
            sys.exit(0)
        print("Connection open at port " + str(EDGE_PORT))

        for TDC_server in TDC_servers:
            TDC_server_threads.append(threading.Thread(target=TDC_server.serve_forever))

        for TDC_server_thread in TDC_server_threads:
            TDC_server_thread.setDaemon(True)
            TDC_server_thread.start()

        for TDC_server_thread in TDC_server_threads:
            TDC_server_thread.join()
    finally:
        print('quitting servers')

        for TDC_server in TDC_servers:
            TDC_server.server_close()
