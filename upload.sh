#!/bin/sh

set -eu
SSH_PORT=45792

rsync -av --progress -e "ssh -p ${SSH_PORT} -o 'UserKnownHostsFile ./known_hosts'" index.html daniels@bore.pub:/var/www/daily-performance-report/
rsync -av --progress -e "ssh -p ${SSH_PORT} -o 'UserKnownHostsFile ./known_hosts'" js daniels@bore.pub:/var/www/daily-performance-report/
