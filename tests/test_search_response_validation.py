"""
Response validation tests

Validates the structure, data types, and value validity of search responses.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
from conftest import get_index_name, is_marengo30, validate_marengo_fields


class TestSearchResponseValidation:
    """Response validation tests"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_structure(self, client, index_id, request):
        """Validate search response structure"""
        search_pager = client.search.query(
            index_id=index_id, query_text="test", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        if len(results) > 0:
            item = results[0]
            index_name = get_index_name(request)

            # Validate fields by Marengo version
            validate_marengo_fields(item, index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_with_rank(self, client, index_id, request):
        """Validate rank field (Marengo 3.0)"""
        search_pager = client.search.query(
            index_id=index_id, query_text="test", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

            # Additional validation if rank exists (Marengo 3.0)
            ranks = [r.rank for r in results if r.rank is not None]
            if len(ranks) > 0:
                assert all(isinstance(r, int) for r in ranks), "rank must be an integer"
                assert all(
                    r > 0 for r in ranks
                ), "rank must be greater than or equal to 1"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_with_thumbnail_url(self, client, index_id, request):
        """Validate thumbnail_url field"""
        search_pager = client.search.query(
            index_id=index_id, query_text="test", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

            for item in results:
                if item.thumbnail_url is not None:
                    assert isinstance(
                        item.thumbnail_url, str
                    ), "thumbnail_url must be a string"
                    assert item.thumbnail_url.startswith(
                        "http"
                    ), "thumbnail_url must be in URL format"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_time_range(self, client, index_id, request):
        """Validate time range validity"""
        search_pager = client.search.query(
            index_id=index_id, query_text="test", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

        for item in results:
            if item.start is not None and item.end is not None:
                assert item.start >= 0, "start must be greater than or equal to 0"
                assert item.end > item.start, "end must be greater than start"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_video_id_format(self, client, index_id, request):
        """Validate video_id field format"""
        search_pager = client.search.query(
            index_id=index_id, query_text="test", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

            for item in results:
                if item.video_id is not None:
                    assert isinstance(item.video_id, str), "video_id must be a string"
                    assert len(item.video_id) > 0, "video_id must not be empty"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_transcription_field(self, client, index_id, request):
        """Validate transcription field type"""
        search_pager = client.search.query(
            index_id=index_id, query_text="test", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

            for item in results:
                if item.transcription is not None:
                    assert isinstance(
                        item.transcription, str
                    ), "transcription must be a string or None"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_user_metadata(self, client, index_id, request):
        """Validate user_metadata field when group_by='video'"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            group_by="video",
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)

            for item in results:
                if item.id is not None:  # Grouped by video
                    # When grouped by video, top-level item doesn't have start/end
                    # Validate clips structure instead
                    if item.clips and len(item.clips) > 0:
                        validate_marengo_fields(item.clips[0], index_name, request)

                    # user_metadata is optional, but if present should be a dict
                    if item.user_metadata is not None:
                        assert isinstance(
                            item.user_metadata, dict
                        ), "user_metadata must be a dictionary or None"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_clips_structure(self, client, index_id, request):
        """Validate clips array structure when group_by='video'"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            group_by="video",
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)

            for item in results:
                if item.id is not None and item.clips is not None:
                    assert isinstance(item.clips, list), "clips must be a list"
                    assert len(item.clips) > 0, "clips must not be empty"

                    # Validate each clip in clips array
                    for clip in item.clips:
                        assert clip.video_id is not None, "clip.video_id must exist"
                        assert clip.start is not None, "clip.start must exist"
                        assert clip.end is not None, "clip.end must exist"
                        assert (
                            clip.start < clip.end
                        ), "clip.start must be less than clip.end"

                        # Validate Marengo version specific fields using validate_marengo_fields
                        validate_marengo_fields(clip, index_name, request)
