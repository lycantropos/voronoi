ARG IMAGE_NAME
ARG IMAGE_VERSION

FROM ${IMAGE_NAME}:${IMAGE_VERSION}

RUN pip install --upgrade pip setuptools

WORKDIR /opt/voronoi

COPY requirements-setup.txt .
COPY requirements-tests.txt .
RUN pip install --force-reinstall -r requirements-tests.txt
COPY requirements.txt .

COPY include/ include/
COPY src/ src/
COPY tests/ tests/
COPY voronoi voronoi/
COPY README.md .
COPY pytest.ini .
COPY setup.py .

RUN python setup.py develop
