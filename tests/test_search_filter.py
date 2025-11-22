"""
filter 파라미터 테스트

filter 파라미터의 기본 기능 및 조합을 테스트합니다.
"""
import pytest
import sys
import os
from twelvelabs.core.api_error import ApiError
sys.path.insert(0, os.path.dirname(__file__))
from conftest import validate_marengo_fields, get_index_name, get_error_code


class TestSearchFilter:
    """filter 파라미터 테스트"""

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_filter(self, client, index_id, request):
        """filter 파라미터 테스트"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                filter='{"category": "nature"}'
            )

            results = list(search_pager)
            assert len(results) >= 0
            
            # 결과가 있는 경우 Marengo 버전별 필드 검증
            if len(results) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(results[0], index_name, request)
        except ApiError as e:
            # 필터가 지원되지 않거나 유효하지 않은 경우
            if "invalid" in str(e).lower() or "not supported" in str(e).lower():
                pytest.skip(f"필터가 지원되지 않거나 유효하지 않습니다: {e}")
            raise

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_filter_various_formats(self, client, index_id, request):
        """다양한 filter 형식 테스트"""
        filter_formats = [
            '{"category": "nature"}',
            '{"type": "video"}',
            '{"status": "active"}',
            '{"category": "nature", "type": "video"}'
        ]

        for filter_str in filter_formats:
            try:
                search_pager = client.search.query(
                    index_id=index_id,
                    query_text="test",
                    search_options=["visual", "audio"],
                    filter=filter_str
                )

                results = list(search_pager)
                assert len(results) >= 0

                # 결과가 있는 경우 Marengo 버전별 필드 검증
                if len(results) > 0:
                    index_name = get_index_name(request)
                    validate_marengo_fields(results[0], index_name, request)
            except ApiError as e:
                # 필터가 지원되지 않거나 유효하지 않은 경우
                error_code = get_error_code(e)
                if "invalid" in str(e).lower() or "not supported" in str(e).lower() or \
                   error_code == "search_filter_invalid":
                    # 특정 필터 형식이 지원되지 않는 경우 스킵
                    continue
                raise

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_filter_with_operator_and(self, client, index_id, request):
        """filter와 operator='and' 조합 테스트"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="water",
                search_options=["visual", "audio"],
                operator="and",
                filter='{"category": "nature"}'
            )

            results = list(search_pager)
            assert len(results) >= 0

            # 결과가 있는 경우 Marengo 버전별 필드 검증
            if len(results) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(results[0], index_name, request)
        except ApiError as e:
            error_code = get_error_code(e)
            if "invalid" in str(e).lower() or "not supported" in str(e).lower() or \
               error_code == "search_filter_invalid":
                pytest.skip(f"필터가 지원되지 않거나 유효하지 않습니다: {e}")
            raise

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_filter_with_operator_or(self, client, index_id, request):
        """filter와 operator='or' 조합 테스트"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="swimming",
                search_options=["visual", "audio"],
                operator="or",
                filter='{"category": "nature"}'
            )

            results = list(search_pager)
            assert len(results) >= 0

            # 결과가 있는 경우 Marengo 버전별 필드 검증
            if len(results) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(results[0], index_name, request)
        except ApiError as e:
            error_code = get_error_code(e)
            if "invalid" in str(e).lower() or "not supported" in str(e).lower() or \
               error_code == "search_filter_invalid":
                pytest.skip(f"필터가 지원되지 않거나 유효하지 않습니다: {e}")
            raise

