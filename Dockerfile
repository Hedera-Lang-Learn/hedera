FROM circleci/python:3.7-node
USER root
RUN mkdir -p /srv/code
WORKDIR /srv/code
#Copy code from current directory to /srv/code/ in image
ADD . .
# Install Python dependencies
RUN pipenv install --system
#Install static dependencies
RUN npm i

EXPOSE 80 8080

RUN npm rebuild node-sass
RUN npm run build