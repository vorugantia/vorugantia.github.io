#!/bin/sh
set -eu

mkdir -p etc/ssl/private/

openssl req \
  -new \
  -newkey rsa:4096 \
  -x509 \
  -sha256 \
  -days 1000 \
  -nodes \
  -out etc/ssl/private/daily-performance-report.crt \
  -keyout etc/ssl/private/daily-performance-report.key \
  -subj "/C=UK/ST=London/L=London/O=SW7/OU=IT/CN=daily-performance-report.sw7group.com"
