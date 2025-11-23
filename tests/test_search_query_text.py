"""
query_text parameter tests

Tests the basic functionality and edge cases of the query_text parameter.
"""

import os
import sys

import pytest
from twelvelabs.core.api_error import ApiError

try:
    from twelvelabs.errors.bad_request_error import BadRequestError
except ImportError:
    BadRequestError = ApiError
sys.path.insert(0, os.path.dirname(__file__))
from conftest import (
    get_error_code,
    get_index_name,
    is_marengo30,
    validate_marengo_fields,
)


class TestSearchQueryText:
    """query_text parameter tests"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_text_query(self, client, index_id, request):
        """Test successful search with basic text query"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="Otter swim with cat",
            search_options=["visual", "audio"],
        )

        # Check if results are returned
        results = list(search_pager)
        assert len(results) > 0, "Search results should be returned"

        # Check required fields of the first result (by Marengo version)
        first_result = results[0]
        index_name = get_index_name(request)
        validate_marengo_fields(first_result, index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_different_query_text(self, client, index_id, request):
        """Test search with different text query"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="A man fall into water",
            search_options=["visual", "audio"],
        )

        results = list(search_pager)
        assert len(results) >= 0, "Search results should be 0 or more"

        # Validate fields by Marengo version if results exist
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_empty_query_text(self, client, index_id, request):
        """Test empty query text

        Empty query text should raise parameter_not_provided error.
        """
        with pytest.raises((ApiError, BadRequestError)) as exc_info:
            client.search.query(
                index_id=index_id, query_text="", search_options=["visual", "audio"]
            )

        # Check error code
        error = exc_info.value
        error_code = get_error_code(error)

        index_name = get_index_name(request)
        print(
            f"\n[ERROR CODE] test_search_with_empty_query_text (index: {index_name}): {error_code}"
        )

        # parameter_not_provided or parameter_invalid error may occur
        expected_codes = ["parameter_not_provided", "parameter_invalid"]
        assert (
            error_code in expected_codes
        ), f"Expected error code: {expected_codes}, actual error code: {error_code}"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_very_long_query_text(self, client, index_id, request):
        """Test very long query text

        Marengo 2.7: maximum 77 tokens, Marengo 3.0: maximum 500 tokens
        Exceeding token limit should raise parameter_invalid error.
        """
        long_query = (
            "test " * 100
        )  # Approximately 500 characters (exceeds limit in Marengo 2.7)
        index_name = get_index_name(request)

        if is_marengo30(index_name):
            # Marengo 3.0 supports up to 500 tokens, so this query should pass
            search_pager = client.search.query(
                index_id=index_id,
                query_text=long_query,
                search_options=["visual", "audio"],
            )
            results = list(search_pager)
            assert len(results) >= 0
            if len(results) > 0:
                validate_marengo_fields(results[0], index_name, request)
        else:
            # Marengo 2.7 has 77 token limit, so BadRequestError is expected
            with pytest.raises((ApiError, BadRequestError)) as exc_info:
                client.search.query(
                    index_id=index_id,
                    query_text=long_query,
                    search_options=["visual", "audio"],
                )

            # Check error code
            error = exc_info.value
            error_code = get_error_code(error)

            print(
                f"\n[ERROR CODE] test_search_with_very_long_query_text (index: {index_name}): {error_code}"
            )

            # parameter_invalid error should occur (token limit exceeded)
            expected_code = "parameter_invalid"
            assert (
                error_code == expected_code
            ), f"Expected error code: {expected_code}, actual error code: {error_code}"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_without_query_text_or_media(self, client, index_id, request):
        """Test when both query text and media are missing

        If both query text and media are missing, parameter_not_provided error should occur.
        """
        with pytest.raises((ApiError, BadRequestError)) as exc_info:
            client.search.query(index_id=index_id, search_options=["visual", "audio"])

        # Check error code
        error = exc_info.value
        error_code = get_error_code(error)

        index_name = get_index_name(request)
        print(
            f"\n[ERROR CODE] test_search_without_query_text_or_media (index: {index_name}): {error_code}"
        )

        # parameter_not_provided error should occur
        expected_code = "parameter_not_provided"
        assert (
            error_code == expected_code
        ), f"Expected error code: {expected_code}, actual error code: {error_code}"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_whitespace_only_query_text(self, client, index_id, request):
        """Test query text with only whitespace characters"""
        with pytest.raises((ApiError, BadRequestError)) as exc_info:
            client.search.query(
                index_id=index_id,
                query_text="   ",
                search_options=["visual", "audio"],
            )

        error = exc_info.value
        error_code = get_error_code(error)
        index_name = get_index_name(request)
        print(
            f"\n[ERROR CODE] test_search_with_whitespace_only_query_text (index: {index_name}): {error_code}"
        )

        expected_codes = ["parameter_not_provided", "parameter_invalid"]
        assert (
            error_code in expected_codes
        ), f"Expected error code: {expected_codes}, actual error code: {error_code}"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_special_characters_query_text(self, client, index_id, request):
        """Test query text with special characters"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test@#$%^&*()",
            search_options=["visual", "audio"],
        )

        results = list(search_pager)
        assert len(results) >= 0

        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_unicode_emoji_query_text(self, client, index_id, request):
        """Test query text with unicode and emoji characters"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test 🎥 video",
            search_options=["visual", "audio"],
        )

        results = list(search_pager)
        assert len(results) >= 0

        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_very_short_query_text(self, client, index_id, request):
        """Test query text with very short query (1-2 words)"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
        )

        results = list(search_pager)
        assert len(results) >= 0

        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)
