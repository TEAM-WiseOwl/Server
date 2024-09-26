## 초기 세팅

#### 1. git clone or git pull

#### 2. 가상환경 생성하기

#### 3. local_settings.py 집어넣기 (manage.py와 같은 계층)

#### 4. pip install -r requirements.txt

## git flow

#### main

-   실제 운영에 반영되는 브랜치

#### dev

-   실제 배포에 적용되기 전 코드들을 테스트해보는 브랜치

#### feat

-   특정 기능을 개발하는 브랜치

## 작업 방식

#### 0. merge한 사람이 merge 했다고 하면 dev에서 pull 받아서 최신화 하기

#### 1. 한 기능에 대해 이슈 생성

#### 2. dev브랜치에서 feat/이슈번호 브랜치 생성 (git switch dev -> git switch -c feat/이슈번호)

#### 3. 기능 개발 완료 후 `[#이슈번호] 커밋 메시지 내용` 형식으로 commit 및 push (git commit -m "[#이슈번호] 커밋 내용" -> git push origin feat/이슈번호)

#### 4. github 사이트 와서 pull & request 생성하기 (dev <- feat/이슈번호)

#### 5. 팀장 코드 피드백 완료 후 본인이 merge 하기

#### 6. merge 후 본인 로컬 dev 브랜치에 git pull origin dev로 최신화 하기

#### 7. 완료된 이슈 브랜치 삭제하기 (git branch -d feat/이슈번호 -> git push origin --delete feat/이슈번호)

#### 8. 화이팅~!
