import socket
import pickle
import struct
import random


from settings import FOG_HOST, EDGEPORTS


def send_text(text):
    """
    This function is used to send the text to the FogNode.
    The Edge device tries to connect to a random FogNode randomly selecting a port. If it successes then it establishes
    the connection with this FogNode and sends the text. Otherwise, it tries with another FogNode.

    :param text: the path of the text that the Edge device collects. For simplicity, in this emulation the text is read
    from a text file.
    """
    fogSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    found = False
    while not found:
        try:
            EDGE_PORT = random.choice(EDGEPORTS)
            fogSocket.connect((FOG_HOST, EDGE_PORT))
            found = True
        except:
            continue

    data = pickle.dumps(text)
    text = struct.pack("L", len(data)) + data

    fogSocket.sendall(text)
    print("I'm sending to " + FOG_HOST + " on port " + str(EDGE_PORT))

    fogSocket.shutdown(1)
    fogSocket.close()


def edge_main(text, n):
    """
    This is the main of the EdgeTextGenerator. It opens the input text file, splits it based on its lines and calls the
    function to send the first n lines of the text.

    :param text: the path of the input text file.
    :param n: the number of lines that the Edge device wants to read and to send.
    """
    with open(text, "r") as f:
        lines = f.read().splitlines()

    send_text(lines[:n])

