# MicroSquad Web UI

The MicroSquad web UI relies on a MQTT broker.

## How to develop the frontend

### Using the maven frontend plugin (preferred method)

* Install Apache Maven 3.6.3+
* Run ```mvn compile``` - this will download and install a local version of Node and NPM
* To run the project from the command line :
  * Execute ```. source-path.sh``` to update your path (on a non-Linux platform, amend the path as indicated in the script)
  * Execute ```npm start``` to run the project

### Using a global node installation

* Install Node v14 or later and NPM v6.14 or later
* Execute ```npm start```

## How to deploy on Openshift

### Preparation steps

* Login to Openshift and switch to your project
* Create a service account for deployment
  * oc create sa usquad-deployer
  * oc policy add-role-to-user admin -z usquad-deployer
* You can now obtain the auth token for that account and use it in your build
  * oc sa get-token usquad-deployer

### Deploy commands


```bash
oc process -p NAMESPACE=microsquad -f deployment/service.yml --local=true | oc apply -f -
```

## How to develop locally with Docker

* Create the image
  ```bash
  docker build -t usquad .
  ```
* Start the image
  ```bash
  docker run -it --rm --name usquad -e NGINX_PORT=8080 -e NGINX_CONTEXT_PATH=/ui -v `pwd`/deployment/conf/nginx/templates:/etc/nginx/templates -p 8080:8080 usquad
  ```
* Access the server from your web browser at http://localhost:8080/ui
## How to set a background image on the Scoreboard

Simply post a base-64 encoded image via mqtt like so :
```
mosquitto_pub -r -t "microsquad/gateway/scoreboard/image" -m "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAJCAYAAAA7KqwyAAAAF0lEQVR42mP8z8BwhoECwDhqwKgBQAAAZaoQLT5kb68AAAAASUVORK5CYII="
```
The website [PNG Pixel](https://png-pixel.com/) is a great help !

