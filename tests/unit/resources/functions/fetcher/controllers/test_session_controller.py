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

        controller = SessionController(ddb_table_name="ReInventSessions")

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
                level=Decimal(300),
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

        controller = SessionController(ddb_table_name="ReInventSessions")

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
                level=Decimal(300),
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
                level=Decimal(300),
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

        controller = SessionController(ddb_table_name="ReInventSessions")

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
                level=Decimal(300),
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

        controller = SessionController(ddb_table_name="ReInventSessions")

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

        controller = SessionController(ddb_table_name="ReInventSessions")

        test_session = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="SVS309",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Enterprise-based serverless developers...",
            scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
            sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
            title="Improve productivity by shifting more responsibility to developers",
            level=Decimal(300),
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

        controller = SessionController(ddb_table_name="ReInventSessions")

        session_a = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="SVS309",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Enterprise-based serverless developers...",
            scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
            sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
            title="Improve productivity by shifting more responsibility to developers",
            level=Decimal(300),
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

        controller = SessionController(ddb_table_name="ReInventSessions")

        session_a = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="SVS309",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Enterprise-based serverless developers...",
            scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
            sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
            title="Improve productivity by shifting more responsibility to developers",
            level=Decimal(300),
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
        session_b.level = Decimal("400")

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

        controller = SessionController(ddb_table_name="ReInventSessions")

        session_a = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="SVS309",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Enterprise-based serverless developers...",
            scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
            sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
            title="Improve productivity by shifting more responsibility to developers",
            level=Decimal(300),
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

        controller = SessionController(ddb_table_name="ReInventSessions")

        session_a = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="SVS309",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Enterprise-based serverless developers...",
            scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
            sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
            title="Improve productivity by shifting more responsibility to developers",
            level=Decimal(300),
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
        session_b.level = Decimal("400")
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

        controller = SessionController(ddb_table_name="ReInventSessions")

        session_a = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="SVS309",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Enterprise-based serverless developers...",
            scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
            sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
            title="Improve productivity by shifting more responsibility to developers",
            level=Decimal(300),
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
        session_b.level = Decimal("400")
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

    @staticmethod
    def test_generate_diff_add_remove_update():
        # 1. ARRANGE
        from models import (
            ReInventSession,
            ReInventSessionTag,
            ReInventSessionListDiff,
            ReInventSessionFieldDiff,
            ReInventSessionDiff,
        )
        from controllers.session_controller import SessionController

        session_a_1 = ReInventSession(
            sessionType="standard",
            thirdPartyID="AUT303",
            trackName="Builders' Session",
            scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="<p>Automakers collect hundreds of petabytes of drive data...",
            scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
            sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
            title="Using generative AI to add objects in model training scenarios in ADDF",
            level=Decimal(300),
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                    tagName="AI/ML",
                    parentTagName="Topic",
                    parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                )
            ],
            topics=["AI/ML"],
            industries=["Automotive"],
            roles=[
                "Data Scientist",
                "Developer/Engineer",
                "Solution/Systems Architect",
            ],
            areas_of_interest=["Generative AI"],
            services=["Amazon Bedrock"],
        )
        session_a_2 = deepcopy(session_a_1)
        session_a_2.level = Decimal("400")

        session_b = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="CMP201",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Generative AI can help you reinvent your applications...",
            scheduleUid="AD1963B3-7991-45AB-A8D7-005C161DC952",
            sessionUid="BC517DF0-1904-49B6-BB63-9D73CFBFF839",
            title="Advancing generative AI innovation with Amazon EC2 accelerated compute",
            level=200,
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="A633F4F0-69C9-4D21-880F-79DD248107A9",
                    tagName="Data Scientist",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                ),
            ],
            topics=["AI/ML", "Compute"],
            industries=["Cross Industry"],
            roles=[
                "Data Scientist",
                "Entrepreneur (Founder/Co-Founder)",
                "Developer/Engineer",
            ],
            areas_of_interest=[
                "Innovation on AWS",
                "Cost Optimization",
                "Generative AI",
            ],
            services=["Amazon Elastic Compute Cloud (EC2)"],
        )

        session_c = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="SVS309",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Enterprise-based serverless developers are often subject to ...",
            scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
            sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
            title="Improve productivity by shifting more responsibility to developers",
            level=Decimal(300),
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                    tagName="DevOps Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                ),
            ],
            topics=["Serverless Compute"],
            industries=[],
            roles=[
                "DevOps Engineer",
                "Solution/Systems Architect",
                "Developer/Engineer",
            ],
            areas_of_interest=[],
            services=["AWS Serverless Application Model (SAM)", "AWS Lambda"],
        )

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = [
            session_a_1,
            session_b,
        ]

        controller = SessionController(ddb_table_name="ReInventSessions")

        # 2. ACT
        response = controller.generate_diff(
            new_session_list=[
                session_a_2,
                session_c,  # One changed, one added, one removed
            ]
        )

        # 3. ASSERT
        assert response == ReInventSessionListDiff(
            added_sessions={
                "BD8998F7-BD38-474F-A5F9-44CDF5502BF4": ReInventSession(
                    sessionType="Breakout Session",
                    thirdPartyID="SVS309",
                    trackName="Breakout Session",
                    scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                    description="Enterprise-based serverless developers are often subject to ...",
                    scheduleUid="706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                    sessionUid="BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                    title="Improve productivity by shifting more responsibility to developers",
                    level=Decimal("300"),
                    tags=[
                        ReInventSessionTag(
                            scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                            tagName="DevOps Engineer",
                            parentTagName="Role",
                            parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                        )
                    ],
                    topics=["Serverless Compute"],
                    industries=[],
                    roles=[
                        "DevOps Engineer",
                        "Solution/Systems Architect",
                        "Developer/Engineer",
                    ],
                    areas_of_interest=[],
                    services=[
                        "AWS Serverless Application Model (SAM)",
                        "AWS Lambda",
                    ],
                )
            },
            removed_sessions={
                "BC517DF0-1904-49B6-BB63-9D73CFBFF839": ReInventSession(
                    sessionType="Breakout Session",
                    thirdPartyID="CMP201",
                    trackName="Breakout Session",
                    scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                    description="Generative AI can help you reinvent your applications...",
                    scheduleUid="AD1963B3-7991-45AB-A8D7-005C161DC952",
                    sessionUid="BC517DF0-1904-49B6-BB63-9D73CFBFF839",
                    title="Advancing generative AI innovation with Amazon EC2 accelerated compute",
                    level=Decimal("200"),
                    tags=[
                        ReInventSessionTag(
                            scheduleTagUid="A633F4F0-69C9-4D21-880F-79DD248107A9",
                            tagName="Data Scientist",
                            parentTagName="Role",
                            parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                        )
                    ],
                    topics=["AI/ML", "Compute"],
                    industries=["Cross Industry"],
                    roles=[
                        "Data Scientist",
                        "Entrepreneur (Founder/Co-Founder)",
                        "Developer/Engineer",
                    ],
                    areas_of_interest=[
                        "Innovation on AWS",
                        "Cost Optimization",
                        "Generative AI",
                    ],
                    services=["Amazon Elastic Compute Cloud (EC2)"],
                )
            },
            updated_sessions={
                "0BA440C0-4774-40FA-A9B4-582ACB8668DA": ReInventSessionDiff(
                    old_session=ReInventSession(
                        sessionType="standard",
                        thirdPartyID="AUT303",
                        trackName="Builders' Session",
                        scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
                        description="<p>Automakers collect hundreds of petabytes of drive data...",
                        scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
                        sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
                        title="Using generative AI to add objects in model training scenarios in ADDF",
                        level=Decimal("300"),
                        tags=[
                            ReInventSessionTag(
                                scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                                tagName="AI/ML",
                                parentTagName="Topic",
                                parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                            )
                        ],
                        topics=["AI/ML"],
                        industries=["Automotive"],
                        roles=[
                            "Data Scientist",
                            "Developer/Engineer",
                            "Solution/Systems Architect",
                        ],
                        areas_of_interest=["Generative AI"],
                        services=["Amazon Bedrock"],
                    ),
                    new_session=ReInventSession(
                        sessionType="standard",
                        thirdPartyID="AUT303",
                        trackName="Builders' Session",
                        scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
                        description="<p>Automakers collect hundreds of petabytes of drive data...",
                        scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
                        sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
                        title="Using generative AI to add objects in model training scenarios in ADDF",
                        level=400,
                        tags=[
                            ReInventSessionTag(
                                scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                                tagName="AI/ML",
                                parentTagName="Topic",
                                parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                            )
                        ],
                        topics=["AI/ML"],
                        industries=["Automotive"],
                        roles=[
                            "Data Scientist",
                            "Developer/Engineer",
                            "Solution/Systems Architect",
                        ],
                        areas_of_interest=["Generative AI"],
                        services=["Amazon Bedrock"],
                    ),
                    changed_fields=[
                        ReInventSessionFieldDiff(
                            field="level",
                            old_value=Decimal("300"),
                            new_value=Decimal("400"),
                        )
                    ],
                )
            },
        )

    @staticmethod
    def test_generate_diff_add_only():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionTag, ReInventSessionListDiff
        from controllers.session_controller import SessionController

        session_a = ReInventSession(
            sessionType="standard",
            thirdPartyID="AUT303",
            trackName="Builders' Session",
            scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="<p>Automakers collect hundreds of petabytes of drive data...",
            scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
            sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
            title="Using generative AI to add objects in model training scenarios in ADDF",
            level=Decimal(300),
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                    tagName="AI/ML",
                    parentTagName="Topic",
                    parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                )
            ],
            topics=["AI/ML"],
            industries=["Automotive"],
            roles=[
                "Data Scientist",
                "Developer/Engineer",
                "Solution/Systems Architect",
            ],
            areas_of_interest=["Generative AI"],
            services=["Amazon Bedrock"],
        )

        session_b = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="CMP201",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Generative AI can help you reinvent your applications...",
            scheduleUid="AD1963B3-7991-45AB-A8D7-005C161DC952",
            sessionUid="BC517DF0-1904-49B6-BB63-9D73CFBFF839",
            title="Advancing generative AI innovation with Amazon EC2 accelerated compute",
            level=200,
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="A633F4F0-69C9-4D21-880F-79DD248107A9",
                    tagName="Data Scientist",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                ),
            ],
            topics=["AI/ML", "Compute"],
            industries=["Cross Industry"],
            roles=[
                "Data Scientist",
                "Entrepreneur (Founder/Co-Founder)",
                "Developer/Engineer",
            ],
            areas_of_interest=[
                "Innovation on AWS",
                "Cost Optimization",
                "Generative AI",
            ],
            services=["Amazon Elastic Compute Cloud (EC2)"],
        )

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = [session_a]

        controller = SessionController(ddb_table_name="ReInventSessions")

        # 2. ACT
        response = controller.generate_diff(new_session_list=[session_a, session_b])

        # 3. ASSERT
        assert response == ReInventSessionListDiff(
            added_sessions={
                "BC517DF0-1904-49B6-BB63-9D73CFBFF839": ReInventSession(
                    sessionType="Breakout Session",
                    thirdPartyID="CMP201",
                    trackName="Breakout Session",
                    scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                    description="Generative AI can help you reinvent your applications...",
                    scheduleUid="AD1963B3-7991-45AB-A8D7-005C161DC952",
                    sessionUid="BC517DF0-1904-49B6-BB63-9D73CFBFF839",
                    title="Advancing generative AI innovation with Amazon EC2 accelerated compute",
                    level=200,
                    tags=[
                        ReInventSessionTag(
                            scheduleTagUid="A633F4F0-69C9-4D21-880F-79DD248107A9",
                            tagName="Data Scientist",
                            parentTagName="Role",
                            parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                        ),
                    ],
                    topics=["AI/ML", "Compute"],
                    industries=["Cross Industry"],
                    roles=[
                        "Data Scientist",
                        "Entrepreneur (Founder/Co-Founder)",
                        "Developer/Engineer",
                    ],
                    areas_of_interest=[
                        "Innovation on AWS",
                        "Cost Optimization",
                        "Generative AI",
                    ],
                    services=["Amazon Elastic Compute Cloud (EC2)"],
                )
            },
            removed_sessions={},
            updated_sessions={},
        )

    @staticmethod
    def test_generate_diff_remove_only():
        # 1. ARRANGE
        from models import ReInventSession, ReInventSessionTag, ReInventSessionListDiff
        from controllers.session_controller import SessionController

        session_a = ReInventSession(
            sessionType="standard",
            thirdPartyID="AUT303",
            trackName="Builders' Session",
            scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="<p>Automakers collect hundreds of petabytes of drive data...",
            scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
            sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
            title="Using generative AI to add objects in model training scenarios in ADDF",
            level=Decimal(300),
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                    tagName="AI/ML",
                    parentTagName="Topic",
                    parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                )
            ],
            topics=["AI/ML"],
            industries=["Automotive"],
            roles=[
                "Data Scientist",
                "Developer/Engineer",
                "Solution/Systems Architect",
            ],
            areas_of_interest=["Generative AI"],
            services=["Amazon Bedrock"],
        )

        session_b = ReInventSession(
            sessionType="Breakout Session",
            thirdPartyID="CMP201",
            trackName="Breakout Session",
            scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="Generative AI can help you reinvent your applications...",
            scheduleUid="AD1963B3-7991-45AB-A8D7-005C161DC952",
            sessionUid="BC517DF0-1904-49B6-BB63-9D73CFBFF839",
            title="Advancing generative AI innovation with Amazon EC2 accelerated compute",
            level=200,
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="A633F4F0-69C9-4D21-880F-79DD248107A9",
                    tagName="Data Scientist",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                ),
            ],
            topics=["AI/ML", "Compute"],
            industries=["Cross Industry"],
            roles=[
                "Data Scientist",
                "Entrepreneur (Founder/Co-Founder)",
                "Developer/Engineer",
            ],
            areas_of_interest=[
                "Innovation on AWS",
                "Cost Optimization",
                "Generative AI",
            ],
            services=["Amazon Elastic Compute Cloud (EC2)"],
        )

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = [session_a, session_b]

        controller = SessionController(ddb_table_name="ReInventSessions")

        # 2. ACT
        response = controller.generate_diff(new_session_list=[session_a])

        # 3. ASSERT
        assert response == ReInventSessionListDiff(
            added_sessions={},
            removed_sessions={
                "BC517DF0-1904-49B6-BB63-9D73CFBFF839": ReInventSession(
                    sessionType="Breakout Session",
                    thirdPartyID="CMP201",
                    trackName="Breakout Session",
                    scheduleTrackUid="CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                    description="Generative AI can help you reinvent your applications...",
                    scheduleUid="AD1963B3-7991-45AB-A8D7-005C161DC952",
                    sessionUid="BC517DF0-1904-49B6-BB63-9D73CFBFF839",
                    title="Advancing generative AI innovation with Amazon EC2 accelerated compute",
                    level=200,
                    tags=[
                        ReInventSessionTag(
                            scheduleTagUid="A633F4F0-69C9-4D21-880F-79DD248107A9",
                            tagName="Data Scientist",
                            parentTagName="Role",
                            parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                        ),
                    ],
                    topics=["AI/ML", "Compute"],
                    industries=["Cross Industry"],
                    roles=[
                        "Data Scientist",
                        "Entrepreneur (Founder/Co-Founder)",
                        "Developer/Engineer",
                    ],
                    areas_of_interest=[
                        "Innovation on AWS",
                        "Cost Optimization",
                        "Generative AI",
                    ],
                    services=["Amazon Elastic Compute Cloud (EC2)"],
                )
            },
            updated_sessions={},
        )

    @staticmethod
    def test_generate_diff_update_tags_only():
        # 1. ARRANGE
        from models import (
            ReInventSession,
            ReInventSessionTag,
            ReInventSessionListDiff,
            ReInventSessionDiff,
            ReInventSessionFieldDiff,
        )
        from controllers.session_controller import SessionController

        session_a_1 = ReInventSession(
            sessionType="standard",
            thirdPartyID="AUT303",
            trackName="Builders' Session",
            scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="<p>Automakers collect hundreds of petabytes of drive data...",
            scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
            sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
            title="Using generative AI to add objects in model training scenarios in ADDF",
            level=Decimal(300),
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                    tagName="AI/ML",
                    parentTagName="Topic",
                    parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                )
            ],
            topics=["AI/ML"],
            industries=["Automotive"],
            roles=[
                "Data Scientist",
                "Developer/Engineer",
                "Solution/Systems Architect",
            ],
            areas_of_interest=["Generative AI"],
            services=["Amazon Bedrock"],
        )
        session_a_2 = ReInventSession(
            sessionType="standard",
            thirdPartyID="AUT303",
            trackName="Builders' Session",
            scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="<p>Automakers collect hundreds of petabytes of drive data...",
            scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
            sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
            title="Using generative AI to add objects in model training scenarios in ADDF",
            level=Decimal(300),
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                    tagName="AI/ML",
                    parentTagName="Topic",
                    parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                ),
                ReInventSessionTag(
                    scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                    tagName="DevOps Engineer",
                    parentTagName="Role",
                    parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                ),
            ],
            topics=["AI/ML"],
            industries=["Automotive"],
            roles=[
                "Data Scientist",
                "Developer/Engineer",
                "Solution/Systems Architect",
            ],
            areas_of_interest=["Generative AI"],
            services=["Amazon Bedrock"],
        )

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = [session_a_1]

        controller = SessionController(ddb_table_name="ReInventSessions")

        # 2. ACT
        response = controller.generate_diff(new_session_list=[session_a_2])

        # 3. ASSERT
        assert response == ReInventSessionListDiff(
            added_sessions={},
            removed_sessions={},
            updated_sessions={
                "0BA440C0-4774-40FA-A9B4-582ACB8668DA": ReInventSessionDiff(
                    old_session=ReInventSession(
                        sessionType="standard",
                        thirdPartyID="AUT303",
                        trackName="Builders' Session",
                        scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
                        description="<p>Automakers collect hundreds of petabytes of drive data...",
                        scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
                        sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
                        title="Using generative AI to add objects in model training scenarios in ADDF",
                        level=Decimal("300"),
                        tags=[
                            ReInventSessionTag(
                                scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                                tagName="AI/ML",
                                parentTagName="Topic",
                                parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                            )
                        ],
                        topics=["AI/ML"],
                        industries=["Automotive"],
                        roles=[
                            "Data Scientist",
                            "Developer/Engineer",
                            "Solution/Systems Architect",
                        ],
                        areas_of_interest=["Generative AI"],
                        services=["Amazon Bedrock"],
                    ),
                    new_session=ReInventSession(
                        sessionType="standard",
                        thirdPartyID="AUT303",
                        trackName="Builders' Session",
                        scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
                        description="<p>Automakers collect hundreds of petabytes of drive data...",
                        scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
                        sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
                        title="Using generative AI to add objects in model training scenarios in ADDF",
                        level=Decimal("300"),
                        tags=[
                            ReInventSessionTag(
                                scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                                tagName="AI/ML",
                                parentTagName="Topic",
                                parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                            ),
                            ReInventSessionTag(
                                scheduleTagUid="16A05B04-62C9-45E5-A5AC-79CB47268800",
                                tagName="DevOps Engineer",
                                parentTagName="Role",
                                parentTagUid="22A77ABD-348D-4E44-800F-846017E75A5D",
                            ),
                        ],
                        topics=["AI/ML"],
                        industries=["Automotive"],
                        roles=[
                            "Data Scientist",
                            "Developer/Engineer",
                            "Solution/Systems Architect",
                        ],
                        areas_of_interest=["Generative AI"],
                        services=["Amazon Bedrock"],
                    ),
                    changed_fields=[
                        ReInventSessionFieldDiff(
                            field="tags",
                            old_value=[
                                {
                                    "scheduleTagUid": "3DC75316-93EB-43DB-972C-594B6A06B18E",
                                    "tagName": "AI/ML",
                                    "parentTagName": "Topic",
                                    "parentTagUid": "F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                                }
                            ],
                            new_value=[
                                {
                                    "scheduleTagUid": "3DC75316-93EB-43DB-972C-594B6A06B18E",
                                    "tagName": "AI/ML",
                                    "parentTagName": "Topic",
                                    "parentTagUid": "F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                                },
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                },
                            ],
                        ),
                        ReInventSessionFieldDiff(
                            field="roles",
                            old_value=[
                                "Data Scientist",
                                "Developer/Engineer",
                                "Solution/Systems Architect",
                            ],
                            new_value=[
                                "Data Scientist",
                                "Developer/Engineer",
                                "Solution/Systems Architect",
                                "DevOps Engineer",
                            ],
                        ),
                    ],
                )
            },
        )

    @staticmethod
    def test_generate_diff_update_only():
        # 1. ARRANGE
        from models import (
            ReInventSession,
            ReInventSessionTag,
            ReInventSessionListDiff,
            ReInventSessionDiff,
            ReInventSessionFieldDiff,
        )
        from controllers.session_controller import SessionController

        session_a_1 = ReInventSession(
            sessionType="standard",
            thirdPartyID="AUT303",
            trackName="Builders' Session",
            scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
            description="<p>Automakers collect hundreds of petabytes of drive data...",
            scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
            sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
            title="Using generative AI to add objects in model training scenarios in ADDF",
            level=Decimal(300),
            tags=[
                ReInventSessionTag(
                    scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                    tagName="AI/ML",
                    parentTagName="Topic",
                    parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                )
            ],
            topics=["AI/ML"],
            industries=["Automotive"],
            roles=[
                "Data Scientist",
                "Developer/Engineer",
                "Solution/Systems Architect",
            ],
            areas_of_interest=["Generative AI"],
            services=["Amazon Bedrock"],
        )
        session_a_2 = deepcopy(session_a_1)
        session_a_2.level = Decimal("400")

        SessionController._init_from_db = MagicMock()
        SessionController._init_from_db.return_value = [session_a_1]

        controller = SessionController(ddb_table_name="ReInventSessions")

        # 2. ACT
        response = controller.generate_diff(new_session_list=[session_a_2])

        # 3. ASSERT
        assert response == ReInventSessionListDiff(
            added_sessions={},
            removed_sessions={},
            updated_sessions={
                "0BA440C0-4774-40FA-A9B4-582ACB8668DA": ReInventSessionDiff(
                    old_session=ReInventSession(
                        sessionType="standard",
                        thirdPartyID="AUT303",
                        trackName="Builders' Session",
                        scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
                        description="<p>Automakers collect hundreds of petabytes of drive data...",
                        scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
                        sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
                        title="Using generative AI to add objects in model training scenarios in ADDF",
                        level=Decimal("300"),
                        tags=[
                            ReInventSessionTag(
                                scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                                tagName="AI/ML",
                                parentTagName="Topic",
                                parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                            )
                        ],
                        topics=["AI/ML"],
                        industries=["Automotive"],
                        roles=[
                            "Data Scientist",
                            "Developer/Engineer",
                            "Solution/Systems Architect",
                        ],
                        areas_of_interest=["Generative AI"],
                        services=["Amazon Bedrock"],
                    ),
                    new_session=ReInventSession(
                        sessionType="standard",
                        thirdPartyID="AUT303",
                        trackName="Builders' Session",
                        scheduleTrackUid="3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
                        description="<p>Automakers collect hundreds of petabytes of drive data...",
                        scheduleUid="C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
                        sessionUid="0BA440C0-4774-40FA-A9B4-582ACB8668DA",
                        title="Using generative AI to add objects in model training scenarios in ADDF",
                        level=Decimal("400"),
                        tags=[
                            ReInventSessionTag(
                                scheduleTagUid="3DC75316-93EB-43DB-972C-594B6A06B18E",
                                tagName="AI/ML",
                                parentTagName="Topic",
                                parentTagUid="F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                            )
                        ],
                        topics=["AI/ML"],
                        industries=["Automotive"],
                        roles=[
                            "Data Scientist",
                            "Developer/Engineer",
                            "Solution/Systems Architect",
                        ],
                        areas_of_interest=["Generative AI"],
                        services=["Amazon Bedrock"],
                    ),
                    changed_fields=[
                        ReInventSessionFieldDiff(
                            field="level",
                            old_value=Decimal("300"),
                            new_value=Decimal("400"),
                        ),
                    ],
                )
            },
        )
