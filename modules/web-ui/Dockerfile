FROM node:14-alpine3.13 as builder

RUN apk add --update nodejs npm

RUN mkdir /home/node/app && chown -R node:node /home/node/app

WORKDIR /home/node/app

# Cache node modules first
COPY --chown=node:node package*.json ./

USER node

RUN npm install --only=prod

COPY --chown=node:node . .

# Set production environment vars
RUN mv .env.prod .env

RUN npm run build

# Fix asset loading
RUN  mv ./public/assets ./dist/

# IMPORTANT : The upstream image defines /etc/lighttpd as a volume.
#             This prevents any modifications to be brought to the image's files
#             under /etc/lighttpd.
FROM sebp/lighttpd:latest

RUN apk update

COPY --from=builder /home/node/app/dist /var/www/localhost/htdocs

# Copy entrypoint 
COPY ./entrypoint.sh /
RUN chmod +x entrypoint.sh


ENTRYPOINT ["sh","/entrypoint.sh"]

USER 1000

CMD ["start.sh"]