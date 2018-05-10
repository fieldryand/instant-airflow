Instant Airflow
===============

Dockerized Airflow based on https://github.com/puckel/docker-airflow, with extra configuration.

A cron job can be useful to remove logs that fill up disk space:
```
0 12 * * * sudo find /var/lib/docker/overlay2 -type f | grep airflow | grep logs | sudo xargs rm 2>&1 | /usr/bin/logger -t remove_airflow_logs
```
