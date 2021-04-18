# MicroSquad Web UI

The MicroSquad web UI relies on a MQTT broker.

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


## How to develop with Docker

* Create the image
  ```bash
  docker build -t usquad .
  ```
* Start the image
  ```bash
  docker run -it --rm --name usquad -e NGINX_PORT=8080 -e NGINX_CONTEXT_PATH=/ui -v `pwd`/deployment/conf/nginx/templates:/etc/nginx/templates -p 8080:8080 usquad
  ```
* Access the server from your web browser at http://localhost:8080/ui