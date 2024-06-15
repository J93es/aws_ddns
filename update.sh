#!/bin/bash

BACKUP_DIR="$(pwd)/aws_ddns_bak.d/"
BACKUP_NAME="aws_ddns_$(date +%Y%m%d%H%M%S).bak/"
AWS_DDNS_GIT_URL="https://github.com/J93es/aws_ddns.git"
TMP_DIR="__tmp_aws_ddns/"

sudo mkdir -p           ${BACKUP_DIR}/${BACKUP_NAME} &&
sudo mv -r src          ${BACKUP_DIR}/${BACKUP_NAME} &&
sudo cp -p config.json  ${BACKUP_DIR}/${BACKUP_NAME} &&
sudo cp -p start.sh     ${BACKUP_DIR}/${BACKUP_NAME} &&

sudo rm -r                          ${TMP_DIR} &&
sudo git clone ${AWS_DDNS_GIT_URL}  ${TMP_DIR} &&
sudo mv -r                          ${TMP_DIR}/src . &&
sudo rm -r                          ${TMP_DIR} &&

sudo systemctl daemon-reload &&
sudo systemctl restart aws_ddns.service &&
sudo systemctl restart aws_ddns.timer