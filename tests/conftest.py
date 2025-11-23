"""
pytest 설정 및 공통 fixture 정의
"""

import json
import os

import pytest
from twelvelabs import TwelveLabs
from twelvelabs.core.api_error import ApiError


def _load_env_file():
    """config.env 파일에서 환경 변수를 로드합니다."""
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 주석과 빈 줄 건너뛰기
                if not line or line.startswith("#"):
                    continue
                # KEY=VALUE 형식 파싱
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    # 환경 변수가 이미 설정되어 있지 않은 경우에만 설정
                    if key and value and key not in os.environ:
                        os.environ[key] = value


# pytest 시작 시 환경 변수 파일 로드
_load_env_file()


@pytest.fixture(scope="session")
def api_key():
    """API 키를 환경 변수 또는 config.env 파일에서 가져옵니다."""
    api_key = os.getenv("TL_API_KEY")
    if not api_key:
        raise ValueError(
            "TL_API_KEY 환경 변수가 설정되지 않았습니다. config.env 파일을 확인하거나 환경 변수를 설정하세요."
        )
    return api_key


@pytest.fixture(scope="function")
def index_id(request):
    """인덱스 ID를 환경 변수 또는 config.env 파일에서 가져옵니다.

    parametrize에서 fixture 이름이 전달된 경우 해당 fixture의 값을 반환합니다.

    Note: scope="function"으로 설정하여 indirect=True와 함께 사용될 때
    각 테스트 함수마다 다른 파라미터 값을 올바르게 처리할 수 있도록 합니다.
    """
    # parametrize에서 fixture 이름이 전달된 경우
    if (
        hasattr(request, "param")
        and isinstance(request.param, str)
        and request.param.startswith("index_")
    ):
        return request.getfixturevalue(request.param)

    # 기본 동작: 환경 변수에서 가져오기
    index_id = os.getenv("TL_INDEX_ID")
    if not index_id:
        raise ValueError(
            "TL_INDEX_ID 환경 변수가 설정되지 않았습니다. config.env 파일을 확인하거나 환경 변수를 설정하세요."
        )
    return index_id


@pytest.fixture(scope="session")
def index_marengo27():
    """Marengo 2.7 인덱스 ID를 환경 변수 또는 config.env 파일에서 가져옵니다."""
    index_id = os.getenv("TL_INDEX_MARENGO_27")
    if not index_id:
        pytest.skip(
            "TL_INDEX_MARENGO_27 환경 변수가 설정되지 않았습니다. config.env 파일을 확인하거나 환경 변수를 설정하세요."
        )
    return index_id


@pytest.fixture(scope="session")
def index_marengo30():
    """Marengo 3.0 인덱스 ID를 환경 변수 또는 config.env 파일에서 가져옵니다."""
    index_id = os.getenv("TL_INDEX_MARENGO_30")
    if not index_id:
        pytest.skip(
            "TL_INDEX_MARENGO_30 환경 변수가 설정되지 않았습니다. config.env 파일을 확인하거나 환경 변수를 설정하세요."
        )
    return index_id


@pytest.fixture(scope="session")
def client(api_key):
    """TwelveLabs 클라이언트 인스턴스를 생성합니다."""
    return TwelveLabs(api_key=api_key)


def get_index_name(request) -> str:
    """
    pytest request에서 사용된 인덱스 이름을 추출합니다.

    Args:
        request: pytest request fixture

    Returns:
        인덱스 이름 문자열 (예: "index_marengo27", "index_marengo30", "default")
    """
    if hasattr(request, "node") and hasattr(request.node, "callspec"):
        return request.node.callspec.params.get("index_id", "default")
    return "default"


def is_marengo30(index_name: str) -> bool:
    """
    인덱스 이름으로 Marengo 버전을 판단합니다.

    Args:
        index_name: 인덱스 이름 (예: "index_marengo27", "index_marengo30")

    Returns:
        True if Marengo 3.0, False if Marengo 2.7
    """
    return index_name == "index_marengo30"


def get_error_code(api_error: ApiError) -> str:
    """
    ApiError에서 error code를 추출합니다.

    Args:
        api_error: ApiError 인스턴스

    Returns:
        error code 문자열, 추출할 수 없는 경우 빈 문자열
    """
    if not api_error.body:
        return ""

    # body가 문자열인 경우 JSON 파싱 시도
    if isinstance(api_error.body, str):
        try:
            body_dict = json.loads(api_error.body)
        except (json.JSONDecodeError, TypeError):
            return ""
    else:
        body_dict = api_error.body

    # ErrorResponse 형식: {"error": {"code": "...", "message": "..."}}
    if isinstance(body_dict, dict):
        if "error" in body_dict and isinstance(body_dict["error"], dict):
            return body_dict["error"].get("code", "")
        # BadRequestErrorBody 형식: {"code": "...", "message": "..."}
        elif "code" in body_dict:
            return body_dict.get("code", "")

    return ""


def validate_marengo_fields(item, index_name: str = None, request=None):
    """
    Marengo 버전에 따라 중요한 필드가 있는지 검증합니다.

    Marengo 2.7: start, end, score, confidence
    Marengo 3.0: start, end, video_id, rank, transcription

    Args:
        item: SearchItem 인스턴스
        index_name: 인덱스 이름 (optional)
        request: pytest request (optional, index_name이 없을 때 사용)
    """
    if not index_name and request:
        index_name = get_index_name(request)
    elif not index_name:
        index_name = "default"

    is_30 = is_marengo30(index_name)

    # 공통 필드
    assert item.start is not None, f"start는 필수입니다 (index: {index_name})"
    assert item.end is not None, f"end는 필수입니다 (index: {index_name})"
    assert item.start < item.end, f"start는 end보다 작아야 합니다 (index: {index_name})"

    if is_30:
        # Marengo 3.0 필드
        assert (
            item.video_id is not None
        ), f"video_id는 필수입니다 (Marengo 3.0, index: {index_name})"
        assert (
            item.rank is not None
        ), f"rank는 필수입니다 (Marengo 3.0, index: {index_name})"
        assert isinstance(
            item.rank, int
        ), f"rank는 정수여야 합니다 (Marengo 3.0, index: {index_name})"
        assert (
            item.rank > 0
        ), f"rank는 1 이상이어야 합니다 (Marengo 3.0, index: {index_name})"
        # transcription은 optional이므로 None일 수 있음
    else:
        # Marengo 2.7 필드
        assert (
            item.score is not None
        ), f"score는 필수입니다 (Marengo 2.7, index: {index_name})"
        assert (
            item.confidence is not None
        ), f"confidence는 필수입니다 (Marengo 2.7, index: {index_name})"
        assert isinstance(
            item.score, (int, float)
        ), f"score는 숫자여야 합니다 (Marengo 2.7, index: {index_name})"
        assert item.confidence in [
            "high",
            "medium",
            "low",
        ], f"confidence는 'high', 'medium', 'low' 중 하나여야 합니다 (Marengo 2.7, index: {index_name})"
