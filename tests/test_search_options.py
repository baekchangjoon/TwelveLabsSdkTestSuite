"""
Search Options parameter tests

Tests various search_options combinations to validate different usage patterns that real users may encounter.
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


class TestSearchOptions:
    """search_options parameter tests"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_options_visual_and_audio(self, client, index_id, request):
        """Test visual and audio options combination"""
        search_pager = client.search.query(
            index_id=index_id, query_text="animal", search_options=["visual", "audio"]
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
    def test_search_options_transcription(self, client, index_id, request):
        """Test transcription option

        Marengo 2.7: search_option_not_supported error expected
        Marengo 3.0: should work normally
        """
        index_name = get_index_name(request)

        if is_marengo30(index_name):
            # Marengo 3.0: should work normally
            search_pager = client.search.query(
                index_id=index_id, query_text="hello", search_options=["transcription"]
            )

            results = list(search_pager)
            assert len(results) >= 0

            # Validate fields by Marengo version if results exist
            if len(results) > 0:
                validate_marengo_fields(results[0], index_name, request)
        else:
            # Marengo 2.7: search_option_not_supported error expected
            with pytest.raises(ApiError) as exc_info:
                client.search.query(
                    index_id=index_id,
                    query_text="hello",
                    search_options=["transcription"],
                )

            error = exc_info.value
            error_code = get_error_code(error)

            print(
                f"\n[ERROR CODE] test_search_options_transcription (index: {index_name}): {error_code}"
            )

            expected_code = "search_option_not_supported"
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
    def test_search_options_all_combined(self, client, index_id, request):
        """Test all options combination

        Marengo 2.7: search_option_not_supported error expected
        Marengo 3.0: should work normally
        """
        index_name = get_index_name(request)

        if is_marengo30(index_name):
            # Marengo 3.0: should work normally
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio", "transcription"],
            )

            results = list(search_pager)
            assert len(results) >= 0

            # Validate fields by Marengo version if results exist
            if len(results) > 0:
                validate_marengo_fields(results[0], index_name, request)
        else:
            # Marengo 2.7: search_option_not_supported error expected
            with pytest.raises(ApiError) as exc_info:
                client.search.query(
                    index_id=index_id,
                    query_text="test",
                    search_options=["visual", "audio", "transcription"],
                )

            error = exc_info.value
            error_code = get_error_code(error)

            print(
                f"\n[ERROR CODE] test_search_options_all_combined (index: {index_name}): {error_code}"
            )

            expected_code = "search_option_not_supported"
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
    def test_search_options_visual_only(self, client, index_id, request):
        """Test search with visual option only"""
        search_pager = client.search.query(
            index_id=index_id, query_text="swimming", search_options=["visual"]
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
    def test_search_options_audio_only(self, client, index_id, request):
        """Test search with audio option only"""
        search_pager = client.search.query(
            index_id=index_id, query_text="water", search_options=["audio"]
        )

        results = list(search_pager)
        assert len(results) >= 0, "Search results should be 0 or more"

        # Validate fields by Marengo version if results exist
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)
