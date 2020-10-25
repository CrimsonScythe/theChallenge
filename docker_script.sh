docker image build --no-cache -t challenge_api .
docker run -p 5000:5000 -d challenge_api