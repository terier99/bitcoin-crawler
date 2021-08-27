# bitcoin-crawler
https://datastudio.google.com/u/0/reporting/b8d9c674-474e-4caf-a56f-3813d067ffff/page/WbRXC

데이터 대시 보드 생성

## 데이터 소스
- 암호 화폐 시세 : 업비트 api
- 네이버 뉴스 개수 : 네이버 뉴스 페이지 크롤링
- 구글 트렌드 : pytrends 모듈 (1~ 2일 딜레이)

- 크롤링 코드 Google Cloud Function에 저장 
- Google Scheduler를 이용해 일정 주기 크론잡으로 실행
- 데이터 Google Spread Sheet에 적재
- Data Studio를 해 대시보드 생성 (대시보드 업데이트 주기 15분)
