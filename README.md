# Twelve Labs SDK Search 메서드 테스트 스위트

이 프로젝트는 Twelve Labs Python SDK의 `search.query()` 메서드에 대한 포괄적인 자동화 테스트 스위트입니다.

## 목차

- [개요](#개요)
- [요구사항](#요구사항)
- [설치](#설치)
- [설정](#설정)
- [테스트 실행](#테스트-실행)
- [테스트 범위](#테스트-범위)
- [테스트 구조](#테스트-구조)
- [테스트된 주요 파라미터](#테스트된-주요-파라미터)
- [테스트되지 않은 파라미터](#테스트되지-않은-파라미터)
- [사용된 SDK 버전](#사용된-sdk-버전)
- [가정 및 제한사항](#가정-및-제한사항)
- [문제 해결](#문제-해결)

## 개요

이 테스트 스위트는 Twelve Labs SDK의 Search 기능을 검증하기 위해 작성되었습니다. 다양한 검색 시나리오, 파라미터 조합, 경계 사례, 오류 처리를 포함한 포괄적인 테스트를 제공합니다.

## 요구사항

- Python 3.9 이상
- Twelve Labs API 키
- Twelve Labs 인덱스 ID (비디오가 업로드된 인덱스)
  - Marengo 2.7 인덱스 (선택사항)
  - Marengo 3.0 인덱스 (선택사항)

## 설치

### 1. 저장소 클론

```bash
git clone <repository_url>
cd TwelveLabsSdkTestSuite
```

### 2. 가상 환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. SDK 및 의존성 설치

```bash
pip install -r requirements.txt
```

설치되는 주요 패키지:
- `twelvelabs>=1.1.0`: Twelve Labs Python SDK
- `pytest>=7.0.0`: 테스트 프레임워크

## 설정

테스트를 실행하기 전에 API 키와 인덱스 ID를 설정해야 합니다.

### 방법 1: config.env 파일 사용 (권장)

1. `config.env.example` 파일을 복사하여 `config.env` 파일을 생성합니다:

```bash
cp config.env.example config.env
```

2. `config.env` 파일을 열고 실제 값을 입력합니다:

```bash
TL_API_KEY=your_api_key_here
TL_INDEX_MARENGO_27=your_marengo_27_index_id_here
TL_INDEX_MARENGO_30=your_marengo_30_index_id_here
```

**참고**: 
- `TL_INDEX_MARENGO_27`과 `TL_INDEX_MARENGO_30` 중 하나만 설정해도 됩니다.
- 설정하지 않은 인덱스에 대한 테스트는 자동으로 스킵됩니다.

### 방법 2: 환경 변수 사용

```bash
export TL_API_KEY="your_api_key_here"
export TL_INDEX_MARENGO_27="your_marengo_27_index_id_here"
export TL_INDEX_MARENGO_30="your_marengo_30_index_id_here"
```

## 테스트 실행

### 모든 테스트 실행

```bash
pytest tests/
```

### 특정 테스트 클래스 실행

```bash
# query_text 파라미터 테스트
pytest tests/test_search_query_text.py::TestSearchQueryText

# sort_option 파라미터 테스트
pytest tests/test_search_sort_option.py::TestSearchSortOption

# group_by 파라미터 테스트
pytest tests/test_search_group_by.py::TestSearchGroupBy

# operator 파라미터 테스트
pytest tests/test_search_operator.py::TestSearchOperator

# page_limit 파라미터 테스트
pytest tests/test_search_page_limit.py::TestSearchPageLimit

# filter 파라미터 테스트
pytest tests/test_search_filter.py::TestSearchFilter

# search_options 파라미터 테스트
pytest tests/test_search_options.py::TestSearchOptions

# 오류 처리 테스트
pytest tests/test_search_error_handling.py::TestSearchErrorHandling

# 응답 검증 테스트
pytest tests/test_search_response_validation.py::TestSearchResponseValidation
```

### 특정 테스트 메소드 실행

```bash
pytest tests/test_search_query_text.py::TestSearchQueryText::test_search_with_text_query
```

### 특정 파라미터로 필터링

```bash
# sort_option 관련 테스트만 실행
pytest tests/ -k "sort_option"

# group_by 관련 테스트만 실행
pytest tests/ -k "group_by"

# 오류 처리 테스트만 실행
pytest tests/test_search_error_handling.py
```

### 상세 출력과 함께 실행

```bash
pytest tests/ -v
```

**참고**: `pytest.ini` 파일에 `-s` 옵션이 기본값으로 설정되어 있어, `pytest -v`만 실행해도 에러 코드(`[ERROR CODE]`)가 출력됩니다. 이는 각 테스트에서 발생한 실제 에러 코드를 확인하는 데 유용합니다.

### Marengo 버전별 테스트 실행

```bash
# Marengo 2.7 테스트만 실행
pytest tests/ -m marengo27

# Marengo 3.0 테스트만 실행
pytest tests/ -m marengo30
```

### 테스트 커버리지 확인

```bash
pytest tests/ --cov=tests --cov-report=html
```

## 테스트 범위

이 테스트 스위트는 `search.query()` 메서드에 대한 포괄적인 검증을 제공하며, subject.md의 요구사항에 따라 다음 4가지 주요 영역을 다룹니다:

### 1. 유효한 매개변수와 예상되는 동작을 가진 성공적인 작업

#### TestSearchQueryText (5개 테스트)
- ✅ **기본 텍스트 쿼리 검색**: `query_text`와 `search_options`를 사용한 기본 검색 동작 검증
- ✅ **다양한 쿼리 텍스트**: 서로 다른 쿼리로 검색하여 일반적인 사용 패턴 검증
- ✅ **빈 쿼리 텍스트**: 빈 문자열에 대한 오류 처리 검증
- ✅ **매우 긴 쿼리 텍스트**: 토큰 제한에 대한 경계 사례 테스트
  - Marengo 2.7: 최대 77 토큰
  - Marengo 3.0: 최대 500 토큰
- ✅ **쿼리 텍스트와 미디어 모두 없음**: 필수 파라미터 누락에 대한 오류 처리

#### TestSearchOptions (5개 테스트)
- ✅ **visual과 audio 조합**: 가장 일반적인 사용 패턴 검증
- ✅ **visual 옵션만 사용**: 단일 옵션 사용 패턴 검증
- ✅ **audio 옵션만 사용**: 단일 옵션 사용 패턴 검증
- ✅ **transcription 옵션**: Marengo 3.0에서 지원하는 transcription 옵션 테스트
  - Marengo 2.7: `search_option_not_supported` 에러 발생 확인
  - Marengo 3.0: 정상 동작 확인
- ✅ **모든 옵션 조합**: `visual`, `audio`, `transcription`을 모두 사용한 조합 테스트

#### TestSearchSortOption (5개 테스트)
- ✅ **sort_option='score'**: 검색 결과를 관련성 순위로 정렬하는 기능 검증
  - 문서 기준: "Sorts results by relevance ranking in ascending order (1 = most relevant)"
  - rank/score 필드의 오름차순 정렬 확인
- ✅ **sort_option='score'와 group_by='video' 조합**: 비디오 그룹화 시 정렬 검증
  - 문서 기준: "sorts videos by highest relevance ranking (lowest number) among their clips"
- ✅ **sort_option='clip_count'와 group_by='video' 조합**: 클립 수로 정렬 검증
  - 문서 기준: "Sorts videos by the number of matching clips in descending order"
  - 각 비디오 내 클립들은 relevance ranking 오름차순 정렬 확인
- ✅ **sort_option='score'와 filter 조합**: 필터와 함께 정렬 기능 검증
- ✅ **sort_option='clip_count'와 filter 조합**: 필터와 함께 클립 수 정렬 검증

#### TestSearchGroupBy (10개 테스트)
- ✅ **group_by='video'**: 비디오 단위로 그룹화하여 반환하는 기능 검증
  - id와 clips 필드 존재 확인
- ✅ **group_by='clip'**: 클립 단위로 반환하는 기본 동작 검증
  - 개별 클립 정보(video_id, start, end) 확인
- ✅ **group_by='video'와 operator='and' 조합**: 논리 AND 연산자와 함께 사용
- ✅ **group_by='video'와 operator='or' 조합**: 논리 OR 연산자와 함께 사용
- ✅ **group_by='clip'와 operator='and' 조합**: 논리 AND 연산자와 함께 사용
- ✅ **group_by='clip'와 operator='or' 조합**: 논리 OR 연산자와 함께 사용
- ✅ **group_by='video'와 page_limit 조합**: 페이지 제한과 함께 사용
- ✅ **group_by='clip'와 page_limit 조합**: 페이지 제한과 함께 사용
- ✅ **group_by='video'와 filter 조합**: 필터와 함께 사용
- ✅ **group_by='clip'와 filter 조합**: 필터와 함께 사용

#### TestSearchOperator (2개 테스트)
- ✅ **operator='or'**: 논리 OR 연산자로 검색 옵션을 결합하는 기능 검증 (기본값)
- ✅ **operator='and'**: 논리 AND 연산자로 검색 옵션을 결합하는 기능 검증

#### TestSearchPageLimit (6개 테스트)
- ✅ **page_limit**: 페이지당 결과 수 제한 기능 검증 (일반값: 5)
- ✅ **page_limit 최대값**: 최대값(50) 테스트
- ✅ **page_limit 최소값**: 최소값(1) 경계 사례 테스트
- ✅ **page_limit 다양한 값**: 1, 5, 10, 25, 50 값으로 테스트
- ✅ **페이지네이션**: 다중 페이지 결과 처리 및 `next_page()` 메서드 동작 검증

#### TestSearchFilter (4개 테스트)
- ✅ **filter 기본**: JSON 문자열을 사용한 메타데이터 필터링 기능 검증
- ✅ **filter 다양한 형식**: 다양한 JSON 필터 형식 테스트
- ✅ **filter와 operator='and' 조합**: 논리 연산자와 함께 사용
- ✅ **filter와 operator='or' 조합**: 논리 연산자와 함께 사용

### 2. SDK 메서드의 안정성과 신뢰성에 영향을 줄 수 있는 다양한 경계 사례(edge cases)

**TestSearchQueryText**에 포함된 경계 사례:
- ✅ **빈 쿼리 텍스트**: 빈 문자열("")을 쿼리로 전달하는 경우 처리 검증
  - `parameter_not_provided` 또는 `parameter_invalid` 에러 발생 확인
- ✅ **매우 긴 쿼리 텍스트**: 토큰 제한에 근접한 긴 쿼리 테스트
  - Marengo 3.0: 최대 500 토큰까지 지원
  - Marengo 2.7: 최대 77 토큰 제한, 초과 시 `parameter_invalid` 에러 발생
- ✅ **쿼리 텍스트와 미디어 모두 없음**: 필수 파라미터가 모두 없는 경우 처리 검증
  - `parameter_not_provided` 에러 발생 확인

**TestSearchPageLimit**에 포함된 경계 사례:
- ✅ **최소 page_limit**: page_limit=1로 설정하여 최소값 경계 테스트

### 3. 적절한 예외 관리를 보장하기 위한 오류 처리 및 경계 조건(boundary conditions)

**TestSearchErrorHandling** (11개 테스트):
- ✅ **유효하지 않은 index_id**: 존재하지 않는 인덱스 ID로 검색 시 ApiError 발생 확인
- ✅ **빈 search_options**: 필수 파라미터인 search_options가 빈 리스트인 경우 예외 처리
- ✅ **유효하지 않은 search_option**: 지원되지 않는 옵션("invalid_option") 전달 시 예외 처리
- ✅ **유효하지 않은 sort_option**: 지원되지 않는 정렬 옵션 전달 시 예외 처리
- ✅ **유효하지 않은 group_by**: 지원되지 않는 그룹화 옵션 전달 시 예외 처리
- ✅ **유효하지 않은 operator**: 지원되지 않는 논리 연산자 전달 시 예외 처리
- ✅ **유효하지 않은 page_limit (음수)**: 음수값 전달 시 예외 처리
- ✅ **page_limit 최대값 초과**: 최대값(50)을 초과하는 값 전달 시 처리 검증
- ✅ **유효하지 않은 filter 문법**: 잘못된 JSON 형식의 filter 전달 시 ApiError 발생 확인
- ✅ **지원되지 않는 옵션 조합**: 특정 옵션 조합이 지원되지 않는 경우 에러 처리
- ✅ **만료된 페이지 토큰**: 페이지네이션 토큰이 만료된 경우 처리 검증

### 4. 실제 사용자가 겪을 수 있는 다양한 사용 패턴과 잠재적인 실패 시나리오

**TestSearchResponseValidation** (4개 테스트):
- ✅ **응답 구조 검증**: 검색 결과의 필수 필드 존재 및 데이터 타입 검증
  - video_id (문자열), start/end (숫자) 타입 확인
- ✅ **rank 필드 검증**: Marengo 3.0에서 반환하는 rank 필드의 유효성 검증
  - 정수 타입 및 1 이상의 값 확인
- ✅ **thumbnail_url 형식 검증**: 썸네일 URL이 올바른 HTTP URL 형식인지 확인
- ✅ **시간 범위 유효성**: start와 end 시간의 논리적 유효성 검증
  - start >= 0, end > start 확인

## 테스트 구조

```
TwelveLabsSdkTestSuite/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # pytest 설정 및 공통 fixture, 유틸리티 함수
│   ├── test_search_query_text.py        # query_text 파라미터 테스트
│   ├── test_search_options.py           # search_options 파라미터 테스트
│   ├── test_search_sort_option.py       # sort_option 파라미터 테스트
│   ├── test_search_group_by.py          # group_by 파라미터 테스트
│   ├── test_search_operator.py          # operator 파라미터 테스트
│   ├── test_search_page_limit.py        # page_limit 파라미터 테스트
│   ├── test_search_filter.py            # filter 파라미터 테스트
│   ├── test_search_error_handling.py    # 오류 처리 테스트
│   └── test_search_response_validation.py # 응답 유효성 검사 테스트
├── reference/
│   └── search.md                         # SDK Search 메서드 명세 (reference 문서)
├── config.env.example                    # 환경 변수 설정 예제
├── config.env                            # 실제 환경 변수 설정 (git에 포함되지 않음)
├── playground.py                         # API 키 및 인덱스 ID 설정 (선택사항)
├── requirements.txt                      # 프로젝트 의존성
├── pytest.ini                            # pytest 설정 (에러 코드 출력을 위한 -s 옵션 포함)
├── README.md                             # 이 파일
├── TESTING_APPROACH.md                   # 테스트 접근 방식 및 가정 문서
└── subject.md                            # 과제 요구사항
```

## 테스트된 주요 파라미터

subject.md의 요구사항에 따라, `search.query()` 메서드의 광범위한 매개변수 중 다음 주요 파라미터들을 선택하여 테스트합니다:

### 1. query_text (텍스트 쿼리) - 필수 파라미터

**테스트 범위**: 
- ✅ 정상적인 텍스트 쿼리로 검색 결과 반환
- ✅ 다양한 쿼리 텍스트로 일반적인 사용 패턴 지원
- ✅ 빈 문자열에 대한 경계 조건 처리 (`parameter_not_provided` 또는 `parameter_invalid`)
- ✅ 매우 긴 문자열에 대한 경계 조건 처리 (토큰 제한)
  - Marengo 2.7: 최대 77 토큰
  - Marengo 3.0: 최대 500 토큰

**테스트 파일**: `test_search_query_text.py` (5개 테스트)

### 2. search_options (검색 옵션) - 필수 파라미터

**테스트 범위**: 
- ✅ 단일 옵션 사용 (visual, audio)
- ✅ visual + audio 조합 (가장 일반적인 사용 패턴)
- ✅ visual + audio + transcription 조합 (Marengo 3.0)
- ✅ 빈 리스트에 대한 오류 처리
- ✅ 유효하지 않은 옵션에 대한 오류 처리

**테스트 파일**: `test_search_options.py` (5개 테스트), `test_search_error_handling.py` (2개 테스트)

### 3. sort_option (정렬 옵션)

**테스트 범위**: 
- ✅ `score`: 검색 결과를 관련성 순위로 오름차순 정렬
  - 문서 기준: "Sorts results by relevance ranking in ascending order (1 = most relevant)"
  - rank/score 필드의 오름차순 정렬 확인
- ✅ `clip_count`: 비디오를 매칭되는 클립 수로 내림차순 정렬 (group_by='video' 필요)
  - 문서 기준: "Sorts videos by the number of matching clips in descending order"
  - 각 비디오 내 클립들은 relevance ranking 오름차순 정렬 확인
- ✅ group_by='video'와의 조합 테스트
- ✅ filter와의 조합 테스트
- ✅ 유효하지 않은 옵션에 대한 오류 처리

**테스트 파일**: `test_search_sort_option.py` (5개 테스트), `test_search_error_handling.py` (1개 테스트)

### 4. group_by (그룹화 옵션)

**테스트 범위**: 
- ✅ `video`: 비디오 단위로 그룹화하여 반환
  - id와 clips 필드 존재 확인
- ✅ `clip`: 클립 단위로 반환 (기본값)
  - 개별 클립 정보(video_id, start, end) 확인
- ✅ operator와의 조합 테스트
- ✅ page_limit와의 조합 테스트
- ✅ filter와의 조합 테스트
- ✅ 유효하지 않은 옵션에 대한 오류 처리

**테스트 파일**: `test_search_group_by.py` (10개 테스트), `test_search_error_handling.py` (1개 테스트)

### 5. operator (논리 연산자)

**테스트 범위**: 
- ✅ `or`: 논리 OR 연산자로 검색 옵션을 결합 (기본값)
- ✅ `and`: 논리 AND 연산자로 검색 옵션을 결합
- ✅ group_by와의 조합 테스트
- ✅ filter와의 조합 테스트
- ✅ 유효하지 않은 연산자에 대한 오류 처리

**테스트 파일**: `test_search_operator.py` (2개 테스트), `test_search_error_handling.py` (1개 테스트)

### 6. page_limit (페이지 크기 제한)

**테스트 범위**: 
- ✅ 일반값 (5)
- ✅ 최대값 (50)
- ✅ 최소값 (1) - 경계 사례
- ✅ 다양한 값 (1, 5, 10, 25, 50)
- ✅ 페이지네이션 기능 (`next_page()` 메서드)
- ✅ 음수값에 대한 오류 처리
- ✅ 최대값 초과 (100) - 경계 사례
- ✅ group_by와의 조합 테스트

**테스트 파일**: `test_search_page_limit.py` (6개 테스트), `test_search_error_handling.py` (2개 테스트)

### 7. filter (메타데이터 필터)

**테스트 범위**: 
- ✅ 유효한 JSON 필터
- ✅ 다양한 JSON 필터 형식
- ✅ operator와의 조합 테스트
- ✅ group_by와의 조합 테스트
- ✅ sort_option과의 조합 테스트
- ✅ 잘못된 JSON 문법에 대한 오류 처리

**테스트 파일**: `test_search_filter.py` (4개 테스트), `test_search_error_handling.py` (1개 테스트)

## 테스트되지 않은 파라미터

다음 파라미터들은 테스트 범위에서 제외되었습니다:

### 미디어 쿼리 관련 파라미터
- **query_media_url**: 미디어 URL 쿼리
  - 제외 이유: 공개적으로 접근 가능한 테스트 이미지 URL이 필요하며, 테스트 환경에서 안정적으로 사용할 수 있는 URL 확보가 어려움
- **query_media_file**: 로컬 미디어 파일 쿼리
  - 제외 이유: 테스트용 이미지 파일이 필요하며, 파일 관리 및 버전 관리 복잡성
- **query_media_type**: 미디어 타입 (이미지 쿼리 테스트와 연관)
  - 제외 이유: 위의 미디어 쿼리 파라미터와 함께 테스트해야 하므로 함께 제외

### 고급 옵션 파라미터
- **transcription_options**: transcription 옵션 세부 설정 (lexical, semantic)
  - 제외 이유: transcription 옵션 자체는 테스트하지만, 세부 옵션까지는 범위에서 제외
- **include_user_metadata**: 사용자 메타데이터 포함 옵션
  - 제외 이유: 사용자 메타데이터가 설정된 인덱스가 필요하며, 기본 테스트 범위에서 제외

### Deprecated 파라미터
- **adjust_confidence_level**: deprecated 파라미터 (Marengo 3.0에서 제거됨)
  - 제외 이유: 더 이상 사용되지 않는 파라미터
- **threshold**: deprecated 파라미터 (Marengo 3.0에서 제거됨)
  - 제외 이유: 더 이상 사용되지 않는 파라미터

## 사용된 SDK 버전

- **twelvelabs**: >=1.1.0 (requirements.txt에 명시)
- **pytest**: >=7.0.0 (requirements.txt에 명시)

실제 설치된 버전을 확인하려면:

```bash
pip list | grep -E "twelvelabs|pytest"
```

## 가정 및 제한사항

### 가정 (Assumptions)

1. **인덱스 전제조건**: 테스트는 이미 생성되고 비디오가 업로드된 인덱스가 필요합니다. 인덱스 생성 및 비디오 업로드는 이 테스트 스위트의 범위에 포함되지 않습니다.

2. **Marengo 버전**: 
   - 인덱스가 사용하는 Marengo 버전에 따라 일부 기능(예: transcription 옵션)이 지원되지 않을 수 있습니다.
   - 이 경우 해당 테스트는 자동으로 스킵됩니다.
   - Marengo 2.7과 3.0 모두에 대해 테스트를 수행하도록 설계되었습니다.

3. **결과 의존성**: 
   - 일부 테스트는 인덱스의 실제 비디오 내용에 따라 결과가 달라질 수 있습니다.
   - 빈 결과가 반환되는 경우도 정상입니다.
   - 테스트는 결과의 존재 여부보다는 응답 구조와 데이터 타입의 유효성을 검증합니다.

4. **문서 기준 우선**: 
   - `reference/search.md`에 명시된 문서 기준이 우선됩니다.
   - 실제 API 응답이 문서 기준과 다를 경우, 테스트는 SKIP 처리되며 명확한 메시지를 제공합니다.

### 제한사항 (Limitations)

1. **실제 API 호출**: 이 테스트는 실제 Twelve Labs API를 호출합니다. 따라서:
   - 인터넷 연결이 필요합니다
   - API 키가 유효해야 합니다
   - 인덱스에 비디오가 있어야 검색 결과를 얻을 수 있습니다

2. **테스트 실행 시간**: 실제 API 호출을 수행하므로 테스트 실행에 시간이 걸릴 수 있습니다.

3. **API 할당량**: 테스트 실행 시 API 할당량이 소모됩니다.

4. **환경 의존성**: 테스트 결과는 인덱스의 실제 내용에 따라 달라질 수 있습니다.

## 문제 해결

### 테스트가 실패하는 경우

1. **API 키 확인**: `TL_API_KEY` 환경 변수 또는 `config.env` 파일의 API 키가 유효한지 확인하세요.

2. **인덱스 ID 확인**: `TL_INDEX_MARENGO_27` 또는 `TL_INDEX_MARENGO_30` 환경 변수 또는 `config.env` 파일의 인덱스 ID가 올바른지 확인하세요.

3. **인덱스 상태 확인**: 인덱스에 비디오가 업로드되어 있고 인덱싱이 완료되었는지 확인하세요.

4. **네트워크 연결 확인**: 인터넷 연결이 안정적인지 확인하세요.

5. **Marengo 버전 확인**: 특정 기능(예: transcription)이 지원되지 않는 경우, 해당 테스트는 자동으로 스킵됩니다.

### 특정 테스트만 실행하고 싶은 경우

특정 기능만 테스트하려면 pytest의 필터링 기능을 사용하세요:

```bash
# 특정 파일의 모든 테스트 실행
pytest tests/test_search_query_text.py

# 특정 클래스만 실행
pytest tests/test_search_query_text.py::TestSearchQueryText

# 특정 테스트만 실행
pytest tests/test_search_query_text.py::TestSearchQueryText::test_search_with_text_query

# 키워드로 필터링
pytest tests/ -k "sort_option"

# Marengo 버전별 필터링
pytest tests/ -m marengo27  # Marengo 2.7만
pytest tests/ -m marengo30  # Marengo 3.0만
```

## 라이선스

이 프로젝트는 Twelve Labs SDK 테스트 목적으로 작성되었습니다.
