### 프로젝트 개요

본 프로젝트는 로컬 서버의 외부 IP가 유동 IP일 경우, 외부 IP가 변경되었을 때 및 설정 파일의 TTL 값이 변경되었을 때, AWS Route53 호스팅 영역의 A 레코드 IP와 TTL을 자동으로 갱신해줍니다. 관련 진행 사항은 Discord를 통해 알림을 받을 수 있습니다.

### 주요 기능

- **IP 및 TTL 자동 갱신**: 유동 IP 변경 및 TTL 값 수정 시, AWS Route53의 A 레코드를 갱신.
- **알림 기능**: Discord를 통해 진행 상황을 실시간으로 알림.
- **타이머**: cron 대신 systemd timer로 구현되었으나, cron으로도 실행 가능.
- **단일 IP 처리**: Route53의 다중값 응답 레코드는 지원하지 않으며, 하나의 IP로 overwrite됩니다.
- **Ubuntu 24.04 기준**: Ubuntu 24.04에서 개발 및 테스트됨.

### 설치 및 의존성

#### AWS 요구 사항

- AWS Route53 호스팅 영역 및 A 레코드 필드
- 아래 권한이 포함된 사용자의 퍼블릭키와 시크릿키 필요:
- (참조: https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/specifying-rrset-conditions.html)

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

#### 로컬 요구 사항

- 80, 443 포트가 열려 있어야 함
- Python 3.9 이상 및 `boto3` 필요:

```bash
foo@bar:~$ apt-get install python3
foo@bar:~$ pip install boto3
```

### 마이그레이션

#### Discord Webhook

- 비활성화: `config.py`에서 `USE_DISCORD`를 `False`로 설정.
- 활성화: Discord Webhook URL을 발급받고 `USE_DISCORD`를 `True`로 설정.
  - 참조: [Discord Webhook 가이드](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

#### 파일 마이그레이션

1. **경로 마이그레이션**:

   - `route53_ddns.service`의 <CUSTOM_PATH>를 수정(절대경로).

2. **config.py 마이그레이션**

   - 추가 예정

### 사용법

1. 프로젝트 클론 및 의존성 설치

   ```bash
   git clone <repository_url>
   cd <project_directory>
   pip install -r requirements.txt
   ```

2. `config.py` 설정

   - AWS 자격 증명, Discord Webhook URL 설정, DDNS를 적용할 hosted zone, A record 지정.

3. Systemd 서비스 및 타이머 설치

   ```bash
   sudo cp route53_ddns.service /etc/systemd/system/
   sudo cp route53_ddns.timer /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable route53_ddns.timer
   sudo systemctl start route53_ddns.timer
   ```

### 주의 사항

- Route53의 다중값 응답 레코드는 지원되지 않으며, 단일 IP로 overwrite됩니다.
- 이 프로젝트는 Ubuntu 24.04 기준으로 개발되었습니다. 다른 환경에서는 테스트되지 않았습니다.

### 문의

문제가 발생하거나 도움이 필요하면 다음의 연락처로 문의해 주세요:

- Email: j93es.jung@gmail.com
