FROM node:23-alpine3.20

WORKDIR /opt/project

COPY package*.json package-lock.json ./

RUN npm install

COPY ./ ./

RUN npm run build
