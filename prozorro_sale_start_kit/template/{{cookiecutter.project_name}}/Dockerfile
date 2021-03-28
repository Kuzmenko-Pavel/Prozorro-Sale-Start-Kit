FROM python:3-slim as prod_base
WORKDIR /billing-service
ENV PYTHONUNBUFFERED True
COPY requirements/requirements.txt .
COPY config /config
COPY billing-config-for-platforms.yml /billing-config-for-platforms.yml
RUN pip install --no-cache-dir -r requirements.txt

FROM prod_base as prod
COPY src/ .
ARG version=unknown
RUN echo $version && sed -i "s/##VERSION##/$version/g" prozorro_sale/__init__.py

FROM prod as test
COPY requirements/test.txt .
COPY fixtures ./fixtures
COPY test ./test
RUN pip install --no-cache-dir -r test.txt

FROM prod as local
COPY requirements/development.txt .
COPY .flake8 /.flake8
COPY .mypy.ini /.mypy.ini
RUN pip install --no-cache-dir -r development.txt

FROM prod
