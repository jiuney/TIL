# Git 기초

> Git은 분산형 버전관리 시스템 (DVCS, Distributed Version Control Systems) 이다.
>
> 소스코드의 이력이 기록된다.



# 기본 명령어

1. git 저장소(`repository`) 초기화

   ```bash
   $ git init
   Initialized empty Git repository in C:/Users/user/Desktop/TIL/.git/
   user@DESKTOP-MN0561E MINGW64 ~/Desktop/TIL (master)
   $
   ```

   * 원하는 폴더를 저장소로 만들게 되면, `git bash`에서는 `(master)`라고 표기된다.
   * 그리고 숨김 폴더로 `.git/`이 생성된다.

2. 커밋할 목록에 담기 (Staging Area)

   ```bash
   $ git add .
   ```

   * 현재 작업 공간 (Working Directory/Tree)의 변경사항을 커밋할 목록에 추가한다. (`add`)
   * `.`는 리눅스에서 현재 디렉토리(폴더)를 표기하는 방법으로, 지금 내 폴더에 있는 파일의 변경사항을 전부 추가한다는 뜻이다.
   * 만일 git.md 파일만을 추가하려면, `git add git.md` 로 추가할 수 있다.
   * 만일 myfolder 폴더를 추가하려면, `git add myfolder/`로 폴더 내의 모든 파일을 추가할 수 있다.

3. 커밋하기

   ```bash
   $ git commit -m '________'
   ```

   * 커밋을 할 떄에는 해당하는 버전의 이력을 의미하는 메시지를 반드시 적어준다.
   * 메시지는 지금 버전을 쉽게 이해할 수 있도록 작성한다.
   * 커밋은 현재 코드의 상태를 스냅샷 찍는 것이다.

4. 로그 확인하기

   ```bash
   $ git log
   commit bbf222f683e88eef239b4d4153773c9def89d144 (HEAD -> master)
   Author: jiuney <jiuney@hotmail.com>
   Date:   Tue May 21 17:13:41 2019 +0900
   
       190521 | 마크다운 연습
   
   ```

   * 현재까지 커밋된 이력을 모두 확인할 수 있다.

5. **git 상태 확인하기**

   ```bash
   $ git status
   ```

   * CLI(Command Line Interface)에서는 현재 상태를 알기 위해 반드시 명령어를 통해 확인해야 한다.
   * 커밋할 목록에 담겨 있는지, untracked인지, commit할 내역이 없는지 등등 다양한 정보를 알려준다.