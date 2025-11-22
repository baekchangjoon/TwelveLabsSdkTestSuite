# Twelve Labs SDK Search Method Test Suite

This project is a comprehensive automated test suite for the `search.query()` method of the Twelve Labs Python SDK.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Test Structure](#test-structure)
- [Tested Parameters](#tested-parameters)
- [Untested Parameters](#untested-parameters)
- [SDK Versions Used](#sdk-versions-used)
- [Assumptions and Limitations](#assumptions-and-limitations)
- [Troubleshooting](#troubleshooting)

## Overview

This test suite was created to validate the Search functionality of the Twelve Labs SDK. It provides comprehensive tests including various search scenarios, parameter combinations, edge cases, and error handling.

- 🔗 **GitHub Repository**: [https://github.com/baekchangjoon/TwelveLabsSdkTestSuite](https://github.com/baekchangjoon/TwelveLabsSdkTestSuite) - You can view the entire project here.
- 📊 **Test Results Dashboard**: [https://baekchangjoon.github.io/TwelveLabsSdkTestSuite/](https://baekchangjoon.github.io/TwelveLabsSdkTestSuite/) - You can view test results here.

## Requirements

- Python 3.8 or higher (Python 3.7 is not supported)
  - According to [PyPI's twelvelabs package metadata](https://pypi.org/project/twelvelabs/), `twelvelabs>=1.0.0` requires `requires_python: "<4.0,>=3.8"`.
  - Therefore, Python 3.7 cannot use the latest SDK (`twelvelabs>=1.1.0`), and Python 3.8 or higher is required.
- Twelve Labs API key
- Twelve Labs Index ID (index with uploaded videos)
  - Marengo 2.7 index
  - Marengo 3.0 index

## Installation

```bash
git clone <repository_url>
cd TwelveLabsSdkTestSuite
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

### Method 1: Using config.env file (Recommended)

```bash
cp config.env.example config.env
# Open config.env file and enter actual values
```

```bash
TL_API_KEY=your_api_key_here
TL_INDEX_MARENGO_27=your_marengo_27_index_id_here
TL_INDEX_MARENGO_30=your_marengo_30_index_id_here
```

**Note**: You can set only one of `TL_INDEX_MARENGO_27` and `TL_INDEX_MARENGO_30`, and tests for unset indexes will be automatically skipped.

### Method 2: Using environment variables

```bash
export TL_API_KEY="your_api_key_here"
export TL_INDEX_MARENGO_27="your_marengo_27_index_id_here"
export TL_INDEX_MARENGO_30="your_marengo_30_index_id_here"
```

## Running Tests

### Run all tests

```bash
pytest tests/
```

### Check test coverage

```bash
pytest tests/ --cov=tests --cov-report=html
```

## CI/CD and Test Results

### Test Results Dashboard

Test results automatically executed through GitHub Actions can be viewed in the following dashboard:

🔗 **Test Results Dashboard**: [https://baekchangjoon.github.io/TwelveLabsSdkTestSuite/](https://baekchangjoon.github.io/TwelveLabsSdkTestSuite/)

The dashboard provides the following information:
- 📊 **Coverage Report**: Code coverage metrics and detailed information
- 🧪 **Matrix Test Summary**: Test results by Python version (Pass/Fail/Skip/Error)
- 📝 **Detailed Test Reports**: HTML reports for each Python version

![CI Dashboard](https://baekchangjoon.github.io/TwelveLabsSdkTestSuite/)

### CI/CD Test Environment Limitations

#### Python Version Limitations
- **Python 3.7**: Excluded from testing.
  - According to [PyPI's twelvelabs package metadata](https://pypi.org/project/twelvelabs/), `twelvelabs>=1.0.0` requires `requires_python: "<4.0,>=3.8"`.
  - Therefore, Python 3.7 cannot use the latest SDK (`twelvelabs>=1.1.0`) and has been excluded from testing.
  - Currently, tests run only on Python 3.8, 3.9, 3.10, 3.11, and 3.12.

#### Operating System Limitations
- **Windows and macOS**: When running tests simultaneously on multiple OSes in CI/CD environments, `too_many_requests` errors occur due to API request limits.
  - Currently, tests run only on `ubuntu-24.04`.

### Skipped Test Items

#### Skipped Test Items

**search_option_combination_not_supported error**
- The test was skipped because we could not find a way to trigger the `search_option_combination_not_supported` error.
- Although this error code is documented, we could not reproduce this error with specific option combinations in the actual test environment.
- Related test: `test_search_with_unsupported_option_combination` in `tests/test_search_error_handling.py`

**Expired page token test**
- The test is skipped when there is no next page because it is difficult to generate an actually expired page token.
- Related test: `test_search_with_expired_page_token` in `tests/test_search_error_handling.py`

**Image file search with audio option only**
- The test is skipped because `query_media_type='image'` requires `search_options` to contain `'visual'`.
- This constraint is not explicitly documented in `reference/search.md`.
- Related test: `test_search_with_image_file_audio_only` in `tests/test_search_query_media_file.py`

## Test Coverage

This test suite provides comprehensive validation of the `search.query()` method and covers the following 4 main areas according to the requirements in subject.md:

### 1. Successful operations with valid parameters and expected behavior

#### TestSearchQueryText (5 tests)
- ✅ **Basic text query search**: Validates basic search behavior using `query_text` and `search_options`
- ✅ **Various query texts**: Validates common usage patterns with different queries
- ✅ **Empty query text**: Validates error handling for empty strings
- ✅ **Very long query text**: Edge case test for token limits
  - Marengo 2.7: Maximum 77 tokens
  - Marengo 3.0: Maximum 500 tokens
- ✅ **No query text or media**: Error handling for missing required parameters
#### TestSearchOptions (5 tests)
- ✅ **visual and audio combination**: Validates the most common usage pattern
- ✅ **visual option only**: Validates single option usage pattern
- ✅ **audio option only**: Validates single option usage pattern
- ✅ **transcription option**: Tests transcription option supported in Marengo 3.0
  - Marengo 2.7: Confirms `search_option_not_supported` error
  - Marengo 3.0: Confirms normal operation
- ✅ **All options combination**: Tests combination using `visual`, `audio`, and `transcription`

#### TestSearchSortOption (5 tests)
- ✅ **sort_option='score'**: Validates sorting search results by relevance ranking
  - Marengo 3.0: Ascending order by rank field (1 = most relevant)
  - Marengo 2.7: Descending order by score field (higher score = more relevant)
- ✅ **sort_option='score' with group_by='video' combination**: Validates sorting when grouping by video
  - Videos are sorted by highest relevance ranking (lowest number)
  - Clips within each video are sorted in ascending order by relevance ranking (Marengo 3.0) or descending order by score (Marengo 2.7)
- ✅ **sort_option='clip_count' with group_by='video' combination**: Validates sorting by number of clips
  - Videos are sorted in descending order by number of matching clips
  - Clips within each video are sorted in ascending order by relevance ranking (Marengo 3.0) or descending order by score (Marengo 2.7)
- ✅ **sort_option='score' with filter combination**: Validates sorting with filter
- ✅ **sort_option='clip_count' with filter combination**: Validates clip count sorting with filter

#### TestSearchGroupBy (10 tests)
- ✅ **group_by='video'**: Validates grouping and returning by video unit
  - Confirms existence of id and clips fields
- ✅ **group_by='clip'**: Validates default behavior of returning by clip unit
  - Confirms individual clip information (video_id, start, end)
- ✅ **group_by='video' with operator='and' combination**: Used with logical AND operator
- ✅ **group_by='video' with operator='or' combination**: Used with logical OR operator
- ✅ **group_by='clip' with operator='and' combination**: Used with logical AND operator
- ✅ **group_by='clip' with operator='or' combination**: Used with logical OR operator
- ✅ **group_by='video' with page_limit combination**: Used with page limit
- ✅ **group_by='clip' with page_limit combination**: Used with page limit
- ✅ **group_by='video' with filter combination**: Used with filter
- ✅ **group_by='clip' with filter combination**: Used with filter

#### TestSearchOperator (2 tests)
- ✅ **operator='or'**: Validates combining search options with logical OR operator (default)
- ✅ **operator='and'**: Validates combining search options with logical AND operator

#### TestSearchPageLimit (6 tests)
- ✅ **page_limit**: Validates limiting number of results per page (typical value: 5)
- ✅ **page_limit maximum**: Tests maximum value (50)
- ✅ **page_limit minimum**: Edge case test for minimum value (1)
- ✅ **page_limit various values**: Tests with values 1, 5, 10, 25, 50
- ✅ **Pagination**: Validates multi-page result processing and `next_page()` method behavior (includes `has_next` check)

#### TestSearchFilter (4 tests)
- ✅ **filter basic**: Validates metadata filtering functionality using JSON strings
- ✅ **filter various formats**: Tests various JSON filter formats (single field, multiple field combinations)
- ✅ **filter with operator='and' combination**: Used with logical AND operator
- ✅ **filter with operator='or' combination**: Used with logical OR operator

#### TestSearchQueryMediaFile (12 tests, 1 skipped)
- ✅ **Basic image file search**: Validates basic search behavior using `query_media_file` with `query_media_type='image'`
- ✅ **Image file search with visual option only**: Validates single option usage pattern
- ⏭️ **Image file search with audio option only**: Skipped (requires visual in search_options, constraint not documented)
- ✅ **Image file search with group_by='video'**: Validates grouping when using image file query
- ✅ **Image file search with page_limit**: Validates pagination with image file query
- ✅ **Image file search with filter**: Validates filtering with image file query
- ✅ **Image file search with sort_option**: Validates sorting with image file query
- ✅ **Image file search with operator**: Validates logical operator with image file query
- ✅ **Composed search with image file and text**: Validates composed image+text search (Marengo 3.0 only)
- ✅ **Error handling for missing query_media_type**: Validates error when query_media_file is provided without query_media_type
- ✅ **Error handling for missing query_media_file or query_text**: Validates error when query_media_type is provided without query
- ✅ **Error handling for invalid image file**: Validates error when invalid file format is provided

**Note**: Uses `resources/rhino.png` as test image file.
### 2. Various edge cases that may affect SDK method stability and reliability

**Edge cases included in TestSearchQueryText**:
- ✅ **Empty query text**: Validates handling when empty string ("") is passed as query
  - Confirms `parameter_not_provided` or `parameter_invalid` error
- ✅ **Very long query text**: Tests long queries near token limits
  - Marengo 3.0: Supports up to 500 tokens
  - Marengo 2.7: Maximum 77 token limit, `parameter_invalid` error when exceeded
- ✅ **No query text or media**: Validates handling when all required parameters are missing
  - Confirms `parameter_not_provided` error

**Edge cases included in TestSearchPageLimit**:
- ✅ **Minimum page_limit**: Edge test for minimum value by setting page_limit=1

### 3. Error handling and boundary conditions to ensure proper exception management

**TestSearchQueryMediaFile** (1 test skipped):
- ⏭️ **Image file search with audio option only**: Skipped because `query_media_type='image'` requires `search_options` to contain `'visual'`. This constraint is not explicitly documented in `reference/search.md`.

**TestSearchErrorHandling** (11 tests, 1 skipped):
- ✅ **Invalid index_id**: Confirms ApiError when searching with non-existent index ID
- ✅ **Empty search_options**: Exception handling when search_options, a required parameter, is an empty list
- ✅ **Invalid search_option**: Exception handling when unsupported option ("invalid_option") is passed
- ✅ **Invalid sort_option**: Exception handling when unsupported sort option is passed
- ✅ **Invalid group_by**: Exception handling when unsupported grouping option is passed
- ✅ **Invalid operator**: Exception handling when unsupported logical operator is passed
- ✅ **Invalid page_limit (negative)**: Exception handling when negative value is passed
- ✅ **page_limit exceeds maximum**: Validates handling when value exceeding maximum (50) is passed
- ✅ **Invalid filter syntax**: Confirms ApiError when filter with invalid JSON format is passed
- ⏭️ **Unsupported option combination**: Skipped because we could not find a way to trigger `search_option_combination_not_supported` error
- ⏭️ **Expired page token**: Skipped when there is no next page because it is difficult to generate an actually expired token

### 4. Various usage patterns and potential failure scenarios that real users may encounter

**TestSearchResponseValidation** (4 tests):
- ✅ **Response structure validation**: Validates existence of required fields and data types in search results
  - Confirms video_id (string), start/end (number) types
- ✅ **rank field validation**: Validates validity of rank field returned in Marengo 3.0
  - Confirms integer type and values >= 1
- ✅ **thumbnail_url format validation**: Confirms thumbnail URL is in correct HTTP URL format
- ✅ **Time range validity**: Validates logical validity of start and end times
  - Confirms start >= 0, end > start

## Test Structure

```
TwelveLabsSdkTestSuite/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # pytest configuration and common fixtures, utility functions
│   ├── test_search_query_text.py        # query_text parameter tests
│   ├── test_search_options.py           # search_options parameter tests
│   ├── test_search_sort_option.py       # sort_option parameter tests
│   ├── test_search_group_by.py          # group_by parameter tests
│   ├── test_search_operator.py          # operator parameter tests
│   ├── test_search_page_limit.py        # page_limit parameter tests
│   ├── test_search_filter.py            # filter parameter tests
│   ├── test_search_query_media_file.py  # query_media_file parameter tests
│   ├── test_search_error_handling.py    # error handling tests
│   └── test_search_response_validation.py # response validation tests
├── reference/
│   └── search.md                         # SDK Search method specification (reference document)
├── config.env.example                    # Environment variable configuration example
├── config.env                            # Actual environment variable configuration (not included in git)
├── playground.py                         # API key and index ID configuration (optional)
├── requirements.txt                      # Project dependencies
├── pytest.ini                            # pytest configuration (includes -s option for error code output)
├── README.md                             # This file
├── TESTING_APPROACH.md                   # Test approach and assumptions document
└── subject.md                            # Assignment requirements
```

## Tested Parameters

According to the requirements in subject.md, the following major parameters are selected and tested from the extensive parameters of the `search.query()` method:

### 1. query_text (Text Query) - Required Parameter

**Test Coverage**: 
- ✅ Returns search results with normal text query
- ✅ Supports common usage patterns with various query texts
- ✅ Edge condition handling for empty strings (`parameter_not_provided` or `parameter_invalid`)
- ✅ Edge condition handling for very long strings (token limits)
  - Marengo 2.7: Maximum 77 tokens
  - Marengo 3.0: Maximum 500 tokens

**Test File**: `test_search_query_text.py` (5 tests)

### 2. search_options (Search Options) - Required Parameter

**Test Coverage**: 
- ✅ Single option usage (visual, audio)
- ✅ visual + audio combination (most common usage pattern)
- ✅ visual + audio + transcription combination (Marengo 3.0)
- ✅ Error handling for empty list
- ✅ Error handling for invalid options

**Test File**: `test_search_options.py` (5 tests), `test_search_error_handling.py` (2 tests)

### 3. sort_option (Sort Option)

**Test Coverage**: 
- ✅ `score`: Sorts search results by relevance ranking
  - Marengo 3.0: Ascending order by rank field (1 = most relevant)
  - Marengo 2.7: Descending order by score field (higher score = more relevant)
- ✅ `clip_count`: Sorts videos by number of matching clips in descending order (requires group_by='video')
  - Documentation: "Sorts videos by the number of matching clips in descending order"
  - Clips within each video are sorted in ascending order by relevance ranking (Marengo 3.0) or descending order by score (Marengo 2.7)
- ✅ Combination tests with group_by='video'
- ✅ Combination tests with filter
- ✅ Error handling for invalid options

**Test File**: `test_search_sort_option.py` (5 tests), `test_search_error_handling.py` (1 test)

### 4. group_by (Grouping Option)

**Test Coverage**: 
- ✅ `video`: Groups and returns by video unit
  - Confirms existence of id and clips fields
- ✅ `clip`: Returns by clip unit (default)
  - Confirms individual clip information (video_id, start, end)
- ✅ Combination tests with operator
- ✅ Combination tests with page_limit
- ✅ Combination tests with filter
- ✅ Error handling for invalid options

**Test File**: `test_search_group_by.py` (10 tests), `test_search_error_handling.py` (1 test)

### 5. operator (Logical Operator)

**Test Coverage**: 
- ✅ `or`: Combines search options with logical OR operator (default)
- ✅ `and`: Combines search options with logical AND operator
- ✅ Combination tests with group_by
- ✅ Combination tests with filter
- ✅ Error handling for invalid operators

**Test File**: `test_search_operator.py` (2 tests), `test_search_error_handling.py` (1 test)

### 6. page_limit (Page Size Limit)

**Test Coverage**: 
- ✅ Typical value (5)
- ✅ Maximum value (50)
- ✅ Minimum value (1) - edge case
- ✅ Various values (1, 5, 10, 25, 50)
- ✅ Pagination functionality (validates `has_next` check and `next_page()` method behavior)
- ✅ Error handling for negative values
- ✅ Exceeds maximum (100) - edge case
- ✅ Combination tests with group_by

**Test File**: `test_search_page_limit.py` (6 tests), `test_search_error_handling.py` (2 tests)

### 7. filter (Metadata Filter)

**Test Coverage**: 
- ✅ Valid JSON filter
- ✅ Various JSON filter formats (single field, multiple field combinations)
- ✅ Combination tests with operator (and, or)
- ✅ Combination tests with group_by
- ✅ Combination tests with sort_option
- ✅ Error handling for invalid JSON syntax

**Test File**: `test_search_filter.py` (4 tests), `test_search_error_handling.py` (1 test)

### 8. query_media_file (Local Media File Query)

**Test Coverage**: 
- ✅ Basic image file search with visual and audio options
- ✅ Image file search with visual option only
- ✅ Image file search with various parameter combinations (group_by, page_limit, filter, sort_option, operator)
- ✅ Composed search with image file and text query (Marengo 3.0 only)
- ✅ Error handling for missing query_media_type
- ✅ Error handling for missing query_media_file or query_text when query_media_type is provided
- ✅ Error handling for invalid image file format
- ⏭️ Image file search with audio option only (skipped: requires visual in search_options, not documented)

**Test File**: `test_search_query_media_file.py` (12 tests, 1 skipped)

**Note**: Uses `resources/rhino.png` as test image file.

## Untested Parameters

The following parameters are excluded from the test scope:

### Media Query Related Parameters
- **query_media_url**: Media URL query
  - Exclusion reason: Requires publicly accessible test image URLs, and it is difficult to secure URLs that can be used reliably in test environments
- **query_media_type**: Media type (related to image query tests)
  - Note: `query_media_file` is now tested, but `query_media_url` remains excluded

### Advanced Option Parameters
- **transcription_options**: Transcription option detailed settings (lexical, semantic)
  - Exclusion reason: The transcription option itself is tested, but detailed options are excluded from scope
- **include_user_metadata**: User metadata inclusion option
  - Exclusion reason: Requires an index with user metadata configured, excluded from basic test scope

### Deprecated Parameters
- **adjust_confidence_level**: Deprecated parameter (removed in Marengo 3.0)
  - Exclusion reason: No longer used parameter
- **threshold**: Deprecated parameter (removed in Marengo 3.0)
  - Exclusion reason: No longer used parameter

## SDK Versions Used

- **twelvelabs**: >=1.1.0 (specified in requirements.txt)
- **pytest**: >=7.0.0 (specified in requirements.txt)
To check the actually installed versions:

```bash
pip list | grep -E "twelvelabs|pytest"
```

## Assumptions and Limitations

### Assumptions

1. **Index Prerequisites**: Tests require indexes that are already created and have videos uploaded. Index creation and video upload are not included in the scope of this test suite.

2. **Marengo Version**: 
   - Depending on the Marengo version used by the index, some features (e.g., transcription option) may not be supported.
   - In such cases, the corresponding tests are automatically skipped.
   - Tests are designed to run for both Marengo 2.7 and 3.0.

3. **Result Dependency**: 
   - Some tests may produce different results depending on the actual video content in the index.
   - Empty results are also considered normal.
   - Tests validate response structure and data type validity rather than result existence.

4. **Documentation-First**: 
   - The documentation criteria specified in `reference/search.md` take precedence.
   - When actual API responses differ from documentation criteria, tests are SKIPPED with clear messages.

### Limitations

1. **Actual API Calls**: These tests call the actual Twelve Labs API. Therefore:
   - Internet connection is required
   - API key must be valid
   - Index must have videos to obtain search results

2. **Test Execution Time**: Since actual API calls are made, test execution may take time.

3. **API Quota**: API quota is consumed when running tests.

4. **Environment Dependency**: Test results may vary depending on the actual content of the index.

## Troubleshooting

### When tests fail

1. **Check API key**: Verify that the `TL_API_KEY` environment variable or API key in the `config.env` file is valid.

2. **Check Index ID**: Verify that the `TL_INDEX_MARENGO_27` or `TL_INDEX_MARENGO_30` environment variable or index ID in the `config.env` file is correct.

3. **Check index status**: Verify that videos are uploaded to the index and indexing is complete.

4. **Check network connection**: Verify that internet connection is stable.

5. **Check Marengo version**: If certain features (e.g., transcription) are not supported, the corresponding tests are automatically skipped.

### Running specific tests only

To test specific features only, use pytest's filtering functionality:

```bash
# Run all tests in a specific file
pytest tests/test_search_query_text.py

# Run only a specific class
pytest tests/test_search_query_text.py::TestSearchQueryText

# Run only a specific test
pytest tests/test_search_query_text.py::TestSearchQueryText::test_search_with_text_query

# Filter by keyword
pytest tests/ -k "sort_option"

# Filter by Marengo version
pytest tests/ -m marengo27  # Marengo 2.7 only
pytest tests/ -m marengo30  # Marengo 3.0 only
```

## License

This project was created for testing purposes of the Twelve Labs SDK.
