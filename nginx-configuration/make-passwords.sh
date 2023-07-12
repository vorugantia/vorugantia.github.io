#!/bin/bash
set -eu

FILE=etc/nginx/htpasswd

rm -f "$FILE"
touch "$FILE"

while true; do
  echo "Type a username:"
  read username
  echo "Type a password:"
  read -s password
  echo -n "$password" | htpasswd -i etc/nginx/htpasswd "$username"

  echo "Add more users (y/n):"
  read more
  if [ "$more" != "y" ]; then
    break
  fi
done

chmod 600 etc/nginx/htpasswd
