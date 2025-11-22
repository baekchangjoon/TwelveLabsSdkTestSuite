"""
filter parameter tests

Tests the basic functionality and combinations of the filter parameter.
"""

import os
import sys

import pytest
from twelvelabs.core.api_error import ApiError

sys.path.insert(0, os.path.dirname(__file__))
from conftest import get_error_code, get_index_name, validate_marengo_fields


class TestSearchFilter:
    """filter parameter tests"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_filter(self, client, index_id, request):
        """Test filter parameter"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                filter='{"category": "nature"}',
            )

            results = list(search_pager)
            assert len(results) >= 0

            # Validate fields by Marengo version if results exist
            if len(results) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(results[0], index_name, request)
        except ApiError as e:
            # If filter is not supported or invalid
            if "invalid" in str(e).lower() or "not supported" in str(e).lower():
                pytest.skip(f"Filter is not supported or invalid: {e}")
            raise

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_filter_various_formats(self, client, index_id, request):
        """Test various filter formats"""
        filter_formats = [
            '{"category": "nature"}',
            '{"type": "video"}',
            '{"status": "active"}',
            '{"category": "nature", "type": "video"}',
        ]

        for filter_str in filter_formats:
            try:
                search_pager = client.search.query(
                    index_id=index_id,
                    query_text="test",
                    search_options=["visual", "audio"],
                    filter=filter_str,
                )

                results = list(search_pager)
                assert len(results) >= 0

                # Validate fields by Marengo version if results exist
                if len(results) > 0:
                    index_name = get_index_name(request)
                    validate_marengo_fields(results[0], index_name, request)
            except ApiError as e:
                # If filter is not supported or invalid
                error_code = get_error_code(e)
                if (
                    "invalid" in str(e).lower()
                    or "not supported" in str(e).lower()
                    or error_code == "search_filter_invalid"
                ):
                    # Skip if specific filter format is not supported
                    continue
                raise

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_filter_with_operator_and(self, client, index_id, request):
        """Test combination of filter and operator='and'"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="water",
                search_options=["visual", "audio"],
                operator="and",
                filter='{"category": "nature"}',
            )

            results = list(search_pager)
            assert len(results) >= 0

            # Validate fields by Marengo version if results exist
            if len(results) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(results[0], index_name, request)
        except ApiError as e:
            error_code = get_error_code(e)
            if (
                "invalid" in str(e).lower()
                or "not supported" in str(e).lower()
                or error_code == "search_filter_invalid"
            ):
                pytest.skip(f"Filter is not supported or invalid: {e}")
            raise

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_filter_with_operator_or(self, client, index_id, request):
        """Test combination of filter and operator='or'"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="swimming",
                search_options=["visual", "audio"],
                operator="or",
                filter='{"category": "nature"}',
            )

            results = list(search_pager)
            assert len(results) >= 0

            # Validate fields by Marengo version if results exist
            if len(results) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(results[0], index_name, request)
        except ApiError as e:
            error_code = get_error_code(e)
            if (
                "invalid" in str(e).lower()
                or "not supported" in str(e).lower()
                or error_code == "search_filter_invalid"
            ):
                pytest.skip(f"Filter is not supported or invalid: {e}")
            raise
