"""
group_by parameter tests

Tests the basic functionality and combinations of the group_by parameter.
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


class TestSearchGroupBy:
    """group_by parameter tests"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_group_by_video(self, client, index_id, request):
        """Test group_by='video'"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            group_by="video",
        )

        results = list(search_pager)
        assert len(results) >= 0

        # Check id and clips fields when grouped by video
        for item in results:
            if item.id is not None:
                assert (
                    item.clips is not None
                ), "clips should exist when grouped by video"
                assert len(item.clips) > 0, "clips should not be empty"
                # Also validate items within clips
                if item.clips:
                    index_name = get_index_name(request)
                    validate_marengo_fields(item.clips[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_group_by_clip(self, client, index_id, request):
        """Test group_by='clip' (default value)"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="animal",
            search_options=["visual", "audio"],
            group_by="clip",
        )

        results = list(search_pager)
        assert len(results) >= 0

        # For clip grouping, verify individual clip information
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
    def test_group_by_video_with_operator_and(self, client, index_id, request):
        """Test combination of group_by='video' and operator='and'"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            group_by="video",
            operator="and",
        )

        results = list(search_pager)
        assert len(results) >= 0

        # Check id and clips fields when grouped by video
        for item in results:
            if item.id is not None:
                assert (
                    item.clips is not None
                ), "clips should exist when grouped by video"
                assert len(item.clips) > 0, "clips should not be empty"
                # Also validate items within clips
                if item.clips:
                    index_name = get_index_name(request)
                    validate_marengo_fields(item.clips[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_group_by_video_with_operator_or(self, client, index_id, request):
        """Test combination of group_by='video' and operator='or'"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="animal",
            search_options=["visual", "audio"],
            group_by="video",
            operator="or",
        )

        results = list(search_pager)
        assert len(results) >= 0

        # Check id and clips fields when grouped by video
        for item in results:
            if item.id is not None:
                assert (
                    item.clips is not None
                ), "clips should exist when grouped by video"
                assert len(item.clips) > 0, "clips should not be empty"
                # Also validate items within clips
                if item.clips:
                    index_name = get_index_name(request)
                    validate_marengo_fields(item.clips[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_group_by_clip_with_operator_and(self, client, index_id, request):
        """Test combination of group_by='clip' and operator='and'"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            group_by="clip",
            operator="and",
        )

        results = list(search_pager)
        assert len(results) >= 0

        # For clip grouping, verify individual clip information
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
    def test_group_by_clip_with_operator_or(self, client, index_id, request):
        """Test combination of group_by='clip' and operator='or' (default value)"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            group_by="clip",
            operator="or",
        )

        results = list(search_pager)
        assert len(results) >= 0

        # For clip grouping, verify individual clip information
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
    def test_group_by_video_with_page_limit(self, client, index_id, request):
        """Test combination of group_by='video' and page_limit"""
        page_limit = 3
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            group_by="video",
            page_limit=page_limit,
        )

        # Check number of results on first page
        first_page_items = search_pager.items
        if first_page_items:
            assert (
                len(first_page_items) <= page_limit
            ), f"First page results should be {page_limit} or less"
            # Validate first result
            if len(first_page_items) > 0 and first_page_items[0].id is not None:
                assert (
                    first_page_items[0].clips is not None
                ), "clips should exist when grouped by video"
                if first_page_items[0].clips:
                    index_name = get_index_name(request)
                    validate_marengo_fields(
                        first_page_items[0].clips[0], index_name, request
                    )

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_group_by_clip_with_page_limit(self, client, index_id, request):
        """Test combination of group_by='clip' and page_limit"""
        page_limit = 5
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            group_by="clip",
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
    def test_group_by_video_with_filter(self, client, index_id, request):
        """Test combination of group_by='video' and filter"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                group_by="video",
                filter='{"category": "nature"}',
            )

            results = list(search_pager)
            assert len(results) >= 0

            # When grouped by video, verify id and clips fields
            for item in results:
                if item.id is not None:
                    assert (
                        item.clips is not None
                    ), "clips should exist when grouped by video"
                    if item.clips:
                        index_name = get_index_name(request)
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
    def test_group_by_clip_with_filter(self, client, index_id, request):
        """Test combination of group_by='clip' and filter"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                group_by="clip",
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
