FROM python:3.7 AS prod

# Upgrade pip
RUN pip install --upgrade pip

# Create app working directory
RUN mkdir -p /app
WORKDIR /app

# Install system dependencies and target node v14
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get update && \
    apt-get install -y netcat git nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY ./hedera/requirements/base.txt /app/
RUN pip install -r base.txt && \
    rm base.txt

# Install node dependencies
COPY ./package-lock.json ./package.json /app/
RUN npm i && \
    npm rebuild node-sass && \
    rm package-lock.json package.json

# Copy app files
COPY . /app

# Build webpack assets
RUN npm run build

# Use port 8000 for django server or 8080 for webpack dev server
EXPOSE 8000 8080

FROM prod AS dev

# Install python dev dependencies
COPY ./hedera/requirements/dev.txt /app/
RUN pip install -r dev.txt && \
    rm dev.txt
