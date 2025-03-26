FROM python:3.7-slim AS builder
ADD . /app
RUN pip install --target=/app --no-cache-dir requests


FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/defectdojo.py"]