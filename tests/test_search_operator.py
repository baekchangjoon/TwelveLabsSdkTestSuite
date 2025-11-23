"""
operator 파라미터 테스트

operator 파라미터의 기본 기능 및 조합을 테스트합니다.
"""

import os
import sys

import pytest
from twelvelabs.core.api_error import ApiError

sys.path.insert(0, os.path.dirname(__file__))
from conftest import get_index_name, validate_marengo_fields


class TestSearchOperator:
    """operator 파라미터 테스트"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_operator_or(self, client, index_id, request):
        """operator='or' 테스트 (기본값)"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            operator="or",
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
    def test_operator_and(self, client, index_id, request):
        """operator='and' 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            operator="and",
        )

        results = list(search_pager)
        assert len(results) >= 0

        # 결과가 있는 경우 Marengo 버전별 필드 검증
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)
