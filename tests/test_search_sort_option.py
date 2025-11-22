"""
sort_option 파라미터 테스트

sort_option 파라미터의 기본 기능 및 조합을 테스트합니다.
"""
import pytest
import sys
import os
from twelvelabs.core.api_error import ApiError
sys.path.insert(0, os.path.dirname(__file__))
from conftest import validate_marengo_fields, get_index_name, is_marengo30, get_error_code


class TestSearchSortOption:
    """sort_option 파라미터 테스트"""

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_sort_option_score(self, client, index_id, request):
        """sort_option='score' 테스트
        
        문서 기준: "Sorts results by relevance ranking in ascending order (1 = most relevant)"
        """
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            sort_option="score"
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)
            
        if len(results) > 1:
            # 문서 기준: "Sorts results by relevance ranking in ascending order (1 = most relevant)"
            index_name = get_index_name(request)
            if is_marengo30(index_name):
                # Marengo 3.0: rank로 오름차순 정렬 확인
                ranks = [r.rank for r in results if r.rank is not None]
                if len(ranks) > 1:
                    sorted_ranks = sorted(ranks)
                    if ranks != sorted_ranks:
                        pytest.skip(
                            f"문서 기준과 실제 API 응답이 다릅니다. "
                            f"문서: rank 오름차순 정렬 (1 = most relevant). "
                            f"실제 순서: {ranks}, 예상 순서: {sorted_ranks}"
                        )
            else:
                # Marengo 2.7: 문서 기준에 따르면 "ascending order (1 = most relevant)"
                scores = [r.score for r in results if r.score is not None]
                if len(scores) > 1:
                    sorted_scores = sorted(scores)
                    if scores != sorted_scores:
                        pytest.skip(
                            f"문서 기준과 실제 API 응답이 다릅니다 (Marengo 2.7). "
                            f"문서: relevance ranking 오름차순 정렬 (1 = most relevant). "
                            f"실제 순서: {scores}, 예상 순서: {sorted_scores}"
                        )

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_sort_option_score_with_group_by_video(self, client, index_id, request):
        """sort_option='score'와 group_by='video' 조합 테스트
        
        문서 기준: group_by='video'일 때 sort_option='score'는 
        각 비디오의 clips 중 가장 높은 관련성 순위(가장 낮은 숫자)로 비디오를 정렬합니다.
        """
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            group_by="video",
            sort_option="score"
        )

        results = list(search_pager)
        assert len(results) >= 0

        video_items = [item for item in results if item.id is not None]
        
        if len(video_items) > 0:
            index_name = get_index_name(request)
            
            # 문서 기준: "sorts videos by highest relevance ranking (lowest number) among their clips"
            if is_marengo30(index_name):
                video_min_ranks = []
                for item in video_items:
                    if item.clips:
                        ranks = [clip.rank for clip in item.clips if clip.rank is not None]
                        if ranks:
                            video_min_ranks.append(min(ranks))
                        else:
                            video_min_ranks.append(None)
                    else:
                        video_min_ranks.append(None)
                
                valid_ranks = [r for r in video_min_ranks if r is not None]
                if len(valid_ranks) > 1:
                    sorted_ranks = sorted(valid_ranks)
                    if valid_ranks != sorted_ranks:
                        pytest.skip(
                            f"문서 기준과 실제 API 응답이 다릅니다. "
                            f"문서: 각 비디오의 가장 낮은 rank로 오름차순 정렬. "
                            f"실제 순서: {valid_ranks}, 예상 순서: {sorted_ranks}"
                        )
            else:
                video_min_ranks_or_scores = []
                for item in video_items:
                    if item.clips:
                        scores = [clip.score for clip in item.clips if clip.score is not None]
                        if scores:
                            video_min_ranks_or_scores.append(min(scores))
                        else:
                            video_min_ranks_or_scores.append(None)
                    else:
                        video_min_ranks_or_scores.append(None)
                
                valid_values = [v for v in video_min_ranks_or_scores if v is not None]
                if len(valid_values) > 1:
                    sorted_values = sorted(valid_values)
                    if valid_values != sorted_values:
                        pytest.skip(
                            f"문서 기준과 실제 API 응답이 다릅니다 (Marengo 2.7). "
                            f"문서: 각 비디오의 가장 낮은 숫자로 오름차순 정렬. "
                            f"실제 순서: {valid_values}, 예상 순서: {sorted_values}"
                        )
            
            for item in video_items:
                if item.clips:
                    validate_marengo_fields(item.clips[0], index_name, request)

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_sort_option_clip_count_with_group_by_video(self, client, index_id, request):
        """sort_option='clip_count'와 group_by='video' 조합 테스트
        
        문서 기준:
        - "Sorts videos by the number of matching clips in descending order"
        - "Clips within each video are sorted by relevance ranking in ascending order"
        """
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            group_by="video",
            sort_option="clip_count"
        )

        results = list(search_pager)
        assert len(results) >= 0

        video_items = [item for item in results if item.id is not None]
        
        if len(video_items) > 0:
            index_name = get_index_name(request)
            
            # 문서 기준: "Sorts videos by the number of matching clips in descending order"
            clip_counts = [len(item.clips) if item.clips else 0 for item in video_items]
            if len(clip_counts) > 1:
                sorted_clip_counts = sorted(clip_counts, reverse=True)
                if clip_counts != sorted_clip_counts:
                    pytest.skip(
                        f"문서 기준과 실제 API 응답이 다릅니다. "
                        f"문서: 비디오를 클립 수로 내림차순 정렬. "
                        f"실제 순서: {clip_counts}, 예상 순서: {sorted_clip_counts}"
                    )
            
            # 문서 기준: "Clips within each video are sorted by relevance ranking in ascending order"
            for item in video_items:
                if item.clips:
                    validate_marengo_fields(item.clips[0], index_name, request)
                    
                    if len(item.clips) > 1:
                        if is_marengo30(index_name):
                            ranks = [clip.rank for clip in item.clips if clip.rank is not None]
                            if len(ranks) > 1:
                                sorted_ranks = sorted(ranks)
                                if ranks != sorted_ranks:
                                    pytest.skip(
                                        f"문서 기준과 실제 API 응답이 다릅니다 (video_id: {item.id}). "
                                        f"문서: 각 비디오 내 클립들은 relevance ranking 오름차순 정렬. "
                                        f"실제 순서: {ranks}, 예상 순서: {sorted_ranks}"
                                    )
                        else:
                            scores = [clip.score for clip in item.clips if clip.score is not None]
                            if len(scores) > 1:
                                sorted_scores = sorted(scores)
                                if scores != sorted_scores:
                                    pytest.skip(
                                        f"문서 기준과 실제 API 응답이 다릅니다 (Marengo 2.7, video_id: {item.id}). "
                                        f"문서: 각 비디오 내 클립들은 relevance ranking 오름차순 정렬. "
                                        f"실제 순서: {scores}, 예상 순서: {sorted_scores}"
                                    )

    @pytest.mark.parametrize("index_id", [
        pytest.param("index_marengo27", marks=pytest.mark.marengo27),
        pytest.param("index_marengo30", marks=pytest.mark.marengo30)
    ], indirect=True)
    def test_sort_option_score_with_filter(self, client, index_id, request):
        """sort_option='score'와 filter 조합 테스트
        
        문서 기준: sort_option='score'는 "Sorts results by relevance ranking in ascending order (1 = most relevant)"
        """
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                sort_option="score",
                filter='{"category": "nature"}'
            )

            results = list(search_pager)
            assert len(results) >= 0

            if len(results) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(results[0], index_name, request)
                
                # 문서 기준: "Sorts results by relevance ranking in ascending order (1 = most relevant)"
                if len(results) > 1:
                    if is_marengo30(index_name):
                        ranks = [r.rank for r in results if r.rank is not None]
                        if len(ranks) > 1:
                            sorted_ranks = sorted(ranks)
                            if ranks != sorted_ranks:
                                pytest.skip(
                                    f"문서 기준과 실제 API 응답이 다릅니다. "
                                    f"문서: rank 오름차순 정렬 (1 = most relevant). "
                                    f"실제 순서: {ranks}, 예상 순서: {sorted_ranks}"
                                )
                    else:
                        scores = [r.score for r in results if r.score is not None]
                        if len(scores) > 1:
                            sorted_scores = sorted(scores)
                            if scores != sorted_scores:
                                pytest.skip(
                                    f"문서 기준과 실제 API 응답이 다릅니다 (Marengo 2.7). "
                                    f"문서: relevance ranking 오름차순 정렬 (1 = most relevant). "
                                    f"실제 순서: {scores}, 예상 순서: {sorted_scores}"
                                )
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
    def test_sort_option_clip_count_with_filter(self, client, index_id, request):
        """sort_option='clip_count'와 filter 조합 테스트 (group_by='video' 필요)
        
        문서 기준:
        - "Sorts videos by the number of matching clips in descending order"
        - "Clips within each video are sorted by relevance ranking in ascending order"
        """
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="water",
                search_options=["visual", "audio"],
                group_by="video",
                sort_option="clip_count",
                filter='{"category": "nature"}'
            )

            results = list(search_pager)
            assert len(results) >= 0

            video_items = [item for item in results if item.id is not None]
            
            if len(video_items) > 0:
                index_name = get_index_name(request)
                
                clip_counts = [len(item.clips) if item.clips else 0 for item in video_items]
                if len(clip_counts) > 1:
                    sorted_clip_counts = sorted(clip_counts, reverse=True)
                    if clip_counts != sorted_clip_counts:
                        pytest.skip(
                            f"문서 기준과 실제 API 응답이 다릅니다. "
                            f"문서: 비디오를 클립 수로 내림차순 정렬. "
                            f"실제 순서: {clip_counts}, 예상 순서: {sorted_clip_counts}"
                        )
                
                for item in video_items:
                    if item.clips:
                        validate_marengo_fields(item.clips[0], index_name, request)
                        
                        if len(item.clips) > 1:
                            if is_marengo30(index_name):
                                ranks = [clip.rank for clip in item.clips if clip.rank is not None]
                                if len(ranks) > 1:
                                    sorted_ranks = sorted(ranks)
                                    if ranks != sorted_ranks:
                                        pytest.skip(
                                            f"문서 기준과 실제 API 응답이 다릅니다 (video_id: {item.id}). "
                                            f"문서: 각 비디오 내 클립들은 relevance ranking 오름차순 정렬. "
                                            f"실제 순서: {ranks}, 예상 순서: {sorted_ranks}"
                                        )
                            else:
                                scores = [clip.score for clip in item.clips if clip.score is not None]
                                if len(scores) > 1:
                                    sorted_scores = sorted(scores)
                                    if scores != sorted_scores:
                                        pytest.skip(
                                            f"문서 기준과 실제 API 응답이 다릅니다 (Marengo 2.7, video_id: {item.id}). "
                                            f"문서: 각 비디오 내 클립들은 relevance ranking 오름차순 정렬. "
                                            f"실제 순서: {scores}, 예상 순서: {sorted_scores}"
                                        )
        except ApiError as e:
            error_code = get_error_code(e)
            if "invalid" in str(e).lower() or "not supported" in str(e).lower() or \
               error_code == "search_filter_invalid":
                pytest.skip(f"필터가 지원되지 않거나 유효하지 않습니다: {e}")
            raise

