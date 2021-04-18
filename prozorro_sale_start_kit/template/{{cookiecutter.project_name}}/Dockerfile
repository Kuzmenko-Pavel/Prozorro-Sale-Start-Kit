FROM python:3-slim as prod_base
WORKDIR /{{cookiecutter.project_name}}
ENV PYTHONUNBUFFERED True
COPY requirements/requirements.txt .
COPY config /config
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev binutils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc python3-dev binutils

FROM prod_base as prod
COPY src/ .
ARG version=unknown
RUN echo $version && sed -i "s/##VERSION##/$version/g" prozorro_sale/__init__.py

FROM prod as test
COPY ["requirements/test.txt", "test", "./"]
RUN pip install --no-cache-dir -r test.txt

FROM prod as local
COPY ["requirements/development.txt", "requirements/test.txt", "requirements/documentation.txt", "./"]
COPY [".flake8", ".mypy.ini", "/"]
RUN pip install --no-cache-dir -r development.txt

FROM prod
