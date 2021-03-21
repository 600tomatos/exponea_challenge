# Exponea Challenge


### Prerequisites


To simplify the work with the repository, 
all basic commands are grouped using bash scripts and can be run using the make utility.

Make is installed by default on Unix systems such as Ubuntu or Mac

To execute the command, simply type `make <command>` in the terminal

|   command	|  description   	|
|---	|---	|
|  init	|  Install the necessary dependencies for local development and deployment. |
|  local 	|   Start local development server (without docker)	|
|  run 	|   Start production ready server based on docker and gunicorn using docker-compose.	|
|  docker 	|   Start production ready server based on docker and gunicorn using docker (I'd suggest using make run)	|
|  test 	|   Run local tests.   |
|  exec_docker & clean 	|   Internal commands which I used for debugging	|

### Getting started

If you want to use local server then use `make init` command in order to install all necessary dependencies.
If you want to start using more efficient server then use `make run` to build application for docker.

It is worth to consider testing perfomance for server, which is running inside docker rather then local server,
Since first one is managed by gunicorn 
and it takes the very best by using multiple threads as well as asynchronous coroutines for better performance.

Before you start you need to have the following software installed on your PC:
* docker
* docker-compose (optionally, you can use `make docker` to build and run container purely with docker)
* python >= 3.7 (optionally,  you need python only if you want to start local server without docker)

### Big Picture

I've used standard consumer/producer approach to design all endpoints.

In each of the endponts, as a rule, 3 producers are launched,
which make requests to the third part api and then put the results of execution to a common queue.
Consumer pulls results from this queue and, depending on the conditions, can cancel further execution of producers.

### API and Swagger

! Server use port 5000.

Server has auto-generated documentaton based on swagger.
After server started go to http://0.0.0.0:5000 with your browser in order to use swagger console.

Feel free to test API with help of swagger console or use tools like Postman. Cors are disabled for API.


![Alt text](images/swagger.jpg?raw=true "Title")


### Tests

Some tests were also implemented that cover the basic functionality of these endpoints.
All test use the pytest library. To run the tests, use the command `make test` or simply `pytest`.

The `make test` command is a wrapper around 
the `pytest`command and it checks if the local server is running and other
 small details before executing the tests.
