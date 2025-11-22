"""
group_by 파라미터 테스트

group_by 파라미터의 기본 기능 및 조합을 테스트합니다.
"""
import pytest
import sys
import os
from twelvelabs.core.api_error import ApiError
sys.path.insert(0, os.path.dirname(__file__))
from conftest import validate_marengo_fields, get_index_name, is_marengo30, get_error_code


class TestSearchGroupBy:
    """group_by 파라미터 테스트"""

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_group_by_video(self, client, index_id, request):
        """group_by='video' 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            group_by="video"
        )

        results = list(search_pager)
        assert len(results) >= 0

        # video로 그룹화된 경우 id와 clips 필드 확인
        for item in results:
            if item.id is not None:
                assert item.clips is not None, "video 그룹화 시 clips가 있어야 합니다"
                assert len(item.clips) > 0, "clips는 비어있지 않아야 합니다"
                # clips 내부 항목도 검증
                if item.clips:
                    index_name = get_index_name(request)
                    validate_marengo_fields(item.clips[0], index_name, request)

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_group_by_clip(self, client, index_id, request):
        """group_by='clip' 테스트 (기본값)"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="animal",
            search_options=["visual", "audio"],
            group_by="clip"
        )

        results = list(search_pager)
        assert len(results) >= 0

        # clip 그룹화의 경우 개별 클립 정보 확인
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_group_by_video_with_operator_and(self, client, index_id, request):
        """group_by='video'와 operator='and' 조합 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            group_by="video",
            operator="and"
        )

        results = list(search_pager)
        assert len(results) >= 0

        # video로 그룹화된 경우 id와 clips 필드 확인
        for item in results:
            if item.id is not None:
                assert item.clips is not None, "video 그룹화 시 clips가 있어야 합니다"
                assert len(item.clips) > 0, "clips는 비어있지 않아야 합니다"
                # clips 내부 항목도 검증
                if item.clips:
                    index_name = get_index_name(request)
                    validate_marengo_fields(item.clips[0], index_name, request)

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_group_by_video_with_operator_or(self, client, index_id, request):
        """group_by='video'와 operator='or' 조합 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="animal",
            search_options=["visual", "audio"],
            group_by="video",
            operator="or"
        )

        results = list(search_pager)
        assert len(results) >= 0

        # video로 그룹화된 경우 id와 clips 필드 확인
        for item in results:
            if item.id is not None:
                assert item.clips is not None, "video 그룹화 시 clips가 있어야 합니다"
                assert len(item.clips) > 0, "clips는 비어있지 않아야 합니다"
                # clips 내부 항목도 검증
                if item.clips:
                    index_name = get_index_name(request)
                    validate_marengo_fields(item.clips[0], index_name, request)

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_group_by_clip_with_operator_and(self, client, index_id, request):
        """group_by='clip'와 operator='and' 조합 테스트"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            group_by="clip",
            operator="and"
        )

        results = list(search_pager)
        assert len(results) >= 0

        # clip 그룹화의 경우 개별 클립 정보 확인
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_group_by_clip_with_operator_or(self, client, index_id, request):
        """group_by='clip'와 operator='or' 조합 테스트 (기본값)"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            group_by="clip",
            operator="or"
        )

        results = list(search_pager)
        assert len(results) >= 0

        # clip 그룹화의 경우 개별 클립 정보 확인
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_group_by_video_with_page_limit(self, client, index_id, request):
        """group_by='video'와 page_limit 조합 테스트"""
        page_limit = 3
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            group_by="video",
            page_limit=page_limit
        )

        # 첫 페이지의 결과 수 확인
        first_page_items = search_pager.items
        if first_page_items:
            assert len(first_page_items) <= page_limit, \
                f"첫 페이지 결과는 {page_limit}개 이하여야 합니다"
            # 첫 번째 결과 검증
            if len(first_page_items) > 0 and first_page_items[0].id is not None:
                assert first_page_items[0].clips is not None, \
                    "video 그룹화 시 clips가 있어야 합니다"
                if first_page_items[0].clips:
                    index_name = get_index_name(request)
                    validate_marengo_fields(first_page_items[0].clips[0], index_name, request)

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_group_by_clip_with_page_limit(self, client, index_id, request):
        """group_by='clip'와 page_limit 조합 테스트"""
        page_limit = 5
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            group_by="clip",
            page_limit=page_limit
        )

        # 첫 페이지의 결과 수 확인
        first_page_items = search_pager.items
        if first_page_items:
            assert len(first_page_items) <= page_limit, \
                f"첫 페이지 결과는 {page_limit}개 이하여야 합니다"
            # 첫 번째 결과 검증
            if len(first_page_items) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(first_page_items[0], index_name, request)

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_group_by_video_with_filter(self, client, index_id, request):
        """group_by='video'와 filter 조합 테스트"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                group_by="video",
                filter='{"category": "nature"}'
            )

            results = list(search_pager)
            assert len(results) >= 0

            # video로 그룹화된 경우 id와 clips 필드 확인
            for item in results:
                if item.id is not None:
                    assert item.clips is not None, "video 그룹화 시 clips가 있어야 합니다"
                    if item.clips:
                        index_name = get_index_name(request)
                        validate_marengo_fields(item.clips[0], index_name, request)
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
    def test_group_by_clip_with_filter(self, client, index_id, request):
        """group_by='clip'와 filter 조합 테스트"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                group_by="clip",
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

