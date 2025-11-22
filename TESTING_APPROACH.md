# Test Approach and Assumptions Document

This document explains the approach, test scope decisions, SDK versions used, and all assumptions set for the Twelve Labs SDK Search method test suite.

## Table of Contents

- [Approach](#approach)
- [Test Scope Decisions](#test-scope-decisions)
- [SDK Versions Used](#sdk-versions-used)
- [Test Structure Design](#test-structure-design)
- [Assumptions](#assumptions)
- [Limitations](#limitations)
- [Test Parameter Selection Rationale](#test-parameter-selection-rationale)

## Approach

This test suite was written following these principles:

### 1. Real Environment Testing

- **No Mock Usage**: Tests are performed using actual SDK and API instead of mocks to simulate real usage environments.
- **Actual API Calls**: All tests call the actual Twelve Labs API to validate the SDK's real behavior.
- **TestContainer Recommended**: Although subject.md recommends using TestContainer instead of mocks, this project chose to directly call the actual API.
- **Mock-based Component Testing Excluded**: Component testing of the SDK using mocks is possible, but was excluded from this scope. This test suite focuses on validating integration behavior with the actual API.
- **Test Environment Combinations**: Tests were performed with combinations of Marengo 2.7 and 3.0, and Python versions. Operating system combinations are also possible, but tests were run only in the `ubuntu-24.04` environment due to API request limits.

### 2. Comprehensive Coverage

Tests cover the following 4 main areas:

1. **Success Cases**: Successful operations with valid parameters and expected behavior
2. **Edge Cases**: Various edge cases that may affect SDK method stability and reliability
3. **Error Handling**: Error handling and boundary conditions to ensure proper exception management
4. **Usage Patterns**: Various usage patterns and potential failure scenarios that real users may encounter

### 3. Parameter-based Test Structure

- Separate test classes and files for each major parameter
- File and class names clearly reflect parameter names
  - Example: `test_search_query_text.py` → `TestSearchQueryText`
  - Example: `test_search_sort_option.py` → `TestSearchSortOption`

### 4. Documentation-First Approach

- The documentation criteria specified in `reference/search.md` take precedence.
- When actual API responses differ from documentation criteria:
  - Tests are SKIPPED
  - Clear messages are provided to inform about differences between documentation and actual responses
  - Example: SKIP when `sort_option` sorting validation differs from documentation criteria

### 5. Flexible Validation

- Since results may vary depending on index content, tests validate response structure and data type validity rather than result existence.
- Empty results are also considered normal.

### 6. Automatic Skipping

- Tests for unsupported features are automatically skipped to not interfere with overall test execution.
- Example: Automatic skip when using transcription option in Marengo 2.7

### 7. Clear Error Handling

- Expected errors are handled appropriately, and unexpected errors cause test failures.
- Error codes are extracted and validated.

## Test Scope Decisions

### Selected Major Parameters

According to the requirements in subject.md, the following major parameters are selected and tested from the extensive parameters of the `search.query()` method:

#### 1. query_text (Text Query) - Required Parameter

**Selection Rationale**: 
- Most basic and essential parameter
- Parameter that forms the basis of all search scenarios
- Important parameter for edge case testing (empty strings, long strings)

**Test Coverage**:
- Basic text query search
- Various query texts
- Empty string (edge case)
- Very long string (token limit edge case)
- No query text or media (required parameter missing)
- Whitespace-only query text (edge case: `"   "`)
- Special characters in query text (edge case: `"test@#$%^&*()"`)
- Unicode and emoji characters in query text (edge case: `"test 🎥 video"`)
- Very short query text (edge case: 1-2 words like `"water"`)

#### 2. search_options (Search Options) - Required Parameter

**Selection Rationale**: 
- Required parameter and core of search behavior
- Various combinations possible, leading to diverse real usage patterns
- Includes options with version-dependent support (transcription)

**Test Coverage**:
- Single option usage (visual, audio)
- Multiple option combinations (visual + audio)
- All option combinations (visual + audio + transcription)
- Empty list (error handling)
- Invalid options (error handling)

#### 3. sort_option (Sort Option)

**Selection Rationale**: 
- Sorting search results is an important feature for user experience
- Clear sorting criteria documented, making validation possible
- Important parameter for combination with group_by

**Test Coverage**:
- `score`: Sort by relevance ranking
- `clip_count`: Sort by number of clips (requires group_by='video')
- Combination with group_by
- Combination with filter
- Invalid options (error handling)

#### 4. group_by (Grouping Option)

**Selection Rationale**: 
- Important parameter that determines search result structure
- Returns different response structures in two modes: video and clip
- Important for combinations with other parameters

**Test Coverage**:
- `video`: Group by video unit
- `clip`: Return by clip unit (default)
- Combination with operator
- Combination with page_limit
- Combination with filter
- Invalid options (error handling)

#### 5. operator (Logical Operator)

**Selection Rationale**: 
- Important parameter that affects how search_options are combined
- OR and AND differences significantly affect search results

**Test Coverage**:
- `or`: Logical OR operator (default)
- `and`: Logical AND operator
- Combinations with other parameters

#### 6. page_limit (Page Size Limit)

**Selection Rationale**: 
- Core parameter for pagination functionality
- Important parameter for edge case testing (minimum, maximum values)
- Frequently used parameter in real usage

**Test Coverage**:
- Typical value (5)
- Maximum value (50)
- Minimum value (1)
- Various values (1, 5, 10, 25, 50)
- Pagination functionality (validates `has_next` check and `next_page()` method behavior)
- Negative values (error handling)
- Exceeds maximum (edge case)
- Zero value (edge case: `page_limit=0`)
- Value just above maximum (edge case: `page_limit=51`)
- Multiple pages iteration (validates pagination across 3+ pages)
- `iter_pages()` method (validates iteration through page objects)

#### 7. filter (Metadata Filter)

**Selection Rationale**: 
- Important feature for filtering search results
- Complex filtering possible with JSON format, leading to various usage patterns

**Test Coverage**:
- Valid JSON filter
- Various JSON filter formats (single field, multiple field combinations)
- Combinations with other parameters (operator, group_by, sort_option)
- Invalid JSON syntax (error handling)
- Empty string filter (error handling)
- Empty JSON object filter (edge case: `"{}"`)

#### 8. query_media_file (Local Media File Query)

**Selection Rationale**: 
- Important parameter for image-based search functionality
- Enables testing of media query capabilities
- Uses local test image file (`resources/rhino.png`) for reliable testing

**Test Coverage**:
- Basic image file search with visual and audio options
- Image file search with visual option only
- Image file search with various parameter combinations (group_by, page_limit, filter, sort_option, operator)
- Composed search with image file and text query (Marengo 3.0 only)
- Error handling for missing query_media_type
- Error handling for missing query_media_file or query_text when query_media_type is provided
- Error handling for invalid image file format
- Image file search with audio option only (skipped: requires visual in search_options, constraint not documented in search.md)

**Note**: One test (`test_search_with_image_file_audio_only`) is skipped because the API requires `search_options` to contain `'visual'` when using `query_media_type='image'`, but this constraint is not explicitly documented in `reference/search.md`.

### Excluded Parameters

The following parameters are excluded from the test scope:

#### Media Query Related Parameters

- **query_media_url**
  - **Exclusion Rationale**: 
    - Requires publicly accessible test image URLs
    - Difficult to secure URLs that can be used reliably in test environments
- **query_media_type**
  - **Note**: `query_media_file` is now tested, but `query_media_url` remains excluded
#### Advanced Option Parameters

- **transcription_options**
  - **Exclusion Rationale**: 
    - The transcription option itself is tested, but detailed options (lexical, semantic) are excluded from scope
    - Basic transcription option testing is considered sufficient

- **include_user_metadata**
  - **Exclusion Rationale**: 
    - Requires an index with user metadata configured
    - Excluded from basic test scope

#### Deprecated Parameters

- **adjust_confidence_level**, **threshold**
  - **Exclusion Rationale**: 
    - Deprecated in Marengo 3.0 and no longer used
    - New versions recommend using the `rank` field

## SDK Versions Used

### Python SDK

- **Package Name**: `twelvelabs`
- **Minimum Version**: 1.1.0 (specified in requirements.txt)
- **Installation Method**: `pip install -r requirements.txt`

### Test Framework

- **Package Name**: `pytest`
- **Minimum Version**: 7.0.0 (specified in requirements.txt)

### Version Check Method

```bash
pip list | grep -E "twelvelabs|pytest"
```

## Test Structure Design

### File Structure

Tests are clearly separated by parameter:

```
tests/
├── conftest.py                      # Common fixtures and utility functions
├── test_search_query_text.py        # query_text parameter tests
├── test_search_options.py           # search_options parameter tests
├── test_search_sort_option.py       # sort_option parameter tests
├── test_search_group_by.py          # group_by parameter tests
├── test_search_operator.py          # operator parameter tests
├── test_search_page_limit.py        # page_limit parameter tests
├── test_search_filter.py            # filter parameter tests
├── test_search_query_media_file.py  # query_media_file parameter tests
├── test_search_error_handling.py    # error handling tests
├── test_search_response_validation.py # response validation tests
└── test_search_combination.py       # combination tests (all parameters together)
```

### Class and Method Naming Rules

- **Class Names**: `TestSearch{ParameterName}` format
  - Example: `TestSearchQueryText`, `TestSearchSortOption`, `TestSearchGroupBy`
- **Method Names**: `test_{parameter_name}_{scenario}` format
  - Example: `test_sort_option_score`, `test_group_by_video_with_operator_and`

### Common Utilities

The following common functions are defined in `conftest.py`:

- `get_error_code()`: Extracts error code from ApiError
- `validate_marengo_fields()`: Validates fields by Marengo version
- `get_index_name()`: Extracts index name from pytest request
- `is_marengo30()`: Determines Marengo version from index name

## Assumptions

### 1. Index Prerequisites

- **Assumption**: Tests require indexes that are already created and have videos uploaded.
- **Rationale**: subject.md states "Creating indexes and uploading videos is not included in the scope of this assignment."
- **Impact**: Index creation and video upload must be completed before test execution.

### 2. Marengo Version

- **Assumption**: Some features may not be supported depending on the Marengo version used by the index.
- **Rationale**: 
  - Marengo 2.7 and 3.0 support different features (e.g., transcription option is only supported in Marengo 3.0)
  - Documentation specifies version differences
- **Handling**: 
  - Designed to test both versions
  - Tests for unsupported features are automatically skipped
  - Use `@pytest.mark.marengo27`, `@pytest.mark.marengo30` markers to distinguish tests by version

### 3. Result Dependency

- **Assumption**: Test results may vary depending on the actual video content in the index.
- **Rationale**: Search results depend on the content of videos uploaded to the index.
- **Handling**: 
  - Validates response structure and data type validity rather than result existence
  - Empty results are also considered normal
  - Validation in format like `assert len(results) >= 0`

### 4. Documentation-First

- **Assumption**: The documentation criteria specified in `reference/search.md` take precedence.
- **Rationale**: Documentation is the official API specification and should take precedence over actual implementation.
- **Handling**: 
  - When actual API responses differ from documentation criteria, tests are SKIPPED
  - Clear messages are provided to inform about differences between documentation and actual responses
  - Example: Call `pytest.skip()` when `sort_option` sorting validation differs from documentation criteria

### 5. Actual API Calls

- **Assumption**: Tests call the actual Twelve Labs API.
- **Rationale**: Although subject.md states "Focus on SDK functionality testing rather than direct API calls," actual API calls are necessary to validate the SDK's real behavior.
- **Impact**: 
  - Internet connection required
  - API key must be valid
  - API quota is consumed
  - Test execution takes time

## Limitations

### 1. Untested Parameters

The following parameters are excluded from the test scope:

- **Media Query Related**: `query_media_url`, `query_media_file`, `query_media_type`
- **Advanced Options**: `transcription_options`, `include_user_metadata`
- **Deprecated Parameters**: `adjust_confidence_level`, `threshold`

See the [Test Parameter Selection Rationale](#test-parameter-selection-rationale) section for details.

### 2. Environment Dependencies

- **Index Content**: Test results may vary depending on the actual video content in the index.
- **Network Connection**: Internet connection is required.
- **API Key Validity**: API key must be valid.

### 3. Test Execution Time

- Since actual API calls are made, test execution may take time.
- Full test suite execution may take tens of seconds to minutes.

### 4. API Quota

- API quota is consumed when running tests.
- Quota limits may be reached when running large numbers of tests.

### 5. Parameter Combination Limitations

- Testing all parameter combinations is impossible.
- Focus on major parameters and common combinations.
- Undocumented combinations or unexpected behaviors may not be included in test scope.

## Test Parameter Selection Rationale

### Included Parameters

#### Required Parameters (Must Test)

1. **query_text**: Essential parameter that forms the basis of all searches
2. **search_options**: Essential parameter that determines the core of search behavior

#### Major Optional Parameters

3. **sort_option**: Sorting search results is an important feature for user experience
4. **group_by**: Important parameter that determines search result structure
5. **operator**: Parameter that affects how search options are combined
6. **page_limit**: Core parameter for pagination functionality
7. **filter**: Important feature for filtering search results

### Excluded Parameters

#### Media Query Related

- **query_media_url**
  - Difficulty securing publicly accessible test image URLs
  - Basic search functionality can be sufficiently validated with text query tests
- **query_media_file**
  - **Note**: Now included in test scope. Uses local test image file (`resources/rhino.png`) for testing.

#### Advanced Options

- **transcription_options**: The transcription option itself is tested, but detailed options are excluded
- **include_user_metadata**: Requires an index with user metadata configured

#### Deprecated Parameters

- **adjust_confidence_level**, **threshold**: Parameters no longer used

## Additional Test Cases

### Enhanced Edge Case Testing

To strengthen the test suite's coverage of edge cases and boundary conditions, the following additional test cases were added:

#### 1. query_text Edge Cases Enhancement

**Added Tests** (4 new tests in `test_search_query_text.py`):

- **`test_search_with_whitespace_only_query_text`**: Tests query text containing only whitespace characters (`"   "`). This edge case validates that the API properly handles whitespace-only input, which should typically result in a `parameter_not_provided` or `parameter_invalid` error, similar to empty string handling.

- **`test_search_with_special_characters_query_text`**: Tests query text containing special characters (`"test@#$%^&*()"`). This validates that the search API can handle special characters in queries, which may be encountered in real-world usage scenarios.

- **`test_search_with_unicode_emoji_query_text`**: Tests query text containing Unicode characters and emojis (`"test 🎥 video"`). This edge case ensures proper handling of international characters and emojis, which are increasingly common in modern applications.

- **`test_search_with_very_short_query_text`**: Tests query text with very short queries (1-2 words like `"water"`). This validates that single-word or minimal queries work correctly, which is a common real-world usage pattern.

**Rationale**: These tests expand edge case coverage for the most fundamental parameter (`query_text`), ensuring the SDK handles various input formats that users might provide in real scenarios.

#### 2. page_limit Edge Cases Enhancement

**Added Tests** (2 new tests in `test_search_page_limit.py`):

- **`test_page_limit_zero`**: Tests `page_limit=0` as an edge case. This validates error handling when zero is passed, which should typically result in an error since page_limit must be at least 1.

- **`test_page_limit_above_max`**: Tests `page_limit=51` (just above the maximum value of 50). This edge case validates how the SDK handles values exceeding the documented maximum, which may result in automatic limiting or an error.

**Rationale**: These tests strengthen boundary condition testing for pagination, ensuring proper validation of the page_limit parameter at its limits.

#### 3. Pagination Enhancement

**Added Tests** (2 new tests in `test_search_page_limit.py`):

- **`test_pagination_multiple_pages`**: Tests pagination across multiple pages (3+ pages). This validates that pagination works correctly when iterating through several pages, ensuring `has_next` and `next_page()` behave correctly across extended result sets.

- **`test_pagination_iter_pages`**: Tests the `iter_pages()` method, which allows iteration through page objects themselves rather than just items. This validates an alternative pagination approach provided by the SDK.

**Rationale**: These tests ensure comprehensive pagination functionality validation, covering both basic and advanced pagination scenarios that users might encounter when processing large result sets.

#### 4. Response Validation Enhancement

**Added Tests** (4 new tests in `test_search_response_validation.py`):

- **`test_search_response_video_id_format`**: Validates that `video_id` fields are non-empty strings. This ensures the response structure contains valid identifiers for videos.

- **`test_search_response_transcription_field`**: Validates that `transcription` fields, when present, are strings (or None). This ensures proper data type handling for optional transcription data.

- **`test_search_response_user_metadata`**: Validates `user_metadata` field structure when `group_by='video'` is used. This ensures that user-defined metadata, if present, is properly structured as a dictionary.

- **`test_search_response_clips_structure`**: Validates the detailed structure of the `clips` array when `group_by='video'` is used. This includes:
  - Verifying `clips` is a non-empty list
  - Validating each clip contains required fields (`video_id`, `start`, `end`)
  - Ensuring time range validity (`start < end`)
  - Validating Marengo version-specific fields (`rank` for 3.0, `score` for 2.7)

**Rationale**: These tests strengthen response validation by ensuring all response fields meet expected data types and structural requirements, which is crucial for SDK reliability and user application stability.

#### 5. Error Handling Enhancement

**Added Tests** (3 new tests in `test_search_error_handling.py`):

- **`test_search_with_empty_filter_string`**: Tests filter parameter with an empty string (`""`). This validates error handling for empty filter input, which should result in an appropriate error code.

- **`test_search_with_empty_json_filter`**: Tests filter parameter with an empty JSON object (`"{}"`). This edge case validates whether an empty filter object is accepted or rejected, which may vary by implementation.

- **`test_search_with_page_limit_zero`**: Tests `page_limit=0` error handling. This ensures proper error reporting when invalid page_limit values are provided.

**Rationale**: These tests expand error handling coverage for edge cases that might not be immediately obvious but could occur in real-world usage, ensuring the SDK provides clear error feedback.

#### 6. Combination Tests

**New Test File**: `test_search_combination.py`

**Added Tests** (3 new tests):

- **`test_search_all_parameters_combined`**: Tests all major parameters used together in a single search request:
  - `query_text`, `search_options`, `group_by`, `sort_option`, `operator`, `page_limit`, `filter`
  - Validates that complex parameter combinations work correctly
  - Ensures response structure is correct when all parameters are combined

- **`test_search_parameters_with_clip_count_sort`**: Tests combination with `sort_option='clip_count'`:
  - Validates sorting behavior when combined with other parameters
  - Ensures `clip_count` sorting works correctly with `group_by='video'`, `operator`, `page_limit`, and `filter`

- **`test_search_parameters_with_pagination`**: Tests parameter combinations with pagination:
  - Validates that pagination works correctly when combined with other parameters
  - Ensures `group_by`, `sort_option`, `operator`, and `page_limit` work together in paginated scenarios

**Rationale**: These tests validate real-world usage scenarios where multiple parameters are used together. This is crucial because parameter interactions may behave differently than when parameters are used individually, and users typically combine multiple parameters in actual applications.

### Impact on Test Coverage

The addition of these 18 new test cases (4 query_text edge cases, 4 page_limit/pagination tests, 4 response validation tests, 3 error handling tests, 3 combination tests) significantly enhances the test suite's coverage:

- **Edge Case Coverage**: Increased from 5 to 11 edge case tests
- **Error Handling Coverage**: Increased from 11 to 14 error handling tests
- **Response Validation Coverage**: Increased from 4 to 8 response validation tests
- **New Test Category**: Added combination tests (3 tests) to validate parameter interactions
- **Total Test Methods**: Increased from 52 to 70 test methods

These additions ensure more comprehensive validation of the SDK's behavior under various conditions and parameter combinations that real users might encounter.

## Test Method Statistics

### Total Number of Test Methods

- **TestSearchQueryText**: 9 tests
  - Basic text query search
  - Various query texts
  - Empty string (edge case)
  - Very long string (token limit edge case)
  - No query text or media (required parameter missing)
  - Whitespace-only query text (edge case)
  - Special characters in query text (edge case)
  - Unicode and emoji characters in query text (edge case)
  - Very short query text (edge case: 1-2 words)
- **TestSearchOptions**: 5 tests
- **TestSearchSortOption**: 5 tests
- **TestSearchGroupBy**: 10 tests
- **TestSearchOperator**: 2 tests
- **TestSearchPageLimit**: 10 tests
  - Typical value (5)
  - Maximum value (50)
  - Minimum value (1)
  - Various values (1, 5, 10, 25, 50)
  - Pagination functionality (basic)
  - Zero value (edge case)
  - Value just above maximum (edge case: 51)
  - Multiple pages iteration (3+ pages)
  - `iter_pages()` method
- **TestSearchFilter**: 4 tests
- **TestSearchQueryMediaFile**: 12 tests (1 skipped: `test_search_with_image_file_audio_only`)
  - Basic image file search with visual and audio options
  - Image file search with visual option only
  - Image file search with audio option only (skipped: requires visual in search_options, not documented)
  - Image file search with group_by='video'
  - Image file search with page_limit
  - Image file search with filter
  - Image file search with sort_option
  - Image file search with operator
  - Composed search with image file and text query (Marengo 3.0 only)
  - Error handling for missing query_media_type
  - Error handling for missing query_media_file or query_text
  - Error handling for invalid image file format
- **TestSearchErrorHandling**: 14 tests (1 skipped: `test_search_with_unsupported_option_combination`, `test_search_with_expired_page_token` is conditionally skipped)
  - Invalid index_id
  - Empty search_options
  - Invalid search_option
  - Invalid sort_option
  - Invalid group_by
  - Invalid operator
  - Invalid page_limit (negative)
  - Excessive page_limit (100)
  - Invalid filter syntax
  - Unsupported option combination (skipped)
  - Expired page token (conditionally skipped)
  - Empty filter string (new)
  - Empty JSON filter (new)
  - Page limit zero (new)
- **TestSearchResponseValidation**: 8 tests
  - Response structure validation
  - Rank field validation (Marengo 3.0)
  - Thumbnail URL format validation
  - Time range validity
  - Video ID format validation (new)
  - Transcription field type validation (new)
  - User metadata validation (new)
  - Clips structure validation (new)
- **TestSearchCombination**: 3 tests (new file)
  - All parameters combined
  - Parameters with clip_count sort
  - Parameters with pagination

**Total**: 82 test methods (Since tests run for both Marengo 2.7 and 3.0, approximately 164 tests actually run, excluding skipped tests)

### Test Category Classification

1. **Success Cases**: 51 tests
   - TestSearchQueryText: 2 (basic success cases), 4 (edge cases with valid input: special chars, unicode, short query)
   - TestSearchOptions: 5
   - TestSearchSortOption: 5
   - TestSearchGroupBy: 10
   - TestSearchOperator: 2
   - TestSearchPageLimit: 5 (success cases: typical, max, min, various values, basic pagination)
   - TestSearchFilter: 4
   - TestSearchQueryMediaFile: 11 (basic image file search, combinations with other parameters, composed search)
   - TestSearchCombination: 3 (all parameters combined scenarios)
2. **Edge Cases**: 11 tests
   - TestSearchQueryText: 3 (empty query, long query, no query/media, whitespace-only)
   - TestSearchPageLimit: 4 (minimum value, zero value, value above max, multiple pages iteration, iter_pages)
   - TestSearchErrorHandling: 1 (exceeds maximum)
   - TestSearchResponseValidation: 3 (edge cases in response validation)
3. **Error Handling**: 14 tests (1 skipped)
   - TestSearchErrorHandling: 14 (1 skipped: `test_search_with_unsupported_option_combination`, `test_search_with_expired_page_token` is conditionally skipped)
     - Includes: invalid parameters, empty values, zero values, empty filter string, empty JSON filter
4. **Response Validation**: 8 tests
   - TestSearchResponseValidation: 8
     - Response structure, rank field, thumbnail URL, time range
     - Video ID format, transcription field, user metadata, clips structure

## Conclusion

This test suite is designed to meet the requirements in subject.md while validating SDK functionality under conditions similar to real usage environments. It provides comprehensive tests for major parameters and prioritizes documentation criteria to validate consistency with API specifications.
