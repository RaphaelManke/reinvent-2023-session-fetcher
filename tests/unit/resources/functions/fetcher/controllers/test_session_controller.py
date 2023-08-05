import sys

import pytest
from unittest.mock import MagicMock


class TestSessionController:
    """Tests for the SessionController."""

    @pytest.fixture(autouse=True)
    def function_path(self):
        sys.path.append("resources/functions/fetcher")
        yield
        sys.path.remove("resources/functions/fetcher")

    @staticmethod
    def test_get_session_from_list_by_id_not_found():
        # 1. ARRANGE
        from models import ReInventSession
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = []

        controller = SessionController(db_table_name="ReInventSessions")
        session_list = [
            ReInventSession(
                sessionType="Breakout Session",
                thirdPartyID="SVS309",
                trackName="Breakout Session",
                scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                description="Enterprise-based serverless developers...",
                scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                title="Improve productivity by shifting more responsibility to developers",
                level=300,
                tags=[
                    {
                        "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                        "tagName": "DevOps Engineer",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    }
                ],
            )
        ]

        # 2. ACT
        response = controller.get_session_from_list_by_id(
            session_id="test_session_id", session_list=session_list
        )

        # 3. ASSERT
        assert response is None

    @staticmethod
    def test_get_session_from_list_by_id_found():
        # 1. ARRANGE
        from models import ReInventSession
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = []

        controller = SessionController(db_table_name="ReInventSessions")
        session_list = [
            ReInventSession(
                sessionType="Breakout Session",
                thirdPartyID="SVS309",
                trackName="Breakout Session",
                scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                description="Enterprise-based serverless developers...",
                scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                title="Improve productivity by shifting more responsibility to developers",
                level=300,
                tags=[
                    {
                        "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                        "tagName": "DevOps Engineer",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    }
                ],
            )
        ]

        # 2. ACT
        response = controller.get_session_from_list_by_id(
            session_id="BD8998F7-BD38-474F-A5F9-44CDF5502BF4", session_list=session_list
        )

        # 3. ASSERT
        assert response is not None
