FROM node:23-alpine3.20 AS frontend

WORKDIR /usr/src/app

COPY ./frontend/package*.json ./frontend/package-lock.json ./

RUN npm install

COPY ./frontend/ ./

RUN npm run build
FROM nginx:stable-alpine AS nginx

COPY --from=frontend /usr/src/app/dist /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
