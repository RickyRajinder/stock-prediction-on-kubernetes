echo $AWS_ACCESS_KEY_ID
docker build --build-arg AWS_SECRET_KEY=$AWS_SECRET_KEY --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -t rickywraith/stock-predict-dm:latest -t rickywraith/stock-predict-dm:$SHA -f ./Data_Model_Dockerfile .
docker build --build-arg AWS_SECRET_KEY=$AWS_SECRET_KEY --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -t rickywraith/stock-predict-s3:latest -t rickywraith/stock-predict-s3:$SHA -f ./S3_Dockerfile .
docker build -t rickywraith/stock-predict-ws:latest -t rickywraith/stock-predict-ws:$SHA -f ./Webserver_Dockerfile .
docker push rickywraith/stock-predict-dm:latest
docker push rickywraith/stock-predict-s3:latest
docker push rickywraith/stock-predict-ws:latest
docker push rickywraith/stock-predict-dm:$SHA
docker push rickywraith/stock-predict-s3:$SHA
docker push rickywraith/stock-predict-ws:$SHA
kubectl apply -f .
kubectl set image deployments/data-model data-model=rickywraith/stock-predict-dm:$SHA
kubectl set image deployments/s3-service s3-service=rickywraith/stock-predict-s3:$SHA
kubectl set image deployments/web-server web-server=rickywraith/stock-predict-ws:$SHA
