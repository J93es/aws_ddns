#!/bin/bash

BACKUP_DIR="$(pwd)/route53_ddns_bak.d/"
BACKUP_NAME="route53_ddns_$(date +%Y%m%d%H%M%S).bak/"
ROUTE53_DDNS_GIT_URL="https://github.com/J93es/route53-ddns.git"
TMP_DIR="__tmp_route53_ddns/"

sudo mkdir -p                                   ${BACKUP_DIR}/${BACKUP_NAME}                &&
sudo mv src                                     ${BACKUP_DIR}/${BACKUP_NAME}    || true     &&
sudo cp -p          config.json                 ${BACKUP_DIR}/${BACKUP_NAME}    || true     &&
sudo cp -p          start.sh                    ${BACKUP_DIR}/${BACKUP_NAME}    || true     &&

sudo rm -rf         ${TMP_DIR} &&
sudo git clone      ${ROUTE53_DDNS_GIT_URL}     ${TMP_DIR}                                  &&
sudo mv             ${TMP_DIR}/src              ./src                                       &&
sudo rm -rf         ${TMP_DIR}                                                              &&

sudo systemctl      daemon-reload                                                           &&
sudo systemctl      restart                     route53_ddns.service                        &&
sudo systemctl      restart                     route53_ddns.timer
