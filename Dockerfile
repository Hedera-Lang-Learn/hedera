FROM python:3.7
USER root
RUN mkdir -p /srv/code
WORKDIR /srv/code
#Copy code from current directory to /srv/code/ in image
ADD . .

RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -

# Install Python dependencies
RUN apt-get update && apt-get install -y netcat git nodejs && \
    pip install pipenv && \
    pipenv install --system --deploy

RUN npm i

EXPOSE 8000 8080

RUN npm rebuild node-sass && \
    npm run build