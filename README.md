[![ci](https://github.com/MaxAnderson95/load-balancer-testing-api/actions/workflows/main.yml/badge.svg)](https://github.com/MaxAnderson95/load-balancer-testing-api/actions/workflows/main.yml)

# Load Balancer Testing API

A basic REST API written in Python using FastAPI that I use for testing load balancers in my day job. It features a separate front-end UI and back-end API that can be run independently or in the same process.

## Running

To run from the command line first install the dependencies: `pip install -r requirements.txt`, then run `python app\main.py`

To run via [docker](https://hub.docker.com/repository/docker/maxanderson95/load-balancer-testing-api) `docker run -it -p 80:80 maxanderson95/load-balancer-testing-api:latest`

You can also deploy the included manifests. This requires a pre-configured ingress controller.
```
kubectl apply -f https://raw.githubusercontent.com/MaxAnderson95/load-balancer-testing-api/main/manifests/deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/MaxAnderson95/load-balancer-testing-api/main/manifests/service.yaml
kubectl apply -f https://raw.githubusercontent.com/MaxAnderson95/load-balancer-testing-api/main/manifests/ingress.yaml
```

## Configuration

You can specify configuration using environment variables.

* To specify the logging level: `API_logging.level="DEBUG"`. The default is `INFO`.

* To specify the instance id (essentially a friendly name for the instance): `API_server.instance_id="HQ-01"`. The default is auto generated.

* To specify the port the server runs on: `API_server.port="8080"`. The default is 80.

* To specify the server "mode": `API_server.mode="FULL"`. The default is `FULL`, and the other options are `UI` and `API`.

## Logging and Data

When a request is made to *any* route, it will respond with a json object in the following format:

```json
{
	"server_details": {
		"server_instance_id": "D2SRCA",
		"server_mode": "API",
		"server_listening_port": 80
	},
	"request_details": {
		"client_ip": "10.1.1.50",
		"x-forwarded-for_header": "172.12.12.12",
		"request_path": "/api/v1"
	}
}
```
Also, an `INFO` level log message will be printed to STDOUT with similar information:

`[2022-03-18 18:01:15,979][main      ][INFO   ] Instance: 'D2SRCA', METHOD: 'GET', PATH: '/testroute' CLIENT: '10.1.1.50', XFF: '172.12.12.12'`

If the word "health" is found anywhere in the request path, the log message will be at `DEBUG` level instead, and the
response object will contain a new key value pair of `"status": "UP`, mimicking the response of the health monitor in
Spring Boot framework.

## Server Modes
Three server modes are available. These are: `API`, `UI`, and `FULL`. They are set using an environment variable with the default being `FULL` if the environment variable is not set.

* When the server is in `API` mode, it simply responds to `GET` and `HEAD` requests at *any* route and returns a sample response.

* When the server is in `UI` mode, it serves a static HTML page and Javascript file. On load, the webpage will attempt to make a call to `/api` and return the `server_instance_id` as text in the HTML body. It will also attempt to get a joke from `/api/joke` which itself gets a joke from a 3rd party joke API.

  Also note, calls with the word `health` anywhere in the path will return a JSON response with a key value pair of `"status": "UP"`, mimicking the response of the health monitor in Spring Boot framework.

* When the server is in `FULL` mode (Fullstack mode), it is the equivalent of having `API` and `UI` mode enabled at the same time.
