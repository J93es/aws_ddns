#!/bin/bash

mkdir aws_ddns_$(date +%Y%m%d%H%M%S).bak || true &&
mv aws_ddns_main.py src aws_ddns_$(date +%Y%m%d%H%M%S).bak || true &&
git clone https://github.com/J93es/aws_ddns.git tmp_aws_ddns &&
mv tmp_aws_ddns/MY_PATH/aws_ddns_main.py tmp_aws_ddns/MY_PATH/src . &&
chmod 755 aws_ddns_main.py start.sh &&
rm -rf tmp_aws_ddns &&

systemctl daemon-reload &&
systemctl restart aws_ddns.service &&
systemctl restart aws_ddns.timer