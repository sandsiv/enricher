FROM python:3.12.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget curl vim.tiny \
    && update-alternatives --set editor /usr/bin/vim.tiny \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN adduser --disabled-password enricher

WORKDIR /app

COPY *.py .
RUN chown -R enricher:enricher /app
USER enricher

ENTRYPOINT ["python", "csv_enrichment_main.py"]
CMD ["default/path/to/file.csv", "default/path/to/config.ini"]
