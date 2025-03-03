FROM alpine:latest
# COPY ./connectors /app
WORKDIR /app
RUN apk add --no-cache curl
CMD ["sh", "/app/publish-connector.sh"]
