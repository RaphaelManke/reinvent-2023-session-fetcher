from http import HTTPStatus
from decimal import Decimal
import json
import os
import sys

import pytest
from unittest import mock
from unittest.mock import MagicMock


class TestApi:
    """Tests for the API."""

    @pytest.fixture(autouse=True)
    def env(self):
        with mock.patch.dict(
            os.environ,
            {"DDB_TABLE_NAME": "MockTable"},
        ):
            yield

    @pytest.fixture()
    def get_session_response(self):
        yield {
            "services": ["AWS Clean Rooms"],
            "sessionUid": "E4D2B238-CDA8-4F5A-93BE-4914CFE8EC60",
            "topics": ["AI/ML", "Analytics"],
            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            "areas_of_interest": [
                "Customer Stories",
                "Data Protection",
                "Business Intelligence",
            ],
            "industries": ["Media & Entertainment", "Advertising & Marketing"],
            "roles": ["Business Executive", "Data Engineer", "Data Scientist"],
            "trackName": "Breakout Session",
            "level": Decimal("200"),
            "thirdPartyID": "ADM201",
            "sessionType": "Breakout Session",
            "scheduleUid": "AB839BEB-0426-4322-B925-254B63BBC0F5",
            "SK": "ADM201",
            "description": "<p>In this session intended for developers and data analysts, ...</p>",
            "PK": "ReInventSession",
            "tags": [
                {
                    "scheduleTagUid": "80461996-D59E-4C0F-9C3B-F76418AC905A",
                    "tagName": "Business Executive",
                    "parentTagName": "Role",
                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                },
            ],
            "title": "Building effective interoperability and data collaboration workflows",
        }

    @pytest.fixture()
    def get_all_sessions_response(self):
        yield [
            {
                "services": ["AWS Clean Rooms"],
                "sessionUid": "E4D2B238-CDA8-4F5A-93BE-4914CFE8EC60",
                "topics": ["AI/ML", "Analytics"],
                "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                "areas_of_interest": [
                    "Customer Stories",
                    "Data Protection",
                    "Business Intelligence",
                ],
                "industries": ["Media & Entertainment", "Advertising & Marketing"],
                "roles": ["Business Executive", "Data Engineer", "Data Scientist"],
                "trackName": "Breakout Session",
                "level": Decimal("200"),
                "thirdPartyID": "ADM201",
                "sessionType": "Breakout Session",
                "scheduleUid": "AB839BEB-0426-4322-B925-254B63BBC0F5",
                "SK": "ADM201",
                "description": "<p>In this session intended for developers and data analysts, ...</p>",
                "PK": "ReInventSession",
                "tags": [
                    {
                        "scheduleTagUid": "80461996-D59E-4C0F-9C3B-F76418AC905A",
                        "tagName": "Business Executive",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    },
                ],
                "title": "Building effective interoperability and data collaboration workflows",
            },
            {
                "services": [
                    "Amazon Athena",
                    "Amazon GuardDuty",
                    "Amazon Detective",
                ],
                "sessionUid": "FBFB541D-9965-4D48-9E61-AFDA7FADD920",
                "topics": ["Compute", "AI/ML"],
                "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                "areas_of_interest": [
                    "Global Infrastructure",
                    "Cost Optimization",
                    "Customer Stories",
                ],
                "industries": [
                    "Aerospace & Satellite",
                    "Nonprofit",
                    "Financial Services",
                ],
                "roles": ["Business Executive", "Data Scientist", "IT Executive"],
                "trackName": "Breakout Session",
                "level": Decimal("200"),
                "thirdPartyID": "AES202",
                "sessionType": "Breakout Session",
                "scheduleUid": "AE0ADA40-8C8B-4732-932D-71F0885EAEDC",
                "SK": "AES202",
                "description": "In this session, learn how Alteia combines AWS open data and machine ...",
                "PK": "ReInventSession",
                "tags": [
                    {
                        "scheduleTagUid": "6A158CFE-6E8A-447D-A3C1-172880E06D98",
                        "tagName": "Global Infrastructure",
                        "parentTagName": "Area of Interest",
                        "parentTagUid": "3428EB86-4D79-4EFE-9F33-E911FCC500A4",
                    },
                ],
                "title": "Alteia, World Bank, and AWS help countries build road networks faster",
            },
        ]

    @staticmethod
    def test_get_sessions(get_all_sessions_response):
        # 1. ARRANGE
        from .. import index

        index._get_all_sessions = MagicMock()
        index._get_all_sessions.return_value = get_all_sessions_response

        # 2. ACT
        response = index.get_sessions()

        # 3. ASSERT
        assert response.status_code == HTTPStatus.OK
        assert response.headers == {"Content-Type": "application/json"}
        assert response.compress is True
        assert json.loads(response.body) == [
            {
                "services": ["AWS Clean Rooms"],
                "sessionUid": "E4D2B238-CDA8-4F5A-93BE-4914CFE8EC60",
                "topics": ["AI/ML", "Analytics"],
                "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                "areas_of_interest": [
                    "Customer Stories",
                    "Data Protection",
                    "Business Intelligence",
                ],
                "industries": ["Media & Entertainment", "Advertising & Marketing"],
                "roles": ["Business Executive", "Data Engineer", "Data Scientist"],
                "trackName": "Breakout Session",
                "level": "200",
                "thirdPartyID": "ADM201",
                "sessionType": "Breakout Session",
                "scheduleUid": "AB839BEB-0426-4322-B925-254B63BBC0F5",
                "description": "<p>In this session intended for developers and data analysts, ...</p>",
                "tags": [
                    {
                        "scheduleTagUid": "80461996-D59E-4C0F-9C3B-F76418AC905A",
                        "tagName": "Business Executive",
                        "parentTagName": "Role",
                        "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                    }
                ],
                "title": "Building effective interoperability and data collaboration workflows",
            },
            {
                "services": [
                    "Amazon Athena",
                    "Amazon GuardDuty",
                    "Amazon Detective",
                ],
                "sessionUid": "FBFB541D-9965-4D48-9E61-AFDA7FADD920",
                "topics": ["Compute", "AI/ML"],
                "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                "areas_of_interest": [
                    "Global Infrastructure",
                    "Cost Optimization",
                    "Customer Stories",
                ],
                "industries": [
                    "Aerospace & Satellite",
                    "Nonprofit",
                    "Financial Services",
                ],
                "roles": ["Business Executive", "Data Scientist", "IT Executive"],
                "trackName": "Breakout Session",
                "level": "200",
                "thirdPartyID": "AES202",
                "sessionType": "Breakout Session",
                "scheduleUid": "AE0ADA40-8C8B-4732-932D-71F0885EAEDC",
                "description": "In this session, learn how Alteia combines AWS open data and machine ...",
                "tags": [
                    {
                        "scheduleTagUid": "6A158CFE-6E8A-447D-A3C1-172880E06D98",
                        "tagName": "Global Infrastructure",
                        "parentTagName": "Area of Interest",
                        "parentTagUid": "3428EB86-4D79-4EFE-9F33-E911FCC500A4",
                    }
                ],
                "title": "Alteia, World Bank, and AWS help countries build road networks faster",
            },
        ]

    @staticmethod
    def test_get_session(get_session_response):
        # 1. ARRANGE
        from .. import index

        index._get_session = MagicMock()
        index._get_session.return_value = get_session_response

        # 2. ACT
        response = index.get_session("ADM201")

        # 3. ASSERT
        assert response.status_code == HTTPStatus.OK
        assert response.headers == {"Content-Type": "application/json"}
        assert response.compress is True
        assert json.loads(response.body) == {
            "services": ["AWS Clean Rooms"],
            "sessionUid": "E4D2B238-CDA8-4F5A-93BE-4914CFE8EC60",
            "topics": ["AI/ML", "Analytics"],
            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
            "areas_of_interest": [
                "Customer Stories",
                "Data Protection",
                "Business Intelligence",
            ],
            "industries": ["Media & Entertainment", "Advertising & Marketing"],
            "roles": ["Business Executive", "Data Engineer", "Data Scientist"],
            "trackName": "Breakout Session",
            "level": "200",
            "thirdPartyID": "ADM201",
            "sessionType": "Breakout Session",
            "scheduleUid": "AB839BEB-0426-4322-B925-254B63BBC0F5",
            "description": "<p>In this session intended for developers and data analysts, ...</p>",
            "tags": [
                {
                    "scheduleTagUid": "80461996-D59E-4C0F-9C3B-F76418AC905A",
                    "tagName": "Business Executive",
                    "parentTagName": "Role",
                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                }
            ],
            "title": "Building effective interoperability and data collaboration workflows",
        }
