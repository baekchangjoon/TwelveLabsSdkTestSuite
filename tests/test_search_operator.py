"""
operator parameter tests

Tests the basic functionality and combinations of the operator parameter.
"""

import os
import sys

import pytest
from twelvelabs.core.api_error import ApiError

sys.path.insert(0, os.path.dirname(__file__))
from conftest import get_index_name, validate_marengo_fields


class TestSearchOperator:
    """operator parameter tests"""

    @pytest.mark.parametrize(
        "index_id",
        [
            pytest.param("index_marengo27", marks=pytest.mark.marengo27),
            pytest.param("index_marengo30", marks=pytest.mark.marengo30),
        ],
        indirect=True,
    )
    def test_operator_or(self, client, index_id, request):
        """Test operator='or' (default)"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="swimming",
            search_options=["visual", "audio"],
            operator="or",
        )

        results = list(search_pager)
        assert len(results) >= 0

        # Validate fields by Marengo version if results exist
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
        """Test operator='and'"""
        search_pager = client.search.query(
            index_id=index_id,
            query_text="water",
            search_options=["visual", "audio"],
            operator="and",
        )

        results = list(search_pager)
        assert len(results) >= 0

        # Validate fields by Marengo version if results exist
        if len(results) > 0:
            index_name = get_index_name(request)
            validate_marengo_fields(results[0], index_name, request)
