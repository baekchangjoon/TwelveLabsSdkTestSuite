"""
page_limit 파라미터 테스트

page_limit 파라미터의 기본 기능 및 조합을 테스트합니다.
"""

import os
import sys

import pytest
from twelvelabs.core.api_error import ApiError

sys.path.insert(0, os.path.dirname(__file__))
from conftest import get_index_name, validate_marengo_fields


class TestSearchPageLimit:
    """page_limit 파라미터 테스트"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_page_limit(self, client, index_id, request):
        """page_limit 파라미터 테스트"""
        page_limit = 5
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=page_limit,
        )

        # 첫 페이지의 결과 수 확인
        first_page_items = search_pager.items
        if first_page_items:
            assert (
                len(first_page_items) <= page_limit
            ), f"첫 페이지 결과는 {page_limit}개 이하여야 합니다"
            # 첫 번째 결과 검증
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
        """page_limit 최대값(50) 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=50,
        )

        first_page_items = search_pager.items
        if first_page_items:
            assert len(first_page_items) <= 50, "최대 50개까지 반환됩니다"
            # 첫 번째 결과 검증
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
        """최소 page_limit 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=1,
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
    def test_page_limit_various_values(self, client, index_id, request):
        """다양한 page_limit 값 테스트"""
        for page_limit in [1, 5, 10, 25, 50]:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                page_limit=page_limit,
            )

            # 첫 페이지의 결과 수 확인
            first_page_items = search_pager.items
            if first_page_items:
                assert (
                    len(first_page_items) <= page_limit
                ), f"첫 페이지 결과는 {page_limit}개 이하여야 합니다"
                # 첫 번째 결과 검증
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
        """페이지네이션 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=2,
        )

        # 첫 페이지 확인
        first_page = list(search_pager.items) if search_pager.items else []
        assert len(first_page) >= 0

        # 첫 페이지 결과 검증
        if len(first_page) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(first_page[0], index_name, request)

        # 다음 페이지가 있는 경우 확인
        if search_pager.has_next:
            next_page_pager = search_pager.next_page()
            if next_page_pager:
                next_page = list(next_page_pager.items) if next_page_pager.items else []
                assert len(next_page) >= 0
                # 다음 페이지 결과도 검증
                if len(next_page) > 0:
                    index_name = get_index_name(request)
                    validate_marengo_fields(next_page[0], index_name, request)
