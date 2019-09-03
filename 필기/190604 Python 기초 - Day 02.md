# 1일차 리뷰

* 컴퓨터 = H/W + S/W
  * H/W = CPU + RAM + Disk(HDD,SSD)
    * HDD의 속도 = RPM (10000, 7200, 4xxx)
    * SSD: M.2, 256GB
  * S/W = OS (Unix, Linux, Windows)
    * Windows
      * 32bit: x86, i386, i586, x32
      * 64bit: x64, x86_64, AMD64
* 가상머신
  * Virtual Box →
    * Fedora 22 (MySQL 5.7)
    * Window Server 2016 (MariaDB 10.4RC, SQL Server 2019 CTP)



# (중요) 외부에서 DB서버에 접속하기

1. MariaDB → root가 외부에서 접속? 방화벽 등록?
2. SQL Server
   * port 허용 (1433)
   * 인증 모드 변경 (Windows 인증 → SQL 인증)
   * sa 사용자 허용
   * TCP(인터넷)를 통한 접속 허용 (= ip주소로 접속 허용)



# Program과 Process

* Program
  * 하드에 저장되어 있음
  * 비활성화 상태
* Process
  * 하드에 저장된 프로그램을 활성화시켜 메모리로 옮겨놓은 상태
  * Foreground process vs. Background process
    * Foreground process: 눈에 보이는 프로세스
    * Background process: 실행되고 있지만 눈에 보이지 않는 프로세스
      * "서비스"는 대부분이 background process



# 미션 - 2일차

0. Windows Server 2019 ISO 파일 다운로드

0. SQL Server 2017 Express 다운로드

0. MySQL 8.0.x 다운로드

--- 자신이 정리한 내용을 확인하면서 진행 ---

1. Virtual Box에 Win2019 설치하고 설정 → 스냅샷
2. Win2019에 SQL 2017과 MySQL 8.0을 설치하고 설정 → 스냅샷
3. Win2019에 Python      3.6과 PyCharm 설치 후 Hello World 작성 → 스냅샷
4. PC의 HeidiSQL에서 SQL 2017과 MySQL 8.0에 접속

- 캡쳐: PyCharm에서 Hello      World 출력한거랑 HeidiSQL에서 접속된 화면



# 2일차 미션 풀이

1. Virtual Box에 Win2019 설치하고 설정

   ![c01](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c01.PNG)

   ![c02](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c02.PNG)

   ![c03](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c03.PNG)

   ![c04](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c04.PNG)

2. Win2019에 SQL 2017과 MySQL 8.0을 설치하고 설정

   ![c05](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c05.PNG)

   ![c06](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c06.PNG)

   ![c07](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c07.PNG)

   ![c08](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c08.PNG)

   ![c09](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c09.PNG)

3. Win2019에 Python 3.6과 PyCharm 설치 후 Hello World 작성

   ![c10](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c10.PNG)

   ![c11](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c11.PNG)

   ![c12](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c12.PNG)

   ![c13](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c13.PNG)

   ![c14](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c14.PNG)

   ![c15](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c15.PNG)

   ![c16](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c16.PNG)

   ![c17](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c17.PNG)

   ![c18 - hello world](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c18%20-%20hello%20world.PNG)

4. PC의 HeidiSQL에서 SQL 2017과 MySQL 8.0에 접속

   ![c19](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c19.PNG)

   ![c20](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c20.PNG)

   ![c21](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c21.PNG)

   ![c22](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c22.PNG)

   ![c23](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c23.PNG)

   ![c24](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c24.PNG)

   ![c25](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c25.PNG)

   ![c26](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c26.PNG)

   ![c27](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c27.PNG)

   ![c28](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c28.PNG)

   ![c29](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c29.PNG)

   ![c30](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c30.PNG)

   ![c31](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c31.PNG)

   ![c32](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c32.PNG)

   ![c33](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c33.PNG)

   ![c34](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c34.PNG)

   ![c35](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c35.PNG)

   ![c36](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c36.PNG)

   ![c37](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c37.PNG)

   ![c38](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c38.PNG)

   * 중요!  여기서 설정 다 끝낸 후에 서버 오른쪽 클릭해서 Restart를 눌러야 설정이 완료된다.

   ![c39](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c39.PNG)

   ![c40](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c40.PNG)

   ![c41](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c41.PNG)

   ![c42 - SQL Server](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c42%20-%20SQL%20Server.PNG)

   ![c43](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c43.PNG)

   ![c44](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c44.PNG)

   ![c45 - MySQL](https://github.com/jiuney/TIL/blob/master/img/190604%20capture/c45%20-%20MySQL.PNG)
