FROM docker.io/library/node:20.10.0

LABEL description="Clinic Frontend image"

# created env variables with default values (can be overridden from podman run)

ENV FRONTEND_SERVER_PORT=4200
ENV FRONTEND_URL=0.0.0.0

EXPOSE $FRONTEND_SERVER_PORT

COPY Pipelines/Frontend/frontend/ /opt/source-code

WORKDIR /opt/source-code

RUN npm install  

# RUN npm cache clean --force


# RUN mkdir /.npm && chown -R 1009860000:0 ~/.npm && chown -R 1009860000:0 /.npm

# RUN mkdir /.npm && chown -R $USER:$GROUP ~/.npm && chown -R $USER:$GROUP /.npm

# CMD npm start --host=0.0.0.0 --port=4200

# invoke a shell to expand the ENV before running the frontend

CMD sh -c 'npm start --host=$FRONTEND_URL --port=$FRONTEND_SERVER_PORT'
