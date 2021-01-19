import os
import threading
import socket
from datetime import datetime, timedelta

import boto3

from stocker import Stocker

REDIS_SERVICE = 'redis-service'
DM_SERVICE = 'data-model'
DM_PORT = 8080
S3_SERVICE_PORT = 8080


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
        resource = boto3.resource('s3')
        my_bucket = resource.Bucket('elasticbeanstalk-us-west-1-643247086707')
        objs = list(my_bucket.objects.filter(Prefix=''))
        files = list()
        for obj in objs:
            _, filename = os.path.split(obj.key)
            files.append(filename)
        if request_symbol+".csv" in files:
            obj = s3_client.get_object(Bucket='elasticbeanstalk-us-west-1-643247086707', Key=request_symbol+'.csv')
            lastUpdated = obj['LastModified']
            if datetime.now() - lastUpdated.replace(tzinfo=None) >= timedelta(days=7):
                Stocker(ticker=request_symbol).stock.to_csv(request_symbol + '.csv')
                my_bucket.upload_file(request_symbol + '.csv', Key=request_symbol + '.csv')
                os.remove(request_symbol + '.csv')
        else:
            Stocker(ticker=request_symbol).stock.to_csv(request_symbol+'.csv')
            my_bucket.upload_file(request_symbol+'.csv', Key=request_symbol+'.csv')
            os.remove(request_symbol+'.csv')
        sock = socket.socket()
        sock.connect((DM_SERVICE, DM_PORT))
        msg = requestID+","+request_symbol+","+days_into_future
        sock.send(msg.encode('ascii'))
        sock.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', S3_SERVICE_PORT))
    s.listen()
    while True:
        client, address = s.accept()
        client.settimeout(60)
        threading.Thread(target=listenToClient, args=(client,)).start()


receive()

# stock_name = 'MSFT'
# # stock = Stocker('MSFT', 'CSV', '.')

# model, future = stock.create_prophet_model(days=50, resample=False)
# model.plot_components(future)
#
#
# # stock.plot_stock(start_date=None, end_date=None, stats=['Adj. Close'], plot_type='basic')
