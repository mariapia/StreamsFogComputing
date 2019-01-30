import socketserver
import threading
import pickle
import struct

from settings import CLOUD_HOST, FOG_PORT


def most_common(text):
    """
    This function show the 10 most common words, namely the words with the max occurrences.
    :param text: all the words with their occurrences
    """
    sorted_pairs = sorted([(k, v) for k, v in text.items()], key=lambda x: x[1], reverse=True)
    most_used = sorted_pairs[:10]
    print(*most_used, sep="\n")
    print("\n\n\n\n")


def aggregate(text, aggregated):
    """
    This functions aggregates the messages received by each FogNode creating a unique list with all the words and their
    occurrences.

    :param text: the most recent message received by the CloudNode
    :param aggregated: the texts already aggregated
    :return: the list with the aggregated words updated
    """
    for k, v in text.items():
        if k in aggregated:
            aggregated[k] = aggregated[k] + v
        else:
            aggregated[k] = v
    return aggregated


class FogToCloudServer(socketserver.BaseRequestHandler):
    """
    The FogtoCloudServer is the server that handles the connection with the FogNodes.
    It receives from a FogNode a list with the words and their occurrences and calls the function that aggregates all
    the messages and the function that finds the 10 most common words.
    """

    def setup(self):
        pass

    def handle(self):
        global aggregated
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
            #print("Reading message from " + str(self.client_address))
            text_data = data[:msg_size]
            data = data[msg_size:]

            text = pickle.loads(text_data)

            aggregated = aggregate(text, aggregated)

        most_common(aggregated)

    def finish(self):
        print("All text received. Connection ended.")


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def cloud_main():
    try:
        global aggregated
        global TDC_servers
        global TDC_server_threads

        TDC_servers = []
        TDC_server_threads = []
        aggregated = {}

        TDC_servers.append(ThreadedServer((CLOUD_HOST, FOG_PORT), FogToCloudServer))

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
