[PREVIEW]

1. 본 프로젝트는 로컬 서버의 외부 ip가 유동 ip일 경우, 외부 ip가 변경되었을 때, config의 TTL 값이 변경되었을 경우 작동합니다.
   작동 시, AWS 호스팅 영역 A레코드의 ip와 TTL을 갱신합니다.
2. 관련 진행 정보를 discord를 통하여 알 수 있도록 구성하였습니다.
3. cron이 아닌 systemd timer로 구현하였으나, cron으로도 실행 가능합니다.
   (단, crontab -e 로 편집하는 것이 아닌 vim /etc/crontab에서 편집하며 root권한이 필요합니다.)
4. royte53의 다중값 응답 레코드를 지원하지 않습니다. 만약 다중 응답 레코드 환경에서 본 서비스를 실행한다면 하나의 ip로 overwrite됩니다.
5. ubuntu24.04 기준으로 개발되었습니다.

[DEPENDENCY]

1. AWS

- 적어도 하나의 AWS Route53 호스팅 영역과 호스팅 영역의 A레코드 필드가 필요합니다.
- 아래의 권한을 가지고 있는 사용자의 퍼블릭키, 시크릿키가 필요합니다.
  (참조: https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/specifying-rrset-conditions.html)

  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "route53:ChangeResourceRecordSets",
          "route53:ListResourceRecordSets"
        ],
        "Resource": "arn:aws:route53:::hostedzone/*",
        "Condition": {
          "ForAllValues:StringEquals": {
            "route53:ChangeResourceRecordSetsRecordTypes": ["A"],
            "route53:ChangeResourceRecordSetsActions": ["UPSERT"]
          }
        }
      },
      {
        "Effect": "Allow",
        "Action": "route53:ListHostedZones",
        "Resource": "*"
      }
    ]
  }
  ```

2. local

- 80, 443 포트가 열려있어야 합니다.
- python3.9 이상과 boto3가 필요합니다.
  ```bash
  foo@bar:~$ pip install {name}
  foo@bar:~$ apt-get python3-{name}
  ```

[Migration]

1. discord webhook

- 만약 비활성화를 원한다면 config.py의 USE_DISCORD를 False로 변경하세요
- discord 알람을 활성화하려면 discord webhook url을 발급하고 USE_DISCORD를 TRUE로 변경하세요.
  (참조: https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

2. file migration

1) PATH migration

- PATH 수정을 필요로하는 타겟은 aws_ddns.service, start.sh, MY_PATH(디렉토리 명)이 존재합니다.
- aws_ddns.service, start.sh, MY_PATH(디렉토리 명)의 MY_PATH를 적절히 migration하세요.
- MY_PATH 디렉토리는 /etc/ 디렉토리에 위치할 필요는 없습니다. 적절한 위치를 선정하세요.
- aws_ddns.service, aws_ddns.timer는 /etc/systemd/system 디렉토리에 위치시키는 것을 권장합니다.
