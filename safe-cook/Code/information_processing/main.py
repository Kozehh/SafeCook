import zmq
from traitement import DataManager
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--obj_Path", required=True,
                    help="The path to the obj.names file")
    args = vars(ap.parse_args())

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:1234")
    dm = DataManager(args["obj_Path"])
    while True:
        #  Wait for next request from client
        message = socket.recv_string()
        dataset = dm.stringToData(message)
        overlapDict = dm.findObjOverlap(dataset)

        # TODO: Choose what information is worth sending to kafka
        # TODO: sendMsgOrDataToKafka

        #Meanwhile we will print an example of the results
        outputMsg = dm.writeOutputMsg(overlapDict)
        print(outputMsg)

        #  Send reply back to client
        socket.send(b"Ok")
main()
