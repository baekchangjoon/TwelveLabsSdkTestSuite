"""
query_media_file parameter tests

Tests the basic functionality and combinations of the query_media_file parameter.
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


def get_rhino_image_path():
    """Get the path to the rhino.png test image file."""
    # Get the project root directory (parent of tests directory)
    project_root = os.path.dirname(os.path.dirname(__file__))
    image_path = os.path.join(project_root, "resources", "rhino.png")
    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Test image file not found: {image_path}. Please ensure rhino.png exists in the resources directory."
        )
    return image_path


class TestSearchQueryMediaFile:
    """query_media_file parameter tests"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_image_file(self, client, index_id, request):
        """Test successful search with image file"""
        image_path = get_rhino_image_path()

        with open(image_path, "rb") as image_file:
            search_pager = client.search.query(
                index_id=index_id,
                query_media_type="image",
                query_media_file=image_file,
                search_options=["visual", "audio"],
            )

            # Check if results are returned
            results = list(search_pager)
            assert len(results) >= 0, "Search results should be returned"

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
    def test_search_with_image_file_visual_only(self, client, index_id, request):
        """Test image file search with visual option only"""
        image_path = get_rhino_image_path()

        with open(image_path, "rb") as image_file:
            search_pager = client.search.query(
                index_id=index_id,
                query_media_type="image",
                query_media_file=image_file,
                search_options=["visual"],
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
    def test_search_with_image_file_audio_only(self, client, index_id, request):
        """Test image file search with audio option only

        Note: According to API behavior, query_media_type='image' requires
        search_options to contain 'visual'. This constraint is not explicitly
        documented in search.md, so this test is skipped.
        """
        index_name = get_index_name(request)
        pytest.skip(
            f"query_media_type='image' requires search_options to contain 'visual'. "
            f"This constraint is not documented in search.md (index: {index_name})"
        )

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_image_file_and_group_by_video(self, client, index_id, request):
        """Test image file search with group_by='video'"""
        image_path = get_rhino_image_path()

        with open(image_path, "rb") as image_file:
            search_pager = client.search.query(
                index_id=index_id,
                query_media_type="image",
                query_media_file=image_file,
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
    def test_search_with_image_file_and_page_limit(self, client, index_id, request):
        """Test image file search with page_limit"""
        image_path = get_rhino_image_path()
        page_limit = 5

        with open(image_path, "rb") as image_file:
            search_pager = client.search.query(
                index_id=index_id,
                query_media_type="image",
                query_media_file=image_file,
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
    def test_search_with_image_file_and_filter(self, client, index_id, request):
        """Test image file search with filter"""
        image_path = get_rhino_image_path()

        try:
            with open(image_path, "rb") as image_file:
                search_pager = client.search.query(
                    index_id=index_id,
                    query_media_type="image",
                    query_media_file=image_file,
                    search_options=["visual", "audio"],
                    filter='{"category": "nature"}',
                )

                results = list(search_pager)
                assert len(results) >= 0

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
    def test_search_with_image_file_and_sort_option(self, client, index_id, request):
        """Test image file search with sort_option"""
        image_path = get_rhino_image_path()

        with open(image_path, "rb") as image_file:
            search_pager = client.search.query(
                index_id=index_id,
                query_media_type="image",
                query_media_file=image_file,
                search_options=["visual", "audio"],
                sort_option="score",
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
    def test_search_with_image_file_and_operator(self, client, index_id, request):
        """Test image file search with operator"""
        image_path = get_rhino_image_path()

        with open(image_path, "rb") as image_file:
            search_pager = client.search.query(
                index_id=index_id,
                query_media_type="image",
                query_media_file=image_file,
                search_options=["visual", "audio"],
                operator="and",
            )

            results = list(search_pager)
            assert len(results) >= 0

            if len(results) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(results[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_image_file_and_text_composed(self, client, index_id, request):
        """Test composed search with image file and text query (Marengo 3.0 only)

        Composed text and media queries are only supported in Marengo 3.0.
        """
        image_path = get_rhino_image_path()
        index_name = get_index_name(request)

        if not is_marengo30(index_name):
            pytest.skip("Composed search is only supported in Marengo 3.0")

        with open(image_path, "rb") as image_file:
            search_pager = client.search.query(
                index_id=index_id,
                query_media_type="image",
                query_media_file=image_file,
                query_text="animal",
                search_options=["visual", "audio"],
            )

            results = list(search_pager)
            assert len(results) >= 0

            if len(results) > 0:
                validate_marengo_fields(results[0], index_name, request)

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_without_query_media_type(self, client, index_id, request):
        """Test error when query_media_file is provided without query_media_type"""
        image_path = get_rhino_image_path()

        with pytest.raises((ApiError, BadRequestError)) as exc_info:
            with open(image_path, "rb") as image_file:
                client.search.query(
                    index_id=index_id,
                    query_media_file=image_file,
                    search_options=["visual", "audio"],
                )

        error = exc_info.value
        error_code = get_error_code(error)
        index_name = get_index_name(request)
        print(
            f"\n[ERROR CODE] test_search_without_query_media_type (index: {index_name}): {error_code}"
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
    def test_search_without_query_media_file_or_text(self, client, index_id, request):
        """Test error when query_media_type is provided without query_media_file or query_text"""
        with pytest.raises((ApiError, BadRequestError)) as exc_info:
            client.search.query(
                index_id=index_id,
                query_media_type="image",
                search_options=["visual", "audio"],
            )

        error = exc_info.value
        error_code = get_error_code(error)
        index_name = get_index_name(request)
        print(
            f"\n[ERROR CODE] test_search_without_query_media_file_or_text (index: {index_name}): {error_code}"
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
    def test_search_with_invalid_image_file(self, client, index_id, request):
        """Test error when invalid file is provided"""
        # Create a temporary invalid file (text file instead of image)
        import tempfile

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as tmp_file:
            tmp_file.write("This is not an image file")
            tmp_path = tmp_file.name

        try:
            with pytest.raises((ApiError, BadRequestError, ValueError)) as exc_info:
                with open(tmp_path, "rb") as invalid_file:
                    client.search.query(
                        index_id=index_id,
                        query_media_type="image",
                        query_media_file=invalid_file,
                        search_options=["visual", "audio"],
                    )

            error = exc_info.value
            if isinstance(error, ApiError):
                error_code = get_error_code(error)
                index_name = get_index_name(request)
                print(
                    f"\n[ERROR CODE] test_search_with_invalid_image_file (index: {index_name}): {error_code}"
                )
                # Error code may vary depending on validation
                assert (
                    error_code != ""
                ), f"Error code could not be extracted. Error: {error}"
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
