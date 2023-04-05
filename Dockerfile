ARG IMAGE_NAME
ARG IMAGE_VERSION

FROM ${IMAGE_NAME}:${IMAGE_VERSION}

WORKDIR /opt/voronoi

COPY pyproject.toml .
COPY README.md .
COPY setup.py .
COPY voronoi voronoi/
COPY src/ src/
COPY tests/ tests/

RUN pip install -e .[tests]
