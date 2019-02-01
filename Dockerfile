FROM circleci/python:3.7-rc-node
USER root
RUN mkdir -p /srv/code
WORKDIR /srv/code
#Copy code from current directory to /srv/code/ in image
ADD . .
RUN apt-get install nginx
# Install Python dependencies
RUN pipenv install --system --deploy
#Install static dependencies
RUN npm i
EXPOSE 8001 80
COPY ./docker-entrypoint.sh /
COPY ./hedera_nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/hedera_nginx.conf /etc/nginx/sites-enabled
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN npm rebuild node-sass
RUN npm run build

RUN python manage.py migrate
RUN python manage.py loaddata sites
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]