FROM node:14-alpine3.13 as builder

RUN apk add --update nodejs npm

RUN mkdir /home/node/app && chown -R node:node /home/node/app

WORKDIR /home/node/app

# Cache node modules first
COPY --chown=node:node package*.json ./

USER node

RUN npm install --only=prod

COPY --chown=node:node . .

RUN npm run build

# Fix asset loading
RUN  mv ./public/assets ./dist/
RUN  mv ./public/conf ./dist/

FROM nginx:stable-alpine

RUN apk update

######################
# Make the image Openshift-friendly
RUN chmod g+rwxt /var/cache/nginx /var/run /var/log/nginx /etc/nginx/conf.d || true
# Remove the upstream default configuration
RUN rm  /etc/nginx/conf.d/default.conf
# Remove the upstream IPv6 configuration entrypoint - only useful if we kept the default configuration
RUN rm /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
RUN chgrp -R root /var/cache/nginx

# comment user directive as master process is run as user in OpenShift anyhow
RUN sed -i.bak 's/^user/#user/' /etc/nginx/nginx.conf

RUN addgroup nginx root

COPY --from=builder /home/node/app/dist /usr/share/nginx/html

ENV NGINX_PORT=8080
ENV NGINX_HOSTNAME=localhost
# You can override with your context path, without leading and trailing slashes
#   e.g. /web-ui 
ENV NGINX_CONTEXT_PATH=/web-ui

COPY deployment/docker/etc/nginx /etc/nginx

# # You can inject the JSON configuration file as config.json in this location
VOLUME /usr/share/nginx/html/conf/

# nginx default.conf.template
VOLUME "/etc/nginx/templates"
USER nginx
