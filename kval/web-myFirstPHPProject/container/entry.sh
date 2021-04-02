#!/bin/sh

cron -f &
apache2-foreground
