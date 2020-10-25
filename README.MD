# theChallenge
 
 ## Running
 
 To run the solution, please run the bash script: `docker_script.sh`, this builds the image and runs the container. If running on Linux make sure you can run docker without `sudo`. Alternatively you can also run the commands:   
`docker image build --no-cache -t challenge_api .` and `docker run -p 5000:5000 -d challenge_api`

## Testing

 Verify that the container is running and then run the bash script: `api_tests.sh`. This is a bunch of curl get requests to the api endpoints to ensure that the api works. There are 12 tests in total. In addition to the example inputs provided in the docx file, there are also tests for malformed week input format and the case where the sensor_id is not valid.
 
 ## API design
 
 The endpoints are: `/task1/`, `/task2/`, `/task3/`
 
 with query string parameters: `week` and `sensor_id` for task 1 and 2 and `machine_id` for task 3.
 
 Example endpoint for task 1 is:
 `http://127.0.0.1:5000/task1/?week=01/09/2020 12:00 - 08/09/2020 12:00&sensor_id=TEK10'`
 
 In curl the spaces need to be replaced with %20 like so:
 
 `http://127.0.0.1:5000/task1/?week=01/09/2020%2012:00%20-%2008/09/2020%2012:00&sensor_id=TEK10'`
 
 The api should run on localhost with port 5000, so it can be tested further if required.
 
 ## Notes:
 
 Cloud database providers (aws RDS and mongo atlas) were used as database providers. An alternative could have been to install the database servers locally each in their own containers. The containers could then be linked with the api container to allow communication. 
