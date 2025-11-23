"""
query_text 파라미터 테스트

query_text 파라미터의 기본 기능 및 엣지 케이스를 테스트합니다.
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
    """query_text 파라미터 테스트"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_text_query(self, client, index_id, request):
        """기본 텍스트 쿼리로 검색 성공 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="Otter swim with cat",
            search_options=["visual", "audio"],
        )

        # 결과가 반환되는지 확인
        results = list(search_pager)
        assert len(results) > 0, "검색 결과가 반환되어야 합니다"

        # 첫 번째 결과의 필수 필드 확인 (Marengo 버전별)
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
        """다른 텍스트 쿼리로 검색 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="A man fall into water",
            search_options=["visual", "audio"],
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
    def test_search_with_empty_query_text(self, client, index_id, request):
        """빈 쿼리 텍스트 테스트

        빈 쿼리 텍스트는 parameter_not_provided 에러를 발생시킵니다.
        """
        with pytest.raises((ApiError, BadRequestError)) as exc_info:
            client.search.query(
                index_id=index_id, query_text="", search_options=["visual", "audio"]
            )

        # 에러 코드 확인
        error = exc_info.value
        error_code = get_error_code(error)

        index_name = get_index_name(request)
        print(
            f"\n[ERROR CODE] test_search_with_empty_query_text (index: {index_name}): {error_code}"
        )

        # parameter_not_provided 또는 parameter_invalid 에러가 발생할 수 있음
        expected_codes = ["parameter_not_provided", "parameter_invalid"]
        assert (
            error_code in expected_codes
        ), f"예상된 에러 코드: {expected_codes}, 실제 발생한 에러 코드: {error_code}"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_with_very_long_query_text(self, client, index_id, request):
        """매우 긴 쿼리 텍스트 테스트

        Marengo 2.7: 최대 77 토큰, Marengo 3.0: 최대 500 토큰 제한
        토큰 제한을 초과하면 parameter_invalid 에러가 발생합니다.
        """
        long_query = "test " * 100  # 약 500자 (Marengo 2.7에서 제한 초과)
        index_name = get_index_name(request)

        if is_marengo30(index_name):
            # Marengo 3.0은 500 토큰까지 지원하므로, 이 쿼리는 통과해야 함
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
            # Marengo 2.7은 77 토큰 제한이 있으므로 BadRequestError 발생 예상
            with pytest.raises((ApiError, BadRequestError)) as exc_info:
                client.search.query(
                    index_id=index_id,
                    query_text=long_query,
                    search_options=["visual", "audio"],
                )

            # 에러 코드 확인
            error = exc_info.value
            error_code = get_error_code(error)

            print(
                f"\n[ERROR CODE] test_search_with_very_long_query_text (index: {index_name}): {error_code}"
            )

            # parameter_invalid 에러가 발생해야 함 (토큰 제한 초과)
            expected_code = "parameter_invalid"
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
    def test_search_without_query_text_or_media(self, client, index_id, request):
        """쿼리 텍스트와 미디어 모두 없는 경우 테스트

        쿼리 텍스트와 미디어가 모두 없으면 parameter_not_provided 에러가 발생합니다.
        """
        with pytest.raises((ApiError, BadRequestError)) as exc_info:
            client.search.query(index_id=index_id, search_options=["visual", "audio"])

        # 에러 코드 확인
        error = exc_info.value
        error_code = get_error_code(error)

        index_name = get_index_name(request)
        print(
            f"\n[ERROR CODE] test_search_without_query_text_or_media (index: {index_name}): {error_code}"
        )

        # parameter_not_provided 에러가 발생해야 함
        expected_code = "parameter_not_provided"
        assert (
            error_code == expected_code
        ), f"예상된 에러 코드: {expected_code}, 실제 발생한 에러 코드: {error_code}"
