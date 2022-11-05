# Using slim-buster here for demonstrative purposes
# Depending on the security requirements, the image can be alpine to minimize
# the amount of installed applications or a custom image maintained by the development team
FROM python:3.10-slim-buster

ARG APP_NAME=videoshare
ARG APP_VERSION="development"
ARG BUILD_REQUIREMENTS="gcc"
ARG APP_REQUIREMENTS=requirements.txt
ARG CODE=.

ENV PIP_NO_CACHE_DIR=on PIP_DISABLE_PIP_VERSION_CHECK=on

# Copy application files
COPY ${CODE} /data/app/${APP_NAME}

# Set working directory
WORKDIR /data/app/${APP_NAME}

# Set version to version file
RUN echo ${APP_VERSION} > VERSION

# Install system and app requirements and remove build requirements
RUN apt-get update && \
    apt-get install -y ${BUILD_REQUIREMENTS} ${SYS_REQUIREMENTS} && \
    pip install --no-cache-dir -r ${APP_REQUIREMENTS} && \
    apt-get remove -y ${BUILD_REQUIREMENTS} && apt-get autoremove -y && apt-get clean -y

# Set entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]
