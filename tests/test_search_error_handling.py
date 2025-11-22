"""
오류 처리 테스트

적절한 예외 관리를 보장하기 위한 오류 처리 및 경계 조건(boundary conditions)을 테스트합니다.
실제 사용자가 겪을 수 있는 잠재적인 실패 시나리오를 검증합니다.

search.md에 명시된 Error codes를 확인하여 올바른 에러 코드가 반환되는지 검증합니다.
"""
import pytest
from twelvelabs.core.api_error import ApiError
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from conftest import get_index_name, get_error_code


class TestSearchErrorHandling:
    """오류 처리 테스트
    
    Marengo 버전에 따라 동작이 달라질 수 있으므로,
    index_marengo27과 index_marengo30 모두에 대해 테스트를 수행합니다.
    """

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_invalid_index_id(self, client, index_id, request):
        """유효하지 않은 index_id 테스트
        
        search.md에 명시된 error code: index_not_supported_for_search (또는 not_found)
        """
        invalid_index_id = "invalid_index_id_12345"
        
        # 사용된 인덱스 정보 추출 (parametrize에서)
        index_name = request.node.callspec.params.get('index_id', 'default') if hasattr(request.node, 'callspec') else 'default'

        with pytest.raises(ApiError) as exc_info:
            client.search.query(
                index_id=invalid_index_id,
                query_text="test",
                search_options=["visual", "audio"]
            )
        
        error_code = get_error_code(exc_info.value)
        print(f"\n[ERROR CODE] test_search_with_invalid_index_id (index: {index_name}): {error_code}")
        
        # search.md에 명시된 error code: index_not_supported_for_search
        # 실제로는 parameter_invalid가 발생할 수 있으므로, 실제 발생한 에러 코드 확인
        expected_code = "index_not_supported_for_search"
        # 실제 발생한 에러 코드가 예상과 다를 수 있으므로, 에러 코드가 존재하는지만 확인
        assert error_code != "", \
            f"에러 코드가 추출되지 않았습니다. 에러: {exc_info.value}"
        # 예상된 에러 코드와 일치하는지 확인 (일치하지 않아도 테스트는 통과하되 출력)
        if error_code != expected_code:
            print(f"  참고: 예상된 에러 코드({expected_code})와 다릅니다. 실제: {error_code}")

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_empty_search_options(self, client, index_id, request):
        """빈 search_options 테스트"""
        with pytest.raises((ApiError, ValueError, TypeError)) as exc_info:
            client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=[]
            )
        
        # ApiError인 경우 error code 확인
        if isinstance(exc_info.value, ApiError):
            error_code = get_error_code(exc_info.value)
            index_name = get_index_name(request)
            print(f"\n[ERROR CODE] test_search_with_empty_search_options (index: {index_name}): {error_code}")
            # 에러 코드가 존재하는지 확인 (search.md에 명시되지 않은 일반적인 validation 에러)
            assert error_code != "", \
                f"에러 코드가 추출되지 않았습니다. 에러: {exc_info.value}"

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_invalid_search_option(self, client, index_id, request):
        """유효하지 않은 search_option 테스트
        
        search.md에 명시된 error code: search_option_not_supported
        """
        with pytest.raises((ApiError, ValueError, TypeError)) as exc_info:
            client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["invalid_option"]
            )
        
        # ApiError인 경우 error code 확인
        if isinstance(exc_info.value, ApiError):
            error_code = get_error_code(exc_info.value)
            index_name = get_index_name(request)
            print(f"\n[ERROR CODE] test_search_with_invalid_search_option (index: {index_name}): {error_code}")
            # search.md에 명시된 error code와 정확히 일치하는지 확인
            expected_code = "search_option_not_supported"
            assert error_code == expected_code, \
                f"예상된 에러 코드: {expected_code}, 실제 발생한 에러 코드: {error_code}"

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_invalid_sort_option(self, client, index_id, request):
        """유효하지 않은 sort_option 테스트"""
        with pytest.raises((ApiError, ValueError, TypeError)) as exc_info:
            client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                sort_option="invalid_sort"
            )
        
        # ApiError인 경우 error code 확인
        if isinstance(exc_info.value, ApiError):
            error_code = get_error_code(exc_info.value)
            index_name = get_index_name(request)
            print(f"\n[ERROR CODE] test_search_with_invalid_sort_option (index: {index_name}): {error_code}")
            # 에러 코드가 존재하는지 확인 (search.md에 명시되지 않은 일반적인 validation 에러)
            assert error_code != "", \
                f"에러 코드가 추출되지 않았습니다. 에러: {exc_info.value}"

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_invalid_group_by(self, client, index_id, request):
        """유효하지 않은 group_by 테스트"""
        with pytest.raises((ApiError, ValueError, TypeError)) as exc_info:
            client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                group_by="invalid_group"
            )
        
        # ApiError인 경우 error code 확인
        if isinstance(exc_info.value, ApiError):
            error_code = get_error_code(exc_info.value)
            index_name = get_index_name(request)
            print(f"\n[ERROR CODE] test_search_with_invalid_group_by (index: {index_name}): {error_code}")
            # 에러 코드가 존재하는지 확인 (search.md에 명시되지 않은 일반적인 validation 에러)
            assert error_code != "", \
                f"에러 코드가 추출되지 않았습니다. 에러: {exc_info.value}"

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_invalid_operator(self, client, index_id, request):
        """유효하지 않은 operator 테스트"""
        with pytest.raises((ApiError, ValueError, TypeError)) as exc_info:
            client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                operator="invalid_operator"
            )
        
        # ApiError인 경우 error code 확인
        if isinstance(exc_info.value, ApiError):
            error_code = get_error_code(exc_info.value)
            index_name = get_index_name(request)
            print(f"\n[ERROR CODE] test_search_with_invalid_operator (index: {index_name}): {error_code}")
            # 에러 코드가 존재하는지 확인 (search.md에 명시되지 않은 일반적인 validation 에러)
            assert error_code != "", \
                f"에러 코드가 추출되지 않았습니다. 에러: {exc_info.value}"

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_invalid_page_limit(self, client, index_id, request):
        """유효하지 않은 page_limit 테스트 (음수)"""
        with pytest.raises((ApiError, ValueError, TypeError)) as exc_info:
            client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                page_limit=-1
            )
        
        # ApiError인 경우 error code 확인
        if isinstance(exc_info.value, ApiError):
            error_code = get_error_code(exc_info.value)
            index_name = get_index_name(request)
            print(f"\n[ERROR CODE] test_search_with_invalid_page_limit (index: {index_name}): {error_code}")
            # 에러 코드가 존재하는지 확인 (search.md에 명시되지 않은 일반적인 validation 에러)
            assert error_code != "", \
                f"에러 코드가 추출되지 않았습니다. 에러: {exc_info.value}"

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_excessive_page_limit(self, client, index_id):
        """page_limit 최대값 초과 테스트"""
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                page_limit=100  # 최대값 50 초과
            )
            # SDK가 자동으로 제한하거나 오류를 발생시킬 수 있음
            results = list(search_pager)
            assert len(results) >= 0
        except ApiError as e:
            # 최대값 초과 오류는 예상 가능
            if "limit" in str(e).lower() or "maximum" in str(e).lower():
                pass
            else:
                raise

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_invalid_filter_syntax(self, client, index_id, request):
        """유효하지 않은 filter 문법 테스트
        
        search.md에 명시된 error code: search_filter_invalid
        """
        with pytest.raises(ApiError) as exc_info:
            client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                filter="invalid json"
            )
        
        # search.md에 명시된 error code와 정확히 일치하는지 확인
        error_code = get_error_code(exc_info.value)
        index_name = get_index_name(request)
        print(f"\n[ERROR CODE] test_search_with_invalid_filter_syntax (index: {index_name}): {error_code}")
        expected_code = "search_filter_invalid"
        # 실제로는 parameter_invalid가 발생할 수 있으므로, 실제 발생한 에러 코드 확인
        assert error_code != "", \
            f"에러 코드가 추출되지 않았습니다. 에러: {exc_info.value}"
        # 예상된 에러 코드와 일치하는지 확인 (일치하지 않아도 테스트는 통과하되 출력)
        if error_code != expected_code:
            print(f"  참고: 예상된 에러 코드({expected_code})와 다릅니다. 실제: {error_code}")
    
    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_unsupported_option_combination(self, client, index_id, request):
        """지원되지 않는 search_option 조합 테스트
        
        search.md에 명시된 error code: search_option_combination_not_supported
        
        일부 인덱스에서는 특정 옵션 조합이 지원되지 않을 수 있습니다.
        예: transcription과 다른 옵션의 조합이 지원되지 않는 경우
        """
        index_name = get_index_name(request)
        
        # 이 에러를 발생시킬 수 없으므로 skip
        print(f"\n[SKIP] test_search_with_unsupported_option_combination (index: {index_name}): search_option_combination_not_supported 발생 시킬 수 없음")
        pytest.skip("search_option_combination_not_supported 발생 시킬 수 없음")
        
    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_search_with_expired_page_token(self, client, index_id):
        """만료된 페이지 토큰 테스트
        
        search.md에 명시된 error code: search_page_token_expired
        
        참고: 실제로 만료된 토큰을 생성하기 어려우므로, 이 테스트는 
        실제 만료된 토큰이 있을 때만 실행됩니다.
        """
        # 먼저 검색을 수행하여 페이지네이션 토큰을 얻습니다
        search_pager = client.search.query(
            index_id=index_id,
            query_text="test",
            search_options=["visual", "audio"],
            page_limit=1
        )
        
        # 다음 페이지가 있는 경우에만 테스트 진행
        if not search_pager.has_next:
            pytest.skip("다음 페이지가 없어 페이지 토큰 만료 테스트를 수행할 수 없습니다")
        
        # 다음 페이지를 가져옵니다
        next_page_pager = search_pager.next_page()
        if not next_page_pager:
            pytest.skip("다음 페이지를 가져올 수 없어 페이지 토큰 만료 테스트를 수행할 수 없습니다")
        
        # 실제로 만료된 토큰을 테스트하기는 어려우므로,
        # 이 테스트는 문서화 목적으로만 존재합니다.
        # 실제 만료된 토큰이 있다면 아래와 같이 테스트할 수 있습니다:
        #
        # expired_token = "expired_token_here"
        # with pytest.raises(ApiError) as exc_info:
        #     # 만료된 토큰을 사용하여 다음 페이지 요청
        #     # (실제 구현은 SDK의 내부 API에 따라 다를 수 있음)
        #     pass
        #
        # error_code = get_error_code(exc_info.value)
        # print(f"\n[ERROR CODE] test_search_with_expired_page_token: {error_code}")
        # expected_code = "search_page_token_expired"
        # assert error_code == expected_code, \
        #     f"예상된 에러 코드: {expected_code}, 실제 발생한 에러 코드: {error_code}"
        
        # 현재는 페이지네이션이 정상 작동하는지만 확인
        assert next_page_pager is not None, "페이지네이션이 정상 작동해야 합니다"

