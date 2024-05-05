#!/bin/bash
wget https://vpa2a.s3.ap-southeast-1.amazonaws.com/sample.wav
curl -X POST -H 'Content-Type: application/json' --data '{"input": "sample.wav"}' http://localhost:5000