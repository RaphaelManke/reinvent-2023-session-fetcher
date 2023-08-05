from decimal import Decimal
import sys

import pytest
from unittest.mock import MagicMock
from copy import deepcopy


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
        from models import ReInventSession, ReInventSessionTag
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
                    ReInventSessionTag(
                        scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                        tagName="DevOps Engineer",
                        parentTagName="Role",
                        parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                    )
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
        from models import ReInventSession, ReInventSessionTag
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
                    ReInventSessionTag(
                        scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                        tagName="DevOps Engineer",
                        parentTagName="Role",
                        parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                    )
                ],
            )
        ]

        # 2. ACT
        response = controller.get_session_from_list_by_id(
            session_id="BD8998F7-BD38-474F-A5F9-44CDF5502BF4", session_list=session_list
        )

        # 3. ASSERT
        assert response is not None

    @staticmethod
    def test_get_session_by_id_not_found():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionTag
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = [
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
                    ReInventSessionTag(
                        scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                        tagName="DevOps Engineer",
                        parentTagName="Role",
                        parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                    )
                ],
            )
        ]

        controller = SessionController(db_table_name="ReInventSessions")

        # 2. ACT
        response = controller.get_session_by_id(session_id="test_session_id")

        # 3. ASSERT
        assert response is None

    @staticmethod
    def test_get_session_by_id_found():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionTag
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = [
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
                    ReInventSessionTag(
                        scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                        tagName="DevOps Engineer",
                        parentTagName="Role",
                        parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                    )
                ],
            )
        ]

        controller = SessionController(db_table_name="ReInventSessions")

        # 2. ACT
        response = controller.get_session_by_id(
            session_id="BD8998F7-BD38-474F-A5F9-44CDF5502BF4"
        )

        # 3. ASSERT
        assert response is not None

    @staticmethod
    def test_get_session_diff_no_change():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionTag
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = []

        controller = SessionController(db_table_name="ReInventSessions")

        test_session = ReInventSession(
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
                ReInventSessionTag(
                    scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                    tagName="DevOps Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                )
            ],
        )

        # 2. ACT
        response = controller.get_session_diff(
            session_a=test_session, session_b=test_session
        )

        # 3. ASSERT
        assert response == []

    @staticmethod
    def test_get_session_diff_order_change():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionTag
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = []

        controller = SessionController(db_table_name="ReInventSessions")

        session_a = ReInventSession(
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
                ReInventSessionTag(
                    scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                    tagName="DevOps Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                ),
                ReInventSessionTag(
                    scheduleTagUid="4F085EF2-7954-4A96-9A8C-45BC0EC61359",
                    tagName="Developer/Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                ),
            ],
        )
        session_b = deepcopy(session_a)
        session_b.tags = [
            ReInventSessionTag(
                scheduleTagUid="4F085EF2-7954-4A96-9A8C-45BC0EC61359",
                tagName="Developer/Engineer",
                parentTagName="Role",
                parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
            ),
            ReInventSessionTag(
                scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                tagName="DevOps Engineer",
                parentTagName="Role",
                parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
            ),
        ]

        # 2. ACT
        response = controller.get_session_diff(session_a=session_a, session_b=session_b)

        # 3. ASSERT
        assert response == []

    @staticmethod
    def test_get_session_diff_field_change():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionTag, ReInventSessionFieldDiff
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = []

        controller = SessionController(db_table_name="ReInventSessions")

        session_a = ReInventSession(
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
                ReInventSessionTag(
                    scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                    tagName="DevOps Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                ),
                ReInventSessionTag(
                    scheduleTagUid="4F085EF2-7954-4A96-9A8C-45BC0EC61359",
                    tagName="Developer/Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                ),
            ],
        )
        session_b = deepcopy(session_a)
        session_b.level = Decimal(400)

        # 2. ACT
        response = controller.get_session_diff(session_a=session_a, session_b=session_b)

        # 3. ASSERT
        assert response == [
            ReInventSessionFieldDiff(
                field="level", old_value=Decimal("300"), new_value=Decimal("400")
            )
        ]

    @staticmethod
    def test_get_session_diff_field_add():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionFieldDiff, ReInventSessionTag
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = []

        controller = SessionController(db_table_name="ReInventSessions")

        session_a = ReInventSession(
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
                ReInventSessionTag(
                    scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                    tagName="DevOps Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                )
            ],
        )
        session_b = deepcopy(session_a)
        session_b.tags.append(
            ReInventSessionTag(
                scheduleTagUid="4F085EF2-7954-4A96-9A8C-45BC0EC61359",
                tagName="Developer/Engineer",
                parentTagName="Role",
                parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
            )
        )

        # 2. ACT
        response = controller.get_session_diff(session_a=session_a, session_b=session_b)

        # 3. ASSERT
        assert response == [
            ReInventSessionFieldDiff(
                field="tags",
                old_value=[
                    {
                        "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                        "tagName": "DevOps Engineer",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    }
                ],
                new_value=[
                    {
                        "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                        "tagName": "DevOps Engineer",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    },
                    {
                        "scheduleTagUid": "4F085EF2-7954-4A96-9A8C-45BC0EC61359",
                        "tagName": "Developer/Engineer",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    },
                ],
            )
        ]

    @staticmethod
    def test_get_session_diff_field_change_and_add():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionFieldDiff, ReInventSessionTag
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = []

        controller = SessionController(db_table_name="ReInventSessions")

        session_a = ReInventSession(
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
                ReInventSessionTag(
                    scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                    tagName="DevOps Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                )
            ],
        )
        session_b = deepcopy(session_a)
        session_b.level = Decimal(400)
        session_b.tags.append(
            ReInventSessionTag(
                scheduleTagUid="4F085EF2-7954-4A96-9A8C-45BC0EC61359",
                tagName="Developer/Engineer",
                parentTagName="Role",
                parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
            )
        )

        # 2. ACT
        response = controller.get_session_diff(session_a=session_a, session_b=session_b)

        # 3. ASSERT
        assert response == [
            ReInventSessionFieldDiff(
                field="level", old_value=Decimal("300"), new_value=Decimal("400")
            ),
            ReInventSessionFieldDiff(
                field="tags",
                old_value=[
                    {
                        "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                        "tagName": "DevOps Engineer",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    }
                ],
                new_value=[
                    {
                        "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                        "tagName": "DevOps Engineer",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    },
                    {
                        "scheduleTagUid": "4F085EF2-7954-4A96-9A8C-45BC0EC61359",
                        "tagName": "Developer/Engineer",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    },
                ],
            ),
        ]

    @staticmethod
    def test_get_session_diff_field_change_double():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionFieldDiff, ReInventSessionTag
        from controllers.session_controller import SessionController

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = []

        controller = SessionController(db_table_name="ReInventSessions")

        session_a = ReInventSession(
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
                ReInventSessionTag(
                    scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                    tagName="DevOps Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                )
            ],
        )
        session_b = deepcopy(session_a)
        session_b.level = Decimal(400)
        session_b.title = (
            "Don't improve productivity by shifting more responsibility to developers"
        )

        # 2. ACT
        response = controller.get_session_diff(session_a=session_a, session_b=session_b)

        # 3. ASSERT
        assert response == [
            ReInventSessionFieldDiff(
                field="title",
                old_value="Improve productivity by shifting more responsibility to developers",
                new_value="Don't improve productivity by shifting more responsibility to developers",
            ),
            ReInventSessionFieldDiff(
                field="level", old_value=Decimal("300"), new_value=Decimal("400")
            ),
        ]
