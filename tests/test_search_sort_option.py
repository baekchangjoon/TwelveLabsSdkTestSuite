"""
sort_option parameter tests

Tests the basic functionality and combinations of the sort_option parameter.
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


class TestSearchSortOption:
    """sort_option parameter tests"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_sort_option_score(self, client, index_id, request):
        """Test sort_option='score'

        Documentation: "Sorts results by relevance ranking in ascending order (1 = most relevant)"
        """
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            sort_option="score",
        )

        results = list(search_pager)
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)

        if len(results) > 1:
            # Documentation: "Sorts results by relevance ranking in ascending order (1 = most relevant)"
            index_name = get_index_name(request)
            if is_marengo30(index_name):
                # Marengo 3.0: check ascending order by rank
                ranks = [r.rank for r in results if r.rank is not None]
                if len(ranks) > 1:
                    sorted_ranks = sorted(ranks)
                    assert ranks == sorted_ranks, (
                        f"Results should be sorted by rank in ascending order. "
                        f"Actual order: {ranks}, expected order: {sorted_ranks}"
                    )
            else:
                # Marengo 2.7: score is sorted in descending order (higher score = more relevant)
                scores = [r.score for r in results if r.score is not None]
                if len(scores) > 1:
                    sorted_scores = sorted(scores, reverse=True)
                    assert scores == sorted_scores, (
                        f"Results should be sorted by score in descending order. "
                        f"Actual order: {scores}, expected order: {sorted_scores}"
                    )

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_sort_option_score_with_group_by_video(self, client, index_id, request):
        """Test sort_option='score' with group_by='video' combination

        Documentation: when group_by='video', sort_option='score'
        sorts videos by the highest relevance ranking (lowest number) among their clips.
        """
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            group_by="video",
            sort_option="score",
        )

        results = list(search_pager)
        assert len(results) >= 0

        video_items = [item for item in results if item.id is not None]

        if len(video_items) > 0:
            index_name = get_index_name(request)

            # Documentation: "Clips within each video are sorted by relevance ranking in ascending order"
            # Verify sorting of clips within each video's clips array
            # - Marengo 2.7: score sorted in descending order (higher score = more relevant)
            # - Marengo 3.0: rank sorted in ascending order (lower rank = more relevant)
            for item in video_items:
                if item.clips:
                    validate_marengo_fields(item.clips[0], index_name, request)

                    if len(item.clips) > 1:
                        if is_marengo30(index_name):
                            # Marengo 3.0: verify ascending order by rank
                            ranks = [
                                clip.rank
                                for clip in item.clips
                                if clip.rank is not None
                            ]
                            if len(ranks) > 1:
                                sorted_ranks = sorted(ranks)
                                assert ranks == sorted_ranks, (
                                    f"Clips within video {item.id} should be sorted by rank in ascending order. "
                                    f"Actual order: {ranks}, expected order: {sorted_ranks}"
                                )
                        else:
                            # Marengo 2.7: verify descending order by score
                            scores = [
                                clip.score
                                for clip in item.clips
                                if clip.score is not None
                            ]
                            if len(scores) > 1:
                                sorted_scores = sorted(scores, reverse=True)
                                assert scores == sorted_scores, (
                                    f"Clips within video {item.id} should be sorted by score in descending order. "
                                    f"Actual order: {scores}, expected order: {sorted_scores}"
                                )

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_sort_option_clip_count_with_group_by_video(
        self, client, index_id, request
    ):
        """Test sort_option='clip_count' with group_by='video' combination

        Documentation:
        - "Sorts videos by the number of matching clips in descending order"
        - "Clips within each video are sorted by relevance ranking in ascending order"
        """
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            group_by="video",
            sort_option="clip_count",
        )

        results = list(search_pager)
        assert len(results) >= 0

        video_items = [item for item in results if item.id is not None]

        if len(video_items) > 0:
            index_name = get_index_name(request)

            # Documentation: "Sorts videos by the number of matching clips in descending order"
            clip_counts = [len(item.clips) if item.clips else 0 for item in video_items]
            if len(clip_counts) > 1:
                sorted_clip_counts = sorted(clip_counts, reverse=True)
                assert clip_counts == sorted_clip_counts, (
                    f"Videos should be sorted by number of clips in descending order. "
                    f"Actual order: {clip_counts}, expected order: {sorted_clip_counts}"
                )

            # Documentation: "Clips within each video are sorted by relevance ranking in ascending order"
            for item in video_items:
                if item.clips:
                    validate_marengo_fields(item.clips[0], index_name, request)

                    if len(item.clips) > 1:
                        if is_marengo30(index_name):
                            ranks = [
                                clip.rank
                                for clip in item.clips
                                if clip.rank is not None
                            ]
                            if len(ranks) > 1:
                                sorted_ranks = sorted(ranks)
                                assert ranks == sorted_ranks, (
                                    f"Clips within video {item.id} should be sorted by rank in ascending order. "
                                    f"Actual order: {ranks}, expected order: {sorted_ranks}"
                                )
                        else:
                            scores = [
                                clip.score
                                for clip in item.clips
                                if clip.score is not None
                            ]
                            if len(scores) > 1:
                                sorted_scores = sorted(scores, reverse=True)
                                assert scores == sorted_scores, (
                                    f"Clips within video {item.id} should be sorted by score in descending order. "
                                    f"Actual order: {scores}, expected order: {sorted_scores}"
                                )

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_sort_option_score_with_filter(self, client, index_id, request):
        """Test sort_option='score' with filter combination

        Documentation: sort_option='score' is "Sorts results by relevance ranking in ascending order (1 = most relevant)"
        """
        try:
            search_pager = client.search.query(
                index_id=index_id,
                query_text="test",
                search_options=["visual", "audio"],
                sort_option="score",
                filter='{"category": "nature"}',
            )

            results = list(search_pager)
            assert len(results) >= 0

            if len(results) > 0:
                index_name = get_index_name(request)
                validate_marengo_fields(results[0], index_name, request)

                # Documentation: "Sorts results by relevance ranking in ascending order (1 = most relevant)"
                if len(results) > 1:
                    if is_marengo30(index_name):
                        ranks = [r.rank for r in results if r.rank is not None]
                        if len(ranks) > 1:
                            sorted_ranks = sorted(ranks)
                            assert ranks == sorted_ranks, (
                                f"Results should be sorted by rank in ascending order. "
                                f"Actual order: {ranks}, expected order: {sorted_ranks}"
                            )
                    else:
                        scores = [r.score for r in results if r.score is not None]
                        if len(scores) > 1:
                            sorted_scores = sorted(scores, reverse=True)
                            assert scores == sorted_scores, (
                                f"Results should be sorted by score in descending order. "
                                f"Actual order: {scores}, expected order: {sorted_scores}"
                            )
        except ApiError as e:
            error_code = get_error_code(e)
            if (
                "invalid" in str(e).lower()
                or "not supported" in str(e).lower()
                or error_code == "search_filter_invalid"
            ):
                # Filter is not supported or invalid - skip this test
                pass
            raise

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_sort_option_clip_count_with_filter(self, client, index_id, request):
        """Test sort_option='clip_count' with filter combination (group_by='video' required)

        Documentation:
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
                filter='{"category": "nature"}',
            )

            results = list(search_pager)
            assert len(results) >= 0

            video_items = [item for item in results if item.id is not None]

            if len(video_items) > 0:
                index_name = get_index_name(request)

                clip_counts = [
                    len(item.clips) if item.clips else 0 for item in video_items
                ]
                if len(clip_counts) > 1:
                    sorted_clip_counts = sorted(clip_counts, reverse=True)
                    assert clip_counts == sorted_clip_counts, (
                        f"Videos should be sorted by number of clips in descending order. "
                        f"Actual order: {clip_counts}, expected order: {sorted_clip_counts}"
                    )

                for item in video_items:
                    if item.clips:
                        validate_marengo_fields(item.clips[0], index_name, request)

                        if len(item.clips) > 1:
                            if is_marengo30(index_name):
                                ranks = [
                                    clip.rank
                                    for clip in item.clips
                                    if clip.rank is not None
                                ]
                                if len(ranks) > 1:
                                    sorted_ranks = sorted(ranks)
                                    assert ranks == sorted_ranks, (
                                        f"Clips within video {item.id} should be sorted by rank in ascending order. "
                                        f"Actual order: {ranks}, expected order: {sorted_ranks}"
                                    )
                            else:
                                scores = [
                                    clip.score
                                    for clip in item.clips
                                    if clip.score is not None
                                ]
                                if len(scores) > 1:
                                    sorted_scores = sorted(scores, reverse=True)
                                    assert scores == sorted_scores, (
                                        f"Clips within video {item.id} should be sorted by score in descending order. "
                                        f"Actual order: {scores}, expected order: {sorted_scores}"
                                    )
        except ApiError as e:
            error_code = get_error_code(e)
            if (
                "invalid" in str(e).lower()
                or "not supported" in str(e).lower()
                or error_code == "search_filter_invalid"
            ):
                # Filter is not supported or invalid - skip this test
                pass
            raise
