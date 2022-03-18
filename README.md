# Load Balancer Testing API

A REST API written in Python using FastAPI that I use for testing load balancers in my day job.

## Running

To run from the command line, simply run `python app\main.py`

Or run via docker `docker run -it -p 80:80 maxanderson95/lb-testing-api:latest`

## Configuration

You can specify configuration using environment variables.

To specify the logging level: `APP_logging.level="DEBUG"`. The default is `INFO`.

To specify the instance id (essentially a friendly name for the instance): `APP_server.instance_id="HQ-01"`. The default is auto generated.

To specify the port the server runs on: `APP_server.port="8080"`. The default is 80.

### Logging and Data

When a request is made to *any* route, it will respond with a json object in the following format:

```json
{
  "Client IP": "10.1.1.50",
  "Requested Path": "/testroute",
  "Server Instance ID": "HQ-01",
  "x-forwarded-for Header": "172.12.12.12"
}
```

Also, an `INFO` level log message will be printed to STDOUT with similar information:

`[2022-03-18 18:01:15,979][main      ][INFO   ] METHOD: 'GET', PATH: '/testroute' CLIENT: '10.1.1.50', XFF: '172.12.12.12'`

If the word "health" is found anywhere in the request path, the log message will be at `DEBUG` level instead, and the
response object will contain a new key value pair of `"status": "UP` mimicking the response of the health monitor in
Spring Boot framework.