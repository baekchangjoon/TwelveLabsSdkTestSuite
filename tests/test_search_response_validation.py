"""
응답 유효성 검사 테스트

검색 응답의 구조와 데이터 타입, 값의 유효성을 검증합니다.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
from conftest import get_index_name, validate_marengo_fields


class TestSearchResponseValidation:
    """응답 유효성 검사 테스트"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_structure(self, client, index_id, request):
        """검색 응답 구조 검증"""
        search_pager = client.search.query(
            index_id=index_id, query_text="test", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        if len(results) > 0:
            item = results[0]
            index_name = get_index_name(request)

            # Marengo 버전별 필드 검증
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
        """rank 필드 검증 (Marengo 3.0)"""
        search_pager = client.search.query(
            index_id=index_id, query_text="test", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

            # rank가 있는 경우 추가 검증 (Marengo 3.0)
            ranks = [r.rank for r in results if r.rank is not None]
            if len(ranks) > 0:
                assert all(isinstance(r, int) for r in ranks), "rank는 정수여야 합니다"
                assert all(r > 0 for r in ranks), "rank는 1 이상이어야 합니다"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_with_thumbnail_url(self, client, index_id, request):
        """thumbnail_url 필드 검증"""
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
                    ), "thumbnail_url은 문자열이어야 합니다"
                    assert item.thumbnail_url.startswith(
                        "http"
                    ), "thumbnail_url은 URL 형식이어야 합니다"

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_search_response_time_range(self, client, index_id, request):
        """시간 범위 유효성 검증"""
        search_pager = client.search.query(
            index_id=index_id, query_text="test", search_options=["visual", "audio"]
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

        for item in results:
            if item.start is not None and item.end is not None:
                assert item.start >= 0, "start는 0 이상이어야 합니다"
                assert item.end > item.start, "end는 start보다 커야 합니다"
