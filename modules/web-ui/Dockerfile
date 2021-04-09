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

FROM sebp/lighttpd:latest

RUN apk update

COPY --from=builder /home/node/app/dist /var/www/localhost/htdocs

# Copy entrypoint 
COPY ./entrypoint.sh /
RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh","/entrypoint.sh"]

CMD ["start.sh"]