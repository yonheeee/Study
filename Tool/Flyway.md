# Flyway

## 분류

```text
Tool > Database Migration
```

Flyway는 데이터베이스 제품이 아니라 **데이터베이스 변경 SQL을 버전 순서대로 실행하고 적용 이력을 관리하는 도구**이다.

## 기본 개념

프로그램 기능이 변경되면 테이블, 컬럼, 인덱스 같은 데이터베이스 구조도 함께 변경될 수 있다. 사람이 개발·테스트·운영 DB에서 각각 SQL을 실행하면 누락이나 순서 오류가 생길 수 있다.

Flyway는 변경 SQL을 버전 파일로 관리하고, 아직 적용하지 않은 파일만 실제 DB에 실행한다.

```text
Git에 저장된 Migration SQL
              ↓
           Flyway
              ↓
실제 SQL Server 구조 변경
              ↓
flyway_schema_history에 실행 이력 기록
```

Flyway는 SQL 파일을 단순히 저장하는 보관함이 아니다. SQL 파일은 보통 프로그램 프로젝트와 Git에 저장되고, Flyway는 그 파일을 읽어 DB에 실행하고 실행 결과를 기록한다.

## 사용하는 이유

- 개발·테스트·운영 DB의 구조를 같은 상태로 유지
- DB 변경 내용을 Git에서 코드와 함께 관리
- 변경 SQL의 실행 순서 보장
- 이미 실행된 SQL의 중복 실행 방지
- 누가 언제 어떤 변경을 적용했는지 추적
- 새로운 테스트 DB를 동일한 구조로 재생성
- CI/CD 파이프라인에서 DB 변경 자동화

### Flyway가 없을 때 발생할 수 있는 문제

```text
개발 DB  → email 컬럼 추가 완료
테스트 DB → 적용 누락
운영 DB  → 적용 순서 오류
```

프로그램은 `email` 컬럼이 있다고 생각하지만 운영 DB에 컬럼이 없다면 실행 중 오류가 발생할 수 있다.

## Migration 파일 이름

### Versioned Migration

한 번만 실행되는 일반적인 변경 파일이다.

```text
V1__create_employee_table.sql
V2__add_email_column.sql
V3__create_department_table.sql
```

```text
V2__add_email_column.sql
│    └─ 변경 내용 설명
└─ 실행 버전
```

예시:

```sql
-- V2__add_email_column.sql

ALTER TABLE dbo.Employees
ADD email VARCHAR(100);
```

### Repeatable Migration

파일 내용이 변경될 때마다 다시 실행되는 Migration이다.

```text
R__create_employee_view.sql
R__create_monthly_sales_procedure.sql
```

주로 View, Stored Procedure, Function처럼 정의 전체를 다시 적용할 수 있는 객체에 사용한다.

## 실행 과정

```text
1. Flyway가 Migration 폴더를 확인
2. flyway_schema_history에서 적용 이력 확인
3. 아직 실행하지 않은 Versioned Migration을 버전 순서대로 실행
4. 변경된 Repeatable Migration 실행
5. 성공·실패 결과와 Checksum을 이력 테이블에 기록
```

예를 들어 현재 DB에 `V1`, `V2`가 적용되어 있고 프로젝트에 `V3`이 추가되었다면 `V3`만 실행한다.

```text
V1 → 이미 실행됨: 건너뜀
V2 → 이미 실행됨: 건너뜀
V3 → 실행되지 않음: 실행
```

## flyway_schema_history

Flyway가 Migration 적용 상태를 기록하는 이력 테이블이다.

| 기록 내용 | 의미 |
|---|---|
| Version | 적용된 Migration 버전 |
| Description | 파일 이름에 작성한 변경 설명 |
| Script | 실행된 파일 이름 |
| Checksum | 실행 당시 파일 내용을 계산한 검사값 |
| Installed By | 실행한 DB 사용자 |
| Installed On | 실행 시간 |
| Success | 성공 여부 |

이 테이블은 DB 변경 이력이지 실제 업무 데이터의 백업이 아니다.

## Checksum과 적용 파일 수정 금지

운영 DB에 적용된 Migration 파일을 나중에 수정하면, 실행 당시 저장된 Checksum과 현재 파일의 Checksum이 달라진다.

```text
DB에 기록된 V2 Checksum: 12345
현재 파일의 V2 Checksum: 67890
                         ↓
                   validate 오류
```

적용된 파일에서 잘못된 내용을 발견하면 기존 파일을 고치지 않고 새로운 수정 Migration을 추가하는 것이 원칙이다.

```text
V2__add_email_column.sql        ← 적용된 파일이므로 유지
V3__fix_email_column_length.sql ← 새로운 수정 파일
```

## 주요 명령어

| 명령어 | 역할 |
|---|---|
| `flyway info` | 적용 완료·대기·실패 Migration 확인 |
| `flyway validate` | 프로젝트 파일과 DB 이력의 일치 여부 검사 |
| `flyway migrate` | 아직 적용되지 않은 Migration 실행 |
| `flyway baseline` | 기존 DB를 특정 버전까지 적용된 상태로 등록 |
| `flyway repair` | 이력 테이블의 실패 기록 또는 Checksum 등을 정리 |
| `flyway clean` | 관리 대상 DB 객체 삭제 |

### 주의할 명령어

`clean`은 테이블·뷰 등 DB 객체를 삭제할 수 있으므로 운영 환경에서는 일반적으로 비활성화한다.

`repair`는 실제 DB 구조를 원하는 상태로 고치는 명령이 아니다. 이력 테이블을 정리하는 기능이므로 실제 DB 상태를 확인하지 않고 사용하면 문제를 숨길 수 있다.

## 기존 DB와 Baseline

이미 운영 중인 DB에 Flyway를 나중에 도입하면 기존 테이블이 Migration 없이 존재할 수 있다.

```text
기존 운영 DB 상태를 V10으로 Baseline
                    ↓
V11부터 Flyway Migration 적용
```

Baseline은 현재 DB의 SQL 파일을 자동 생성하는 기능이 아니다. **현재 DB가 특정 버전까지 적용된 것으로 이력에 표시하는 기능**이다. 버전을 잘못 지정하면 필요한 Migration을 건너뛸 수 있으므로 기존 구조와 변경 이력을 먼저 확인해야 한다.

## Schema라는 단어의 구분

Flyway를 공부할 때 다음 두 의미를 구분해야 한다.

### SQL Server Schema

테이블과 뷰 등의 이름과 소속을 구분하는 논리적 구역이다.

```text
dbo.Employees
hr.Employees
```

### Database Schema

테이블, 컬럼, 인덱스, 뷰 등 DB 구조 전체를 뜻하기도 한다.

`flyway_schema_history`는 DB 구조 자체가 아니라 **DB 구조 변경 이력을 기록하는 테이블**이다.

## Schema Drift

운영 담당자가 Flyway를 사용하지 않고 SSMS에서 DB를 직접 변경하면 Flyway 이력과 실제 DB 구조가 달라질 수 있다. 이를 Schema Drift라고 한다.

```text
Flyway 기록: V1, V2
실제 운영 DB: V1, V2 + 수동 추가 컬럼
```

긴급하게 운영 DB를 직접 수정했다면 변경 내용을 정식 Migration으로 남기고 다른 환경에도 반영하는 절차가 필요하다.

## 일반적인 실무 흐름

```text
1. 개발자가 Migration SQL 작성
2. Git에 등록하고 코드 리뷰
3. 임시 또는 개발 DB에서 실행 검증
4. 테스트·스테이징 DB에 반영
5. 운영용 변경 SQL과 영향 확인
6. 담당자 또는 DBA 승인
7. 배포 전용 계정으로 운영 DB에 적용
8. 실행 결과와 로그 확인
```

Flyway를 사용한다고 해서 개발자가 운영 DB를 마음대로 변경한다는 의미는 아니다. 자동화 과정 중간에 SQL 검토와 운영 승인 단계를 둘 수 있다.

## 보안 원칙

- 개발·테스트·운영 DB 접속정보 분리
- DB 비밀번호를 Migration이나 Git에 저장하지 않기
- CI/CD Secret 또는 회사의 비밀정보 관리 시스템 사용
- Flyway용 배포 계정과 애플리케이션 실행 계정 분리
- 배포 계정에는 필요한 최소 권한만 부여
- 운영 DB 접근 가능 네트워크 제한
- 운영 반영 전 코드 리뷰와 승인 수행
- 누가 언제 실행했는지 감사 로그 기록

```text
CI/CD 배포 계정
→ 배포할 때만 DB 구조 변경 권한 사용

애플리케이션 계정
→ 평상시 필요한 조회·입력·수정 권한만 사용
```

## 롤백과 복구

Flyway는 DB 백업 도구가 아니며 모든 변경을 자동으로 이전 상태로 돌려주지 않는다. 데이터가 삭제되면 반대 SQL만으로 원래 데이터를 복구할 수 없을 수 있다.

운영 적용 전 다음 사항을 정해야 한다.

- 실패 시 작업을 어떻게 중단할지
- 수정 Migration으로 앞으로 진행할지
- 이전 프로그램이 변경된 DB 구조에서 동작하는지
- 별도의 복구 SQL이 필요한지
- 백업에서 복원해야 하는지

문제가 있는 버전을 직접 수정하는 대신 다음 버전에서 바로잡는 방식을 Roll Forward라고 한다.

```text
V5에서 문제 발생
       ↓
V6에서 문제 수정
```

## 대용량 데이터 변경 주의

개발 DB에서 빠르게 끝난 SQL도 운영 DB의 데이터가 많으면 다음 문제를 만들 수 있다.

- 테이블 잠금
- 프로그램 응답 지연
- 트랜잭션 로그 증가
- 실행 시간 초과
- 다른 업무의 INSERT·UPDATE 대기

대량 `UPDATE`나 데이터 변환은 여러 번에 나누어 처리하거나 별도의 배치 작업으로 분리하는 방법을 검토한다.

## 무중단 변경: Expand and Contract

운영 중인 프로그램이 사용하는 컬럼을 즉시 삭제하거나 이름을 변경하면 이전 프로그램에서 오류가 발생할 수 있다.

```text
1. 새 컬럼 추가
2. 프로그램이 기존·새 컬럼을 함께 처리
3. 기존 데이터를 새 컬럼으로 이동
4. 프로그램이 새 컬럼만 사용하도록 전환
5. 다음 배포에서 기존 컬럼 삭제
```

- **Expand:** 새 구조를 먼저 추가
- **전환:** 프로그램과 데이터를 새 구조로 이동
- **Contract:** 사용하지 않는 기존 구조 제거

## 다른 방식과 비교

| 방식 | 대표 도구 | 특징 |
|---|---|---|
| Migration 기반 | Flyway | 버전별 SQL을 순서대로 실행 |
| Changelog 기반 | Liquibase | SQL·XML·YAML·JSON으로 변경 단위 관리 |
| 목표 상태 기반 | SQL Database Project, DACPAC | 현재 DB와 원하는 최종 구조를 비교하여 변경 SQL 생성 |
| ORM 기반 | EF Core Migrations | 프로그램 데이터 모델의 변경에서 Migration 생성 |
| 승인 SQL 방식 | SSMS, 사내 배포 시스템 | DBA가 검토한 SQL을 정해진 절차로 실행 |

### Flyway가 잘 맞는 경우

- SQL을 개발자가 직접 명확하게 관리하고 싶은 경우
- Java·Spring Boot 기반 애플리케이션
- 여러 DB 제품에서 비슷한 배포 흐름을 사용하려는 경우
- Git과 CI/CD를 이용해 DB 변경 이력을 관리하려는 경우

### 다른 방식을 검토할 수 있는 경우

- SQL Server의 테이블·뷰·프로시저를 객체별 최종 상태로 관리: DACPAC
- .NET과 EF Core 데이터 모델 중심 개발: EF Core Migrations
- 여러 DB에 공통적인 추상화와 세밀한 Changelog가 필요: Liquibase
- 운영 DB 변경을 DBA가 엄격히 통제: 검토된 SQL과 승인 절차

## 자주 하는 실수

- 적용 완료된 Migration 파일 수정
- 운영 DB에서 `clean` 실행
- 운영 DB를 직접 수정한 뒤 Migration에 반영하지 않음
- 운영 접속정보를 Git에 저장
- Flyway 계정을 애플리케이션 실행 계정으로 사용
- 개발 DB의 적은 데이터만 보고 운영 실행 시간을 판단
- 컬럼 삭제·자료형 변경 전 백업과 복구 계획을 세우지 않음
- Flyway 이력 테이블을 실제 데이터 백업으로 오해

## 확인 방법

프로젝트에 다음 파일과 테이블이 있다면 Flyway를 사용하고 있을 가능성이 높다.

```text
V1__...sql
V2__...sql
R__...sql
flyway.toml
flyway.conf
flyway_schema_history
```

Spring Boot 프로젝트에서는 다음 경로와 설정도 확인할 수 있다.

```text
src/main/resources/db/migration
spring.flyway.*
```

## 한 줄 정리

> Flyway는 DB 변경 SQL에 버전을 붙여 순서대로 실행하고, 어떤 변경이 어느 환경에 적용되었는지 기록하는 데이터베이스 마이그레이션 도구이다.

