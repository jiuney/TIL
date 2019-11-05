# SQL과 django ORM

## 기본 준비 사항

* https://bit.do/djangoorm에서 csv 파일 다운로드

* django app

  * `django_extensions` 설치

  * `users` app 생성

  * csv 파일에 맞춰 `models.py` 작성 및 migrate

    아래의 명령어를 통해서 실제 쿼리문 확인

    ```bash
    $ python manage.py sqlmigrate users 0001
    ```

* `db.sqlite3` 활용

  * `sqlite3`  실행

    ```bash
    $ ls
    db.sqlite3 manage.py ...
    $ sqlite3 db.sqlite3
    ```

  * csv 파일 data 로드

    ```sqlite
    sqlite > .tables
    auth_group                  django_admin_log
    auth_group_permissions      django_content_type
    auth_permission             django_migrations
    auth_user                   django_session
    auth_user_groups            auth_user_user_permissions  
    users_user
    sqlite > .mode csv
    sqlite > .import users.csv users_user
    sqlite > SELECT COUNT(*) FROM users_user;
    100
    ```
    
    * select count 해서 100이 나오면 제대로 들어간 것. 나는 import 했을 때 `users.csv:1: INSERT failed: datatype mismatch` 라는 에러가 나왔는데도 막상 select 해보니 입력된걸로 나옴;;

* 확인

  * sqlite3에서 스키마 확인

    ```sqlite
    sqlite > .schema users_user
    CREATE TABLE IF NOT EXISTS "users_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(10) NOT NULL, "last_name" varchar(10) NOT NULL, "age" integer NOT NULL, "country" varchar(10) NOT NULL, "phone" varchar(15) NOT NULL, "balance" integer NOT NULL);
    ```

    

## 문제

> 아래의 문제들을 sql문과 대응되는 orm을 작성 하세요.

### 기본 CRUD 로직

1. 모든 user 레코드 조회

   ```python
   # orm
   User.objects.all()
   ```

   * sql문으로 어떻게 쓰는지 모를 때 다음과 같이 하면 된다

     ```python
     >>> print(User.objects.all().query)
     SELECT "users_user"."id", "users_user"."first_name", "users_user"."last_name", "users_user"."age", "users_user"."country", "users_user"."phone", "users_user"."balance" FROM "users_user"
     ```

   ```sql
   -- sql
   SELECT * FROM users_user;
   ```

2. user 레코드 생성

   ```python
   # orm
   User.objects.create(
       first_name = "Jiun",
       last_name = "Hwang",
       age = 29,
       country = "South Korea",
       phone = "010-4800-2154",
       balance = 10000000000000
   )
   ```

   ```sql
   -- sql
   INSERT INTO users_user (first_name, last_name, age, country, phone, balance) VALUES ("Jiun", "Hwang", 29, "South Korea", "010-4800-2154", 10000000000000);
   ```

   * column명을 안써주면 id가 자동생성이 안되고 에러가 나서 생성이 안된다.

   * 하나의 레코드를 빼고 작성 후 `NOT NULL` constraint 오류를 orm과 sql에서 모두 확인 해보세요.

     ```python
     sqlite3.IntegrityError: NOT NULL constraint failed: users_user.balance
     Error: NOT NULL constraint failed: users_user.first_name
     ```

3. 해당 user 레코드 조회

   ```python
   # orm
   user = User.objects.get(pk=101)
   user.first_name
   user.last_name
   user.age
   user.country
   user.phone
   user.balance
   ```

      ```sql
   -- sql
   SELECT * FROM users_user WHERE id=101;
      ```

4. 해당 user 레코드 수정

   ```python
   # orm
   user = User.objects.get(pk=101)
   user.first_name = "지운"
   user.last_name = "황"
   user.country = "서울특별시"
   user.balance = 77777777777777
   user.save()
   ```

      ```sql
   -- sql
   UPDATE users_user SET first_name="지운", last_name="황", country="서울특별시", balance=77777777777777 WHERE id=101;
      ```

5. 해당 user 레코드 삭제

   ```python
   # orm
   user = User.objects.get(pk=101)
user.delete()
   ```
   
      ```sql
   -- sql
   DELETE FROM users_user WHERE id=101;
      ```

### 조건에 따른 쿼리문

1. 전체 인원 수 

   ```python
   # orm
   User.objects.all().count*()
   ```

      ```sql
   -- sql
   SELECT COUNT(*) FROM users_user;
      ```

2. 나이가 30인 사람의 이름

   ```python
   # orm
   User.objects.filter(age=30).values('first_name')
   ```

      ```sql
   -- sql
   SELECT first_name FROM users_user WHERE age=30;
      ```

3. 나이가 30살 이상인 사람의 인원 수

   ```python
   # orm
   User.objects.filter(age__gte=30).count()
   ```

   * gte = greater than or equal

      ```sql
   -- sql
   SELECT COUNT(*) FROM users_user WHERE age >= 30;
      ```

4. 나이가 30이면서 성이 김씨인 사람의 인원 수

   ```python
   # orm
   User.objects.filter(age=30, last_name="김").count()
   User.objects.filter(age=30).filter(last_name="김").count()
   
   from django.db.models import Q
   User.objects.filter(
       Q(age=30) | Q(last_name="김")    # or 사용하고 싶을 때
   )
   ```

      ```sql
   -- sql
   SELECT COUNT(*) FROM users_user WHERE age=30 and last_name="김";
      ```

5. 지역번호가 02인 사람의 인원 수

   ```python
   # orm
   User.objects.filter(phone__startswith="02-").count()
   ```

      ```sql
   -- sql
   SELECT COUNT(*) FROM users_user WHERE phone LIKE '02-%'
      ```

6. 거주 지역이 강원도이면서 성이 황씨인 사람의 이름

   ```python
   # orm
   User.objects.filter(country="강원도", last_name="황").values("first_name")
   ```
   
   ```sql
   -- sql
   SELECT first_name FROM users_user WHERE country="강원도" and last_name="황";
   ```



### 정렬 및 LIMIT, OFFSET

1. 나이가 많은 사람 10명

   ```python
   # orm
   User.objects.order_by('-age')[:10]
   ```

      ```sql
   -- sql
   SELECT * FROM users_user ORDER BY age DESC LIMIT 10;
      ```

2. 잔액이 적은 사람 10명

   ```python
   # orm
   User.objects.order_by('balance')[:10]
   ```

      ```sql
   -- sql
   SELECT * FROM users_user ORDER BY balance ASC LIMIT 10;
      ```

3. 성, 이름 내림차순 순으로 5번째 있는 사람

      ```python
   # orm
   User.objects.order_by('-last_name', '-first_name')[4]
   ```
   
      ```sql
   -- sql
   SELECT * FROM users_user ORDER BY last_name DESC, first_name DESC LIMIT 1 OFFSET 4;
      ```




### 표현식 (aggregate, annotate)

1. 전체 평균 나이

   ```python
   # orm
   from django.db.models import Avg
   User.objects.aggregate(Ave('age'))
   ```

   * aggregate는 전체 query set에 대한 계산 결과 값.
   * annotate는 query set에 담긴 애들 하나하나에다가 field를 추가해주는 것.

   ```sql
   -- sql
   SELECT AVG(age) FROM users_user;
   ```

2. 김씨의 평균 나이

   ```python
   # orm
   User.objects.filter(last_name="김").aggregate(Avg('age'))
   ```

      ```sql
   -- sql
   SELECT AVG(age) FROM users_user WHERE last_name="김";
      ```

3. 계좌 잔액 중 가장 높은 값

   ```python
   # orm
   from django.db.models import Max
   User.objects.aggregate(Max('balance'))
   ```

      ```sql
   -- sql
   SELECT MAX(balance) FROM users_user;
      ```

4. 계좌 잔액 총액

      ```python
   # orm
   from django.db.models import SUM
User.objects.aggregate(Sum('balance'))
   ```
   
      ```sql
   -- sql
   SELECT SUM(balance) FROM users_user;
      ```