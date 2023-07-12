#!/bin/sh
set -eu

if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as the root user!"
  exit
fi

if [ ! -f etc/ssl/private/daily-performance-report.crt ]; then
  echo 'Please first generate a TLS certificate and key via "./make-selfsigned-cert.sh"'
  exit 1
fi

if [ ! -f etc/nginx/htpasswd ]; then
  echo 'Please first generate a password file via "./make-passwords.sh"'
  exit 1
fi

systemctl stop nginx

rsync -va --chown "root:root" --progress etc/ /etc

chown "daniels:daniels" /etc/nginx/htpasswd
mkdir -p /var/www/daily-performance-report/
chown -R "daniels:daniels" "/var/www/daily-performance-report/"

systemctl start nginx
