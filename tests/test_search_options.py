"""
Search Options 파라미터 테스트

다양한 search_options 조합을 테스트하여 실제 사용자가 겪을 수 있는 다양한 사용 패턴을 검증합니다.
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
    """search_options 파라미터 테스트"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_options_visual_and_audio(self, client, index_id, request):
        """visual과 audio 옵션 조합 테스트"""
        search_pager = client.search.query(
            index_id=index_id, query_text="animal", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        assert len(results) >= 0

        # 결과가 있는 경우 Marengo 버전별 필드 검증
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
        """transcription 옵션 테스트

        Marengo 2.7: search_option_not_supported 에러 발생 예상
        Marengo 3.0: 정상적으로 작동
        """
        index_name = get_index_name(request)

        if is_marengo30(index_name):
            # Marengo 3.0: 정상적으로 작동해야 함
            search_pager = client.search.query(
                index_id=index_id, query_text="hello", search_options=["transcription"]
            )

            results = list(search_pager)
            assert len(results) >= 0

            # 결과가 있는 경우 Marengo 버전별 필드 검증
            if len(results) > 0:
                validate_marengo_fields(results[0], index_name, request)
        else:
            # Marengo 2.7: search_option_not_supported 에러 발생 예상
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
            ), f"예상된 에러 코드: {expected_code}, 실제 발생한 에러 코드: {error_code}"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_options_all_combined(self, client, index_id, request):
        """모든 옵션 조합 테스트

        Marengo 2.7: search_option_not_supported 에러 발생 예상
        Marengo 3.0: 정상적으로 작동
        """
        index_name = get_index_name(request)

        if is_marengo30(index_name):
            # Marengo 3.0: 정상적으로 작동해야 함
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio", "transcription"],
            )

            results = list(search_pager)
            assert len(results) >= 0

            # 결과가 있는 경우 Marengo 버전별 필드 검증
            if len(results) > 0:
                validate_marengo_fields(results[0], index_name, request)
        else:
            # Marengo 2.7: search_option_not_supported 에러 발생 예상
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
            ), f"예상된 에러 코드: {expected_code}, 실제 발생한 에러 코드: {error_code}"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_options_visual_only(self, client, index_id, request):
        """visual 옵션만 사용한 검색 테스트"""
        search_pager = client.search.query(
            index_id=index_id, query_text="swimming", search_options=["visual"]
        )

        results = list(search_pager)
        assert len(results) >= 0, "검색 결과는 0개 이상이어야 합니다"

        # 결과가 있는 경우 Marengo 버전별 필드 검증
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
        """audio 옵션만 사용한 검색 테스트"""
        search_pager = client.search.query(
            index_id=index_id, query_text="water", search_options=["audio"]
        )

        results = list(search_pager)
        assert len(results) >= 0, "검색 결과는 0개 이상이어야 합니다"

        # 결과가 있는 경우 Marengo 버전별 필드 검증
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)
