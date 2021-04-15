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

Publish the Web UI NGINX configuration template as a config map.
This is useful to share the settings between OpenShift and Docker (for local development).
```bash
oc create configmap nginx-templates-config --from-file=deployment/conf/nginx/templates --dry-run -o yaml | oc apply -f -
```

```bash
oc process -p NAMESPACE=microsquad -f deployment/service.yml --local=true | oc apply -f -
```

