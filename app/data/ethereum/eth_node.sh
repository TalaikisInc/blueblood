# docker pull ethereum/client-go

docker run -d --name ethereum-node -v /home/ethereum:/root \
    -p 8545:8545 -p 30303:30303 \
    ethereum/client-go --syncmode light --cache=1024
