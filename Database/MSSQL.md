# Microsoft SQL Server (MS-SQL)

## 기본 개념

**Microsoft SQL Server**는 Microsoft가 만든 관계형 데이터베이스 관리 시스템(RDBMS)이다.

실무에서는 **MS-SQL**, **MSSQL**, **SQL Server**라고 부른다. 회사의 직원, 거래처, 회계 전표, 예산, 구매 내역, 재고 등 구조화된 데이터를 저장하고 조회·수정·삭제하며, 사용자 권한과 백업을 관리한다.

```text
사용자가 업무 프로그램에서 데이터를 요청
                  ↓
업무 프로그램이 SQL Server에 SQL 전달
                  ↓
SQL Server가 데이터베이스에서 데이터 처리
                  ↓
결과를 업무 프로그램 화면에 표시
```

예를 들어 사용자가 ERP에서 전표를 조회하면, ERP 프로그램은 뒤쪽의 SQL Server에 데이터를 요청하고 그 결과를 화면에 보여줄 수 있다.

## SQL과 SQL Server의 차이

| 구분 | 의미 |
|---|---|
| SQL | 데이터베이스에 명령을 전달하는 언어 |
| SQL Server | SQL을 처리하고 실제 데이터를 저장·관리하는 Microsoft의 프로그램 |

```text
SQL        = 데이터베이스와 대화하는 언어
SQL Server = SQL을 이해하고 데이터를 관리하는 시스템
```

PostgreSQL, MySQL, Oracle도 SQL을 사용하지만 SQL Server와는 서로 다른 DBMS이다. 제품마다 지원 기능과 세부 SQL 문법에는 차이가 있을 수 있다.

## SQL Server의 데이터 구조

```text
SQL Server
└─ Database
   └─ Schema
      ├─ Table
      ├─ View
      ├─ Stored Procedure
      └─ Function
```

- **Server:** 여러 데이터베이스를 실행하고 관리하는 SQL Server 환경
- **Database:** 관련 데이터를 모아 놓은 논리적인 저장공간
- **Schema:** 테이블과 뷰 등의 객체를 분류하는 이름 공간
- **Table:** 데이터를 행과 열로 저장하는 객체
- **View:** 하나 이상의 테이블을 조회한 결과를 가상 테이블처럼 제공하는 객체
- **Stored Procedure:** 자주 사용하는 SQL 작업을 데이터베이스에 저장한 실행 단위
- **Function:** 값을 입력받아 계산 결과를 반환하는 데이터베이스 함수

## 테이블의 구성

직원 정보를 저장하는 테이블은 다음과 같은 형태가 될 수 있다.

| employee_id | name | department | position |
|---:|---|---|---|
| 1001 | 김신입 | 경영기획팀 | 사원 |
| 1002 | 이대리 | 회계팀 | 대리 |

- **Column(열):** 이름, 부서처럼 데이터의 항목
- **Row(행):** 직원 한 명처럼 하나의 데이터 기록
- **Primary Key(기본 키):** 각 행을 중복 없이 구별하는 값

위 예시에서는 직원마다 값이 다른 `employee_id`를 Primary Key로 사용할 수 있다.

## 기본 SQL 명령

### SELECT — 조회

```sql
SELECT *
FROM dbo.Employees;
```

`dbo.Employees` 테이블의 모든 데이터를 조회한다.

### INSERT — 추가

```sql
INSERT INTO dbo.Employees (employee_id, name, department)
VALUES (1003, '박사원', '경영기획팀');
```

새로운 직원 데이터를 추가한다.

### UPDATE — 수정

```sql
UPDATE dbo.Employees
SET department = 'IT기획팀'
WHERE employee_id = 1001;
```

1001번 직원의 부서를 변경한다.

### DELETE — 삭제

```sql
DELETE FROM dbo.Employees
WHERE employee_id = 1003;
```

1003번 직원의 데이터를 삭제한다.

> `UPDATE`와 `DELETE`에서 `WHERE` 조건을 빠뜨리면 테이블의 여러 행이 한꺼번에 변경되거나 삭제될 수 있으므로 특히 주의해야 한다.

## Login, User, Schema, Permission

SQL Server에서는 서버 접속 계정, 데이터베이스 사용자, 데이터 영역과 권한을 구분한다.

```text
Login으로 SQL Server에 접속
              ↓
Database User 자격으로 특정 DB에 접근
              ↓
부여된 Permission으로 작업 수행
              ↓
Schema 안의 Table·View 등에 접근
```

| 개념 | 의미 |
|---|---|
| Login | SQL Server 자체에 접속하기 위한 서버 수준 계정 |
| Database User | 특정 데이터베이스 안에서 사용하는 사용자 계정 |
| Schema | 테이블과 뷰 같은 데이터베이스 객체를 분류하는 이름 공간 |
| Permission | 사용자나 역할이 할 수 있는 작업을 정한 권한 |
| Role | 여러 권한을 묶어 사용자에게 부여하기 위한 역할 그룹 |

자주 보는 권한은 다음과 같다.

| 권한 | 의미 |
|---|---|
| `CONNECT` | 데이터베이스 접속 |
| `SELECT` | 데이터 조회 |
| `INSERT` | 데이터 추가 |
| `UPDATE` | 데이터 수정 |
| `DELETE` | 데이터 삭제 |
| `EXECUTE` | 프로시저나 함수 실행 |

## 기본 사용자와 스키마

`dbo`, `sys`, `guest`는 단순한 권한 이름이 아니다. SQL Server가 기본으로 사용하는 **사용자 또는 스키마**이며, 각각에게 권한이 연결되는 구조이다.

### dbo — Database Owner

`dbo`는 **Database Owner**의 약자로, 다음 두 가지 의미로 사용된다.

1. 데이터베이스 소유자를 나타내는 특별한 사용자
2. 업무용 테이블 등이 많이 생성되는 기본 스키마

```sql
SELECT *
FROM dbo.Employees;
```

위 명령에서 `dbo`는 스키마, `Employees`는 테이블 이름이다.

```text
회사 Database
└─ dbo Schema
   ├─ Employees Table
   ├─ Departments Table
   └─ Sales Table
```

`dbo`는 데이터베이스에서 강한 권한을 가지므로 용도를 모르는 상태에서 삭제하거나 변경하면 안 된다.

### sys — System

`sys`는 SQL Server가 관리하는 시스템 정보와 카탈로그 뷰가 들어 있는 스키마이다.

```sql
SELECT * FROM sys.tables;    -- 현재 DB의 테이블 목록
SELECT * FROM sys.columns;   -- 컬럼 정보
SELECT * FROM sys.objects;   -- 테이블, 뷰 등 객체 정보
```

업무용 테이블을 `sys` 아래에 만들거나 시스템 객체를 직접 수정하는 용도로 사용하지 않는다.

### guest — Guest User

`guest`는 해당 데이터베이스에 별도 사용자로 등록되지 않은 Login의 접근을 처리하기 위한 내장 사용자이다.

`guest`에게 `CONNECT` 권한이 부여되어 있으면, SQL Server에는 접속했지만 해당 데이터베이스의 사용자가 아닌 Login도 제한적으로 접근할 수 있다. 불필요하게 활성화하면 의도하지 않은 접근이 발생할 수 있으므로 일반 업무용 데이터베이스에서는 제한하는 것이 보통이다.

목록에 `guest`가 보인다는 사실만으로 현재 활성화되었다고 판단할 수는 없다.

### INFORMATION_SCHEMA

테이블, 컬럼 등 데이터베이스 구조를 표준 형식으로 조회할 수 있도록 제공되는 시스템 스키마이다.

```sql
SELECT *
FROM INFORMATION_SCHEMA.TABLES;
```

## 다른 DBMS의 유사한 개념

다른 DBMS에도 관리자, 기본 스키마, 시스템 정보 영역이 있지만 이름과 동작 방식이 다르다.

| 역할 | SQL Server | PostgreSQL | MySQL | Oracle |
|---|---|---|---|---|
| 대표 관리자 | `sa`, `dbo` | `postgres` | `root` | `SYS`, `SYSTEM` |
| 기본 업무 스키마 | `dbo` | `public` | 데이터베이스 단위로 주로 관리 | 사용자별 스키마 |
| 시스템 정보 | `sys` | `pg_catalog` | `mysql`, `sys` | `SYS` |
| 표준 구조 정보 | `INFORMATION_SCHEMA` | `information_schema` | `information_schema` | 데이터 딕셔너리 |

각 항목은 역할이 비슷한 부분이 있지만 완전히 동일한 개념은 아니다.

## SSMS

**SSMS — SQL Server Management Studio**는 SQL Server에 접속해 관리 작업을 수행하는 프로그램이다.

- 데이터베이스와 테이블 확인
- SQL 작성 및 실행
- Login과 사용자 권한 관리
- 데이터 백업 및 복원
- 서버 상태와 오류 확인

```text
SSMS       = SQL Server에 접속하는 관리 도구
SQL        = SQL Server에 명령하는 언어
SQL Server = 실제 데이터를 저장하고 관리하는 시스템
```

## 개발 DB와 운영 DB

- **개발 DB:** 기능 개발과 테스트에 사용하는 데이터베이스
- **운영 DB:** 실제 회사 업무에서 사용하는 데이터베이스

운영 DB의 데이터를 직접 수정하면 실제 업무 장애나 데이터 오류가 발생할 수 있다. 일반적으로 개발 DB에서 먼저 검증하고, 승인과 백업 등 회사의 변경 절차를 거쳐 운영 DB에 반영한다.

## 실무 표현

### “MS-SQL에서 데이터를 조회해 주세요.”

SQL Server에 접속하여 필요한 데이터를 SQL로 조회해 달라는 뜻이다.

### “DB 백업을 받아 주세요.”

장애나 데이터 손상 시 복구할 수 있도록 데이터베이스 복사본을 만들어 달라는 뜻이다.

### “운영 DB에서 직접 수정하지 마세요.”

실제 업무 데이터에 영향을 줄 수 있으므로 승인된 변경 절차를 따르라는 뜻이다.

### “개발 DB에서 먼저 테스트해 주세요.”

운영 데이터에 영향을 주지 않도록 별도의 테스트 환경에서 먼저 검증하라는 뜻이다.

## 한 줄 정리

> Microsoft SQL Server는 회사의 데이터를 구조적으로 저장·조회·수정하고, 사용자 권한과 백업 등을 관리하는 Microsoft의 관계형 데이터베이스 관리 시스템이다.
