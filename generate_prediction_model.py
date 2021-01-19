import os
import threading
import socket
import boto3
import redis

from stocker import Stocker
REDIS_SERVICE = 'redis-service'
DM_SERVICE = 'data-model'
DM_PORT = 8080

r = redis.Redis(host=REDIS_SERVICE)


def receive():
    BUFFER = 1024

    def listenToClient(client):
        data = bytearray()
        while True:
            datachunk = client.recv(BUFFER)
            if not datachunk:
                break
            data += datachunk
        client.close()
        data = data.decode().strip('\n').replace(" ", "").split(",")
        requestID = data[0]
        request_symbol = data[1]
        days_into_future = data[2]
        s3_client = boto3.client('s3')
        obj = s3_client.get_object(Bucket='elasticbeanstalk-us-west-1-643247086707', Key=request_symbol+'.csv')
        payload = str(obj['Body'].read()).replace(r'\n', '\n')
        with open(request_symbol+".csv", 'w') as f:
            f.write(payload)
        stock = Stocker(request_symbol, 'CSV', '')
        predicted_price = stock.create_prophet_model(days=int(days_into_future), resample=False, symbol=request_symbol, requestID=requestID)
        graph = open(request_symbol+"_"+requestID+".png", "rb").read()
        os.remove(request_symbol+'.csv')
        r.set(request_symbol+"_"+requestID, graph)
        os.remove(request_symbol+"_"+requestID+".png")
        r.set(request_symbol+"_price_"+requestID, predicted_price)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', DM_PORT))
    s.listen()
    while True:
        client, address = s.accept()
        client.settimeout(60)
        threading.Thread(target=listenToClient, args=(client,)).start()


receive()
