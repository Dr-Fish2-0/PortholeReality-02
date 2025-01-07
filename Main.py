import cv2 as cv
import Triangulation as tri
import numpy as np
import socket

if __name__ == "__main__":

    # Intialize OpenCV video capture and force 1600x600 resolution
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

    #Intialize the object that will get the 3D world coordinates
    posCalc = tri.Triangulator()

    #initialize this to prevent communication errors
    pos = np.zeros((1, 3), np.float32)
    posRaw = np.zeros((1, 4), np.float32)

    # Start the socket server on the loopback address
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 25465))
    print("Started Socket Server")
    s.listen()
    conn, addr = s.accept()  # accept any incoming connections

    # While the connection, perform the communication loop
    with conn:
        while True:

            # Read in the camera video feed and read data from the socket
            # isReturned, frame = cap.read()
            data = conn.recv(2)

            pos, posRaw = posCalc.getPosition(cap)

            # if the bytes 'rr' are received, send back the position
            if data == b'rr':
                conn.send(pos.tobytes())

            # Terminates everything if the "p" key is held down
            if cv.waitKey(1) == ord('p'):
                break

        cap.release()
        cv.destroyAllWindows()
    conn.close()
    s.close()

