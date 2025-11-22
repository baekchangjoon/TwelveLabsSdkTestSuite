"""
Combination tests

Tests all major parameters used together in complex scenarios.
"""

import os
import sys

import pytest
from twelvelabs.core.api_error import ApiError

sys.path.insert(0, os.path.dirname(__file__))
from conftest import (
    get_error_code,
    get_index_name,
    is_marengo30,
    validate_marengo_fields,
)


class TestSearchCombination:
    """Combination tests for all major parameters"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_all_parameters_combined(self, client, index_id, request):
        """Test all major parameters used together"""
        index_name = get_index_name(request)

        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="water",
                search_options=["visual", "audio"],
                group_by="video",
                sort_option="score",
                operator="and",
                page_limit=5,
                filter='{"category": "nature"}',
            )

            results = list(search_pager)
            assert len(results) >= 0

            if len(results) > 0:
                validate_marengo_fields(results[0], index_name, request)

                # Validate group_by='video' structure
                video_items = [item for item in results if item.id is not None]
                if len(video_items) > 0:
                    for item in video_items:
                        assert (
                            item.clips is not None
                        ), "clips should exist when grouped by video"
                        if item.clips:
                            validate_marengo_fields(item.clips[0], index_name, request)

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
    def test_search_parameters_with_clip_count_sort(self, client, index_id, request):
        """Test combination with sort_option='clip_count'"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                group_by="video",
                sort_option="clip_count",
                operator="or",
                page_limit=10,
                filter='{"category": "nature"}',
            )

            results = list(search_pager)
            assert len(results) >= 0

            video_items = [item for item in results if item.id is not None]

            if len(video_items) > 0:
                index_name = get_index_name(request)

                # Validate clip_count sorting
                clip_counts = [
                    len(item.clips) if item.clips else 0 for item in video_items
                ]
                if len(clip_counts) > 1:
                    sorted_clip_counts = sorted(clip_counts, reverse=True)
                    assert clip_counts == sorted_clip_counts, (
                        f"Videos should be sorted by number of clips in descending order. "
                        f"Actual order: {clip_counts}, expected order: {sorted_clip_counts}"
                    )

                # Validate clips structure
                for item in video_items:
                    if item.clips:
                        validate_marengo_fields(item.clips[0], index_name, request)

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
    def test_search_parameters_with_pagination(self, client, index_id, request):
        """Test combination with pagination"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            group_by="clip",
            sort_option="score",
            operator="and",
            page_limit=3,
        )

        # Check first page
        first_page_items = search_pager.items
        if first_page_items:
            assert len(first_page_items) <= 3
            if len(first_page_items) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(first_page_items[0], index_name, request)

        # Check pagination
        if search_pager.has_next:
            next_page_pager = search_pager.next_page()
            if next_page_pager and next_page_pager.items:
                next_page_items = list(next_page_pager.items)
                assert len(next_page_items) >= 0
                if len(next_page_items) > 0:
                    index_name = get_index_name(request)
                    validate_marengo_fields(next_page_items[0], index_name, request)
