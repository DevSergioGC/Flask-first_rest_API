#!/bin/sh

flask db upgrade

exec gunicor --bind 0.0.0.0:80 "app:create_app()"