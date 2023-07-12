#!/bin/sh

set -eu

rsync -av --progress -e "ssh -p 50247" index.html daniels@bore.pub:/var/www/daily-performance-report/
rsync -av --progress -e "ssh -p 50247" js/ daniels@bore.pub:/var/www/daily-performance-report/
