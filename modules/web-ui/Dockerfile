FROM node:14-alpine3.13

RUN apk add --update nodejs npm

RUN mkdir /home/node/app && chown -R node:node /home/node/app

WORKDIR /home/node/app

# Cache node modules first
COPY --chown=node:node package*.json ./

USER node

RUN npm install --only=prod

ENV NODE_ENV=production
ENV PORT=8080

COPY --chown=node:node . .

RUN npm run build

# Fix asset loading
RUN  mv ./public/assets ./dist/

FROM sebp/lighttpd:latest

RUN apk update

COPY --from=0 /home/node/app/dist /var/www/localhost/htdocs