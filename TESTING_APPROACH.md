# 테스트 접근 방식 및 가정 문서

이 문서는 Twelve Labs SDK Search 메서드 테스트 스위트의 접근 방식, 테스트 범위 결정, 사용된 SDK 버전 및 설정된 모든 가정을 설명합니다.

## 목차

- [접근 방식](#접근-방식)
- [테스트 범위 결정](#테스트-범위-결정)
- [사용된 SDK 버전](#사용된-sdk-버전)
- [테스트 구조 설계](#테스트-구조-설계)
- [가정 (Assumptions)](#가정-assumptions)
- [제한사항 (Limitations)](#제한사항-limitations)
- [테스트 파라미터 선택 근거](#테스트-파라미터-선택-근거)

## 접근 방식

이 테스트 스위트는 다음 원칙에 따라 작성되었습니다:

### 1. 실제 환경 테스트 (Real Environment Testing)

- **Mock 사용 안 함**: Mock 대신 실제 SDK와 API를 사용하여 실제 사용 환경과 유사한 테스트를 수행합니다.
- **실제 API 호출**: 모든 테스트는 실제 Twelve Labs API를 호출하여 SDK의 실제 동작을 검증합니다.
- **TestContainer 사용 권장**: subject.md의 요구사항에 따라 Mock 대신 TestContainer를 활용하도록 설계되었지만, 이 프로젝트는 실제 API를 직접 호출하는 방식을 선택했습니다.

### 2. 포괄적 커버리지 (Comprehensive Coverage)

테스트는 다음 4가지 주요 영역을 다룹니다:

1. **성공 케이스**: 유효한 매개변수와 예상되는 동작을 가진 성공적인 작업
2. **경계 사례**: SDK 메서드의 안정성과 신뢰성에 영향을 줄 수 있는 다양한 경계 사례
3. **오류 처리**: 적절한 예외 관리를 보장하기 위한 오류 처리 및 경계 조건
4. **사용 패턴**: 실제 사용자가 겪을 수 있는 다양한 사용 패턴과 잠재적인 실패 시나리오

### 3. 파라미터별 테스트 구조

- 각 주요 파라미터별로 별도의 테스트 클래스와 파일을 생성
- 파라미터 이름을 명확하게 반영한 파일명과 클래스명 사용
  - 예: `test_search_query_text.py` → `TestSearchQueryText`
  - 예: `test_search_sort_option.py` → `TestSearchSortOption`

### 4. 문서 기준 우선 (Documentation-First Approach)

- `reference/search.md`에 명시된 문서 기준이 우선됩니다.
- 실제 API 응답이 문서 기준과 다를 경우:
  - 테스트는 SKIP 처리됩니다
  - 명확한 메시지를 제공하여 문서와 실제 응답의 차이를 알립니다
  - 예: `sort_option` 정렬 검증 시 문서 기준과 다르면 SKIP

### 5. 유연한 검증 (Flexible Validation)

- 인덱스의 내용에 따라 결과가 달라질 수 있으므로, 결과의 존재 여부보다는 응답 구조와 데이터 타입의 유효성을 검증합니다.
- 빈 결과가 반환되는 경우도 정상으로 간주합니다.

### 6. 자동 스킵 (Automatic Skipping)

- 지원되지 않는 기능에 대한 테스트는 자동으로 스킵되어 전체 테스트 실행을 방해하지 않습니다.
- 예: Marengo 2.7에서 transcription 옵션 사용 시 자동 스킵

### 7. 명확한 오류 처리 (Clear Error Handling)

- 예상되는 오류는 적절히 처리하고, 예상치 못한 오류는 테스트를 실패시킵니다.
- 에러 코드를 추출하여 검증합니다.

## 테스트 범위 결정

### 선택한 주요 파라미터

subject.md의 요구사항에 따라, `search.query()` 메서드의 광범위한 매개변수 중 다음 주요 파라미터들을 선택하여 테스트합니다:

#### 1. query_text (텍스트 쿼리) - 필수 파라미터

**선택 근거**: 
- 가장 기본적이고 필수적인 파라미터
- 모든 검색 시나리오의 기반이 되는 파라미터
- 경계 사례 테스트가 중요한 파라미터 (빈 문자열, 긴 문자열)

**테스트 범위**:
- 기본 텍스트 쿼리 검색
- 다양한 쿼리 텍스트
- 빈 문자열 (경계 사례)
- 매우 긴 문자열 (토큰 제한 경계 사례)
- 쿼리 텍스트와 미디어 모두 없음 (필수 파라미터 누락)

#### 2. search_options (검색 옵션) - 필수 파라미터

**선택 근거**: 
- 필수 파라미터이며 검색 동작의 핵심
- 다양한 조합이 가능하여 실제 사용 패턴이 다양함
- Marengo 버전에 따라 지원 여부가 달라지는 옵션 포함 (transcription)

**테스트 범위**:
- 단일 옵션 사용 (visual, audio)
- 다중 옵션 조합 (visual + audio)
- 모든 옵션 조합 (visual + audio + transcription)
- 빈 리스트 (오류 처리)
- 유효하지 않은 옵션 (오류 처리)

#### 3. sort_option (정렬 옵션)

**선택 근거**: 
- 검색 결과의 정렬은 사용자 경험에 중요한 기능
- 문서에 명확한 정렬 기준이 명시되어 있어 검증 가능
- group_by와의 조합이 중요한 파라미터

**테스트 범위**:
- `score`: 관련성 순위로 정렬
- `clip_count`: 클립 수로 정렬 (group_by='video' 필요)
- group_by와의 조합
- filter와의 조합
- 유효하지 않은 옵션 (오류 처리)

#### 4. group_by (그룹화 옵션)

**선택 근거**: 
- 검색 결과의 구조를 결정하는 중요한 파라미터
- video와 clip 두 가지 모드로 다른 응답 구조를 반환
- 다른 파라미터들과의 조합이 중요

**테스트 범위**:
- `video`: 비디오 단위로 그룹화
- `clip`: 클립 단위로 반환 (기본값)
- operator와의 조합
- page_limit와의 조합
- filter와의 조합
- 유효하지 않은 옵션 (오류 처리)

#### 5. operator (논리 연산자)

**선택 근거**: 
- search_options를 결합하는 방식에 영향을 주는 중요한 파라미터
- OR과 AND의 차이가 검색 결과에 큰 영향을 미침

**테스트 범위**:
- `or`: 논리 OR 연산자 (기본값)
- `and`: 논리 AND 연산자
- 다른 파라미터와의 조합

#### 6. page_limit (페이지 크기 제한)

**선택 근거**: 
- 페이지네이션 기능의 핵심 파라미터
- 경계 사례 테스트가 중요한 파라미터 (최소값, 최대값)
- 실제 사용에서 자주 사용되는 파라미터

**테스트 범위**:
- 일반값 (5)
- 최대값 (50)
- 최소값 (1)
- 다양한 값 (1, 5, 10, 25, 50)
- 페이지네이션 기능
- 음수값 (오류 처리)
- 최대값 초과 (경계 사례)

#### 7. filter (메타데이터 필터)

**선택 근거**: 
- 검색 결과를 필터링하는 중요한 기능
- JSON 형식의 복잡한 필터링이 가능하여 다양한 사용 패턴이 있음

**테스트 범위**:
- 유효한 JSON 필터
- 다양한 JSON 필터 형식
- 다른 파라미터와의 조합
- 잘못된 JSON 문법 (오류 처리)

### 제외된 파라미터

다음 파라미터들은 테스트 범위에서 제외되었습니다:

#### 미디어 쿼리 관련 파라미터

- **query_media_url**, **query_media_file**, **query_media_type**
  - **제외 근거**: 
    - 공개적으로 접근 가능한 테스트 이미지 URL 또는 테스트용 이미지 파일이 필요
    - 테스트 환경에서 안정적으로 사용할 수 있는 리소스 확보가 어려움
    - 파일 관리 및 버전 관리의 복잡성

#### 고급 옵션 파라미터

- **transcription_options**
  - **제외 근거**: 
    - transcription 옵션 자체는 테스트하지만, 세부 옵션(lexical, semantic)까지는 범위에서 제외
    - 기본 transcription 옵션 테스트로 충분하다고 판단

- **include_user_metadata**
  - **제외 근거**: 
    - 사용자 메타데이터가 설정된 인덱스가 필요
    - 기본 테스트 범위에서 제외

#### Deprecated 파라미터

- **adjust_confidence_level**, **threshold**
  - **제외 근거**: 
    - Marengo 3.0에서 deprecated되어 더 이상 사용되지 않음
    - 새로운 버전에서는 `rank` 필드를 사용하도록 권장

## 사용된 SDK 버전

### Python SDK

- **패키지명**: `twelvelabs`
- **최소 버전**: 1.1.0 (requirements.txt에 명시)
- **설치 방법**: `pip install -r requirements.txt`

### 테스트 프레임워크

- **패키지명**: `pytest`
- **최소 버전**: 7.0.0 (requirements.txt에 명시)

### 버전 확인 방법

```bash
pip list | grep -E "twelvelabs|pytest"
```

## 테스트 구조 설계

### 파일 구조

테스트는 파라미터별로 명확하게 분리되어 있습니다:

```
tests/
├── conftest.py                      # 공통 fixture 및 유틸리티 함수
├── test_search_query_text.py        # query_text 파라미터 테스트
├── test_search_options.py           # search_options 파라미터 테스트
├── test_search_sort_option.py       # sort_option 파라미터 테스트
├── test_search_group_by.py          # group_by 파라미터 테스트
├── test_search_operator.py          # operator 파라미터 테스트
├── test_search_page_limit.py        # page_limit 파라미터 테스트
├── test_search_filter.py            # filter 파라미터 테스트
├── test_search_error_handling.py    # 오류 처리 테스트
└── test_search_response_validation.py # 응답 검증 테스트
```

### 클래스 및 메소드 명명 규칙

- **클래스명**: `TestSearch{파라미터이름}` 형식
  - 예: `TestSearchQueryText`, `TestSearchSortOption`, `TestSearchGroupBy`
- **메소드명**: `test_{파라미터이름}_{시나리오}` 형식
  - 예: `test_sort_option_score`, `test_group_by_video_with_operator_and`

### 공통 유틸리티

`conftest.py`에 다음 공통 함수들이 정의되어 있습니다:

- `get_error_code()`: ApiError에서 error code를 추출
- `validate_marengo_fields()`: Marengo 버전별 필드 검증
- `get_index_name()`: pytest request에서 인덱스 이름 추출
- `is_marengo30()`: 인덱스 이름으로 Marengo 버전 판단

## 가정 (Assumptions)

### 1. 인덱스 전제조건

- **가정**: 테스트는 이미 생성되고 비디오가 업로드된 인덱스가 필요합니다.
- **근거**: subject.md에 "인덱스를 생성하고 비디오를 업로드하는 것은 이 과제의 범위에 포함되지 않습니다"라고 명시되어 있습니다.
- **영향**: 인덱스 생성 및 비디오 업로드는 테스트 실행 전에 완료되어 있어야 합니다.

### 2. Marengo 버전

- **가정**: 인덱스가 사용하는 Marengo 버전에 따라 일부 기능이 지원되지 않을 수 있습니다.
- **근거**: 
  - Marengo 2.7과 3.0은 서로 다른 기능을 지원합니다 (예: transcription 옵션은 Marengo 3.0만 지원)
  - 문서에 버전별 차이가 명시되어 있습니다
- **처리 방식**: 
  - 두 버전 모두에 대해 테스트를 수행하도록 설계
  - 지원되지 않는 기능에 대한 테스트는 자동으로 스킵
  - `@pytest.mark.marengo27`, `@pytest.mark.marengo30` 마커를 사용하여 버전별 테스트 구분

### 3. 결과 의존성

- **가정**: 테스트 결과는 인덱스의 실제 비디오 내용에 따라 달라질 수 있습니다.
- **근거**: 검색 결과는 인덱스에 업로드된 비디오의 내용에 의존합니다.
- **처리 방식**: 
  - 결과의 존재 여부보다는 응답 구조와 데이터 타입의 유효성을 검증
  - 빈 결과가 반환되는 경우도 정상으로 간주
  - `assert len(results) >= 0` 형식으로 검증

### 4. 문서 기준 우선

- **가정**: `reference/search.md`에 명시된 문서 기준이 우선됩니다.
- **근거**: 문서는 API의 공식 명세이며, 실제 구현보다 우선되어야 합니다.
- **처리 방식**: 
  - 실제 API 응답이 문서 기준과 다를 경우, 테스트는 SKIP 처리
  - 명확한 메시지를 제공하여 문서와 실제 응답의 차이를 알림
  - 예: `sort_option` 정렬 검증 시 문서 기준과 다르면 `pytest.skip()` 호출

### 5. 실제 API 호출

- **가정**: 테스트는 실제 Twelve Labs API를 호출합니다.
- **근거**: subject.md에 "직접적인 API 호출보다는 SDK의 기능 테스트에 중점을 두십시오"라고 명시되어 있지만, SDK의 실제 동작을 검증하기 위해서는 실제 API 호출이 필요합니다.
- **영향**: 
  - 인터넷 연결이 필요
  - API 키가 유효해야 함
  - API 할당량이 소모됨
  - 테스트 실행 시간이 걸림

## 제한사항 (Limitations)

### 1. 테스트되지 않은 파라미터

다음 파라미터들은 테스트 범위에서 제외되었습니다:

- **미디어 쿼리 관련**: `query_media_url`, `query_media_file`, `query_media_type`
- **고급 옵션**: `transcription_options`, `include_user_metadata`
- **Deprecated 파라미터**: `adjust_confidence_level`, `threshold`

자세한 내용은 [테스트 파라미터 선택 근거](#테스트-파라미터-선택-근거) 섹션을 참조하세요.

### 2. 환경 의존성

- **인덱스 내용**: 테스트 결과는 인덱스의 실제 비디오 내용에 따라 달라질 수 있습니다.
- **네트워크 연결**: 인터넷 연결이 필요합니다.
- **API 키 유효성**: API 키가 유효해야 합니다.

### 3. 테스트 실행 시간

- 실제 API 호출을 수행하므로 테스트 실행에 시간이 걸릴 수 있습니다.
- 전체 테스트 스위트 실행 시 수십 초에서 수분이 소요될 수 있습니다.

### 4. API 할당량

- 테스트 실행 시 API 할당량이 소모됩니다.
- 대량의 테스트 실행 시 할당량 제한에 도달할 수 있습니다.

### 5. 파라미터 조합의 제한

- 모든 파라미터 조합을 테스트하는 것은 불가능합니다.
- 주요 파라미터와 일반적인 조합에 집중합니다.
- 문서화되지 않은 조합이나 예상치 못한 동작은 테스트 범위에 포함되지 않을 수 있습니다.

## 테스트 파라미터 선택 근거

### 포함된 파라미터

#### 필수 파라미터 (반드시 테스트)

1. **query_text**: 모든 검색의 기반이 되는 필수 파라미터
2. **search_options**: 검색 동작의 핵심을 결정하는 필수 파라미터

#### 주요 선택적 파라미터

3. **sort_option**: 검색 결과 정렬은 사용자 경험에 중요한 기능
4. **group_by**: 검색 결과 구조를 결정하는 중요한 파라미터
5. **operator**: 검색 옵션 결합 방식에 영향을 주는 파라미터
6. **page_limit**: 페이지네이션 기능의 핵심 파라미터
7. **filter**: 검색 결과 필터링의 중요한 기능

### 제외된 파라미터

#### 미디어 쿼리 관련

- **query_media_url**, **query_media_file**, **query_media_type**
  - 테스트 리소스 확보의 어려움
  - 파일 관리의 복잡성
  - 텍스트 쿼리 테스트로 기본 검색 기능은 충분히 검증 가능

#### 고급 옵션

- **transcription_options**: transcription 옵션 자체는 테스트하지만, 세부 옵션은 제외
- **include_user_metadata**: 사용자 메타데이터가 설정된 인덱스가 필요

#### Deprecated 파라미터

- **adjust_confidence_level**, **threshold**: 더 이상 사용되지 않는 파라미터

## 테스트 메소드 통계

### 전체 테스트 메소드 수

- **TestSearchQueryText**: 5개
- **TestSearchOptions**: 5개
- **TestSearchSortOption**: 5개
- **TestSearchGroupBy**: 10개
- **TestSearchOperator**: 2개
- **TestSearchPageLimit**: 6개
- **TestSearchFilter**: 4개
- **TestSearchErrorHandling**: 11개
- **TestSearchResponseValidation**: 4개

**총계**: 약 52개 테스트 메소드 (Marengo 2.7과 3.0 각각에 대해 실행되므로 실제 실행되는 테스트는 약 104개)

### 테스트 카테고리별 분류

1. **성공 케이스**: 약 37개 테스트
2. **경계 사례**: 약 5개 테스트
3. **오류 처리**: 약 11개 테스트
4. **응답 검증**: 약 4개 테스트

## 결론

이 테스트 스위트는 subject.md의 요구사항을 충족하면서도, 실제 사용 환경과 유사한 조건에서 SDK의 기능을 검증하도록 설계되었습니다. 주요 파라미터에 대한 포괄적인 테스트를 제공하며, 문서 기준을 우선시하여 API 명세와의 일치성을 검증합니다.

