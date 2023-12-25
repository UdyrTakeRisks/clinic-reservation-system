FROM node:16.14
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install

RUN if [ ! -d "/.npm" ]; then mkdir /.npm; fi
RUN if [ ! -d "/app/.angular" ]; then mkdir /app/.angular; fi

RUN chown -R 1009860000:0 /.npm
RUN chown -R 1009860000:0 /app/.angular
USER 1009860000
COPY ./frontend/. .

CMD ["npm", "start"]
