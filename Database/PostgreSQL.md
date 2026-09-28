## PostgreSQL

- 오픈소스 객체 관계형 데이터베이스 관리 시스템(ORDBMS)
- 데이터를 테이블 형태로 저장하고 SQL을 사용하여 조회·등록·수정·삭제
- 일반적인 관계형 데이터뿐 아니라 JSON, 배열, UUID, 공간정보 등 다양한 데이터 형식을 지원
- 트랜잭션, 동시성 제어, 데이터 무결성을 제공하여 웹 서비스와 업무 시스템의 핵심 데이터베이스로 사용

```text
┌──────────────────────────────────┐
│          PostgreSQL              │
│                                  │
│ Table       → 데이터 저장        │
│ SQL         → 데이터 처리        │
│ Transaction → 작업 단위 보장     │
│ Index       → 조회 성능 향상      │
│ Constraint  → 데이터 무결성      │
│ Role / RLS  → 접근 권한 관리     │
└──────────────────────────────────┘
```

PostgreSQL은 단순히 데이터를 저장하는 프로그램이 아니라, 여러 사용자가 동시에 데이터를 안전하게 처리하도록 관리하는 데이터베이스 서버이다.

</br>

### 핵심 구성

**Database**

- 하나의 PostgreSQL 서버 안에 여러 데이터베이스를 생성 가능
- 일반적으로 서비스나 시스템 단위로 데이터베이스를 분리

**Schema**

- 테이블, 뷰, 함수 등을 묶는 논리적인 공간
- 기본 스키마는 `public`
- 같은 데이터베이스 안에서 업무 영역별로 객체를 구분할 때 사용

**Table**

- 행(Row)과 열(Column)로 데이터를 저장
- 기본키, 외래키, `NOT NULL`, `UNIQUE`, `CHECK` 등의 제약조건으로 잘못된 데이터 입력을 방지

**SQL**

- DDL: `CREATE`, `ALTER`, `DROP`처럼 구조를 정의
- DML: `SELECT`, `INSERT`, `UPDATE`, `DELETE`처럼 데이터를 처리
- DCL: `GRANT`, `REVOKE`처럼 권한을 관리
- TCL: `COMMIT`, `ROLLBACK`처럼 트랜잭션을 제어

</br>

### 주요 특징

**트랜잭션과 ACID**

- 여러 SQL 작업을 하나의 작업 단위로 처리
- 작업이 모두 성공하면 `COMMIT`, 문제가 생기면 `ROLLBACK`
- 데이터의 일관성과 안정성을 유지

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 10000
WHERE id = 1;

UPDATE accounts
SET balance = balance + 10000
WHERE id = 2;

COMMIT;
```

**MVCC(Multi-Version Concurrency Control)**

- 데이터를 수정할 때 기존 데이터를 즉시 덮어쓰지 않고 여러 버전으로 관리
- 조회 작업과 수정 작업이 서로를 과도하게 막지 않아 동시 처리에 유리
- 오래된 행 버전은 `VACUUM` 작업으로 정리

**다양한 데이터 타입**

- 숫자, 문자열, 날짜, Boolean 같은 기본 타입
- `UUID`, `ARRAY`, `JSON`, `JSONB`, Range, 네트워크 주소 등의 타입
- `JSONB`를 사용하면 JSON 문서를 저장하면서 인덱스와 검색 기능을 함께 사용 가능

**인덱스**

- 자주 조회하는 열의 검색 속도를 높이는 구조
- 기본적인 B-tree 외에도 GIN, GiST, BRIN 등 여러 인덱스 방식을 지원
- 인덱스가 많으면 조회는 빨라질 수 있지만 등록·수정 비용과 저장 공간이 증가

**확장 기능**

- 필요한 기능을 Extension으로 추가 가능
- `PostGIS`: 위치·공간정보 처리
- `pgvector`: 벡터와 임베딩 저장 및 유사도 검색
- `pg_cron`: 데이터베이스 내부의 예약 작업

**보안과 권한**

- Role을 기준으로 접속 및 객체 권한을 관리
- `GRANT`, `REVOKE`로 테이블과 함수의 접근 권한을 설정
- RLS(Row Level Security)를 사용하면 같은 테이블에서도 사용자별로 접근 가능한 행을 제한 가능

</br>

### 기본 SQL 예시

```sql
-- 테이블 생성
CREATE TABLE members (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 데이터 등록
INSERT INTO members (name, email)
VALUES ('홍길동', 'hong@example.com');

-- 데이터 조회
SELECT id, name, email
FROM members
WHERE name = '홍길동';

-- 데이터 수정
UPDATE members
SET email = 'new@example.com'
WHERE id = 1;

-- 데이터 삭제
DELETE FROM members
WHERE id = 1;
```

</br>

### 장점

**데이터 무결성과 안정성**

- 트랜잭션과 제약조건을 통해 데이터 오류를 줄일 수 있음
- 복잡한 관계와 업무 규칙을 데이터베이스에 명확하게 표현 가능

**표준 SQL과 강력한 조회 기능**

- JOIN, 집계, 서브쿼리, CTE, Window Function 등 복잡한 데이터 분석을 지원
- 관계형 데이터 처리와 JSON 문서 처리를 함께 사용 가능

**확장성과 이식성**

- 무료 오픈소스이며 특정 클라우드 업체에 종속되지 않음
- 자체 서버, Docker, AWS, Azure, Supabase 등 다양한 환경에서 운영 가능
- 함수, 데이터 타입, 인덱스, Extension을 추가하여 기능 확장 가능

### 단점

**운영 지식 필요**

- 백업, 복구, 권한, 연결 수, 모니터링 등을 직접 운영하려면 데이터베이스 관리 지식이 필요
- 쿼리와 인덱스 설계가 잘못되면 데이터가 증가할수록 성능이 저하될 수 있음

**수평 확장의 복잡성**

- 단일 서버의 성능을 높이는 수직 확장은 비교적 쉽지만, 데이터를 여러 서버로 분산하는 수평 확장은 별도 설계가 필요
- 읽기 복제본, 파티셔닝, 샤딩 등을 서비스 규모에 맞게 검토해야 함

**스키마 변경 관리**

- 운영 중인 테이블 구조를 변경할 때 데이터와 애플리케이션의 호환성을 함께 고려해야 함
- Migration 파일을 사용하여 변경 이력을 관리하는 것이 안전

</br>

### Supabase와의 관계

- Supabase 프로젝트의 핵심 데이터베이스가 PostgreSQL
- Supabase는 PostgreSQL 위에 Auth, Storage, Realtime, 자동 생성 API, Edge Functions 등의 기능을 추가로 제공
- Supabase Dashboard에서 만든 테이블도 실제 PostgreSQL 테이블이므로 SQL과 PostgreSQL 기능을 그대로 사용 가능

```text
Supabase = PostgreSQL + Auth + Storage + Realtime + API + Functions
```

- PostgreSQL을 이해하면 Supabase의 테이블 관계, SQL, 함수, 인덱스, RLS를 더 정확하게 설계할 수 있음
