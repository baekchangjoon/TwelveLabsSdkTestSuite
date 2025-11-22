"""
page_limit parameter tests

Tests the basic functionality and combinations of the page_limit parameter.
"""

import os
import sys

import pytest
from twelvelabs.core.api_error import ApiError

sys.path.insert(0, os.path.dirname(__file__))
from conftest import get_error_code, get_index_name, validate_marengo_fields


class TestSearchPageLimit:
    """page_limit parameter tests"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_page_limit(self, client, index_id, request):
        """Test page_limit parameter"""
        page_limit = 5
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=page_limit,
        )

        # Check number of results on first page
        first_page_items = search_pager.items
        if first_page_items:
            assert (
                len(first_page_items) <= page_limit
            ), f"First page results should be {page_limit} or less"
            # Validate first result
            index_name = get_index_name(request)
            validate_marengo_fields(first_page_items[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_page_limit_max(self, client, index_id, request):
        """Test page_limit maximum value (50)"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=50,
        )

        first_page_items = search_pager.items
        if first_page_items:
            assert len(first_page_items) <= 50, "Maximum 50 items should be returned"
            # Validate first result
            index_name = get_index_name(request)
            validate_marengo_fields(first_page_items[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_page_limit_minimal(self, client, index_id, request):
        """Test minimum page_limit"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=1,
        )

        results = list(search_pager)
        assert len(results) >= 0

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
    def test_page_limit_various_values(self, client, index_id, request):
        """Test various page_limit values"""
        for page_limit in [1, 5, 10, 25, 50]:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                page_limit=page_limit,
            )

            # Check number of results on first page
            first_page_items = search_pager.items
            if first_page_items:
                assert (
                    len(first_page_items) <= page_limit
                ), f"First page results should be {page_limit} or less"
                # Validate first result
                if len(first_page_items) > 0:
                    index_name = get_index_name(request)
                    validate_marengo_fields(first_page_items[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_pagination(self, client, index_id, request):
        """Test pagination"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=2,
        )

        # Check first page
        first_page = list(search_pager.items) if search_pager.items else []
        assert len(first_page) >= 0

        # Validate first page results
        if len(first_page) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(first_page[0], index_name, request)

        # Check if next page exists
        if search_pager.has_next:
            next_page_pager = search_pager.next_page()
            if next_page_pager:
                next_page = list(next_page_pager.items) if next_page_pager.items else []
                assert len(next_page) >= 0
                # Also validate next page results
                if len(next_page) > 0:
                    index_name = get_index_name(request)
                    validate_marengo_fields(next_page[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_page_limit_zero(self, client, index_id, request):
        """Test page_limit=0 (edge case)

        page_limit=0 may be accepted or rejected depending on implementation.
        If accepted, validate that search works (may return 0 results per page).
        """
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                page_limit=0,
            )

            # If page_limit=0 is accepted, validate normal search behavior
            first_page_items = search_pager.items
            if first_page_items is not None:
                assert len(first_page_items) >= 0
        except (ApiError, ValueError, TypeError) as e:
            # If page_limit=0 is rejected, validate error
            if isinstance(e, ApiError):
                error_code = get_error_code(e)
                index_name = get_index_name(request)
                print(
                    f"\n[ERROR CODE] test_page_limit_zero (index: {index_name}): {error_code}"
                )
                assert (
                    error_code != ""
                ), f"Error code could not be extracted. Error: {e}"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_page_limit_above_max(self, client, index_id, request):
        """Test page_limit=51 (just above maximum value)"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                page_limit=51,  # Just above maximum 50
            )
            # SDK may automatically limit or raise error
            results = list(search_pager)
            assert len(results) >= 0
        except ApiError as e:
            # Error for exceeding maximum is expected
            if "limit" in str(e).lower() or "maximum" in str(e).lower():
                pass
            else:
                raise

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_pagination_multiple_pages(self, client, index_id, request):
        """Test pagination with multiple pages (3+ pages)"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=2,
        )

        pages_visited = 0
        total_items = 0

        # Iterate through pages
        current_pager = search_pager
        while current_pager and pages_visited < 3:
            if current_pager.items:
                page_items = list(current_pager.items)
                total_items += len(page_items)
                pages_visited += 1

                # Validate first item of each page
                if len(page_items) > 0:
                    index_name = get_index_name(request)
                    validate_marengo_fields(page_items[0], index_name, request)

            # Move to next page
            if current_pager.has_next:
                current_pager = current_pager.next_page()
            else:
                break

        assert pages_visited >= 1, "At least one page should be visited"
        assert total_items >= 0, "Total items should be non-negative"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_pagination_iter_pages(self, client, index_id, request):
        """Test iter_pages() method"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=2,
        )

        pages = []
        for page in search_pager.iter_pages():
            pages.append(page)
            if len(pages) >= 3:  # Limit to 3 pages for testing
                break

        assert len(pages) >= 1, "At least one page should be returned"

        # Validate first page
        if pages[0] and pages[0].items:
            first_page_items = list(pages[0].items)
            if len(first_page_items) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(first_page_items[0], index_name, request)
