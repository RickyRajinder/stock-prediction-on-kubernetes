import os
import threading
import socket
import boto3
import pandas as pd

from stocker import Stocker

df = pd.read_csv('companylist.csv')
symbols = list(df.Symbol)
S3_INGESTION_NODE_PORT = 8088
DATA_MODELING_NODE_PORT = 8089
NODE_ADDRESS = '127.0.0.1'


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
        request_symbol = data.decode().strip('\n')
        if request_symbol in symbols:
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
                payload = str(obj['Body'].read()).replace(r'\n', '\n')
                sock = socket.socket()
                sock.connect((NODE_ADDRESS, DATA_MODELING_NODE_PORT))
                sock.send(payload.encode('ascii'))
                s.close()
            else:
                Stocker(ticker=request_symbol).stock.to_csv(request_symbol+'.csv')
                my_bucket.upload_file(request_symbol+'.csv', Key=request_symbol+'.csv')
                os.remove(request_symbol+'.csv')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', S3_INGESTION_NODE_PORT))
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
