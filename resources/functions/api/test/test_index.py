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
            {"DDB_TABLE_NAME": "ReInventSessionTable"},
        ):
            yield

    @pytest.fixture()
    def get_mutations_response(self):
        yield [
            {
                "SK": "2023-08-07T21:12:27.836826+00:00",
                "sessionID": "CMP201",
                "PK": "SessionMutation",
                "mutationType": "SessionAdded",
                "mutationData": {
                    "level": "200",
                    "topics": ["AI/ML", "Compute"],
                    "roles": [
                        "Data Scientist",
                        "Entrepreneur (Founder/Co-Founder)",
                        "Developer/Engineer",
                    ],
                    "scheduleUid": "AD1963B3-7991-45AB-A8D7-005C161DC952",
                    "description": "Generative AI can help you reinvent your applications, create entirely new customer experiences, and drive unprecedented levels of productivity. To help you realize the full promise of this transformative technology, Amazon EC2 provides performant, energy-efficient, and cost-effective instances. In this session, learn about the capabilities, benchmarks, and ideal use cases for each of these instances. Hear from AWS customers about how they built, deployed, and scaled large text and image generation models across various products and services using accelerated instances.",
                    "services": ["Amazon Elastic Compute Cloud (EC2)"],
                    "trackName": "Breakout Session",
                    "title": "Advancing generative AI innovation with Amazon EC2 accelerated compute",
                    "tags": [
                        {
                            "scheduleTagUid": "A633F4F0-69C9-4D21-880F-79DD248107A9",
                            "tagName": "Data Scientist",
                            "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                            "parentTagName": "Role",
                        },
                    ],
                    "thirdPartyID": "CMP201",
                    "industries": ["Cross Industry"],
                    "sessionUid": "BC517DF0-1904-49B6-BB63-9D73CFBFF839",
                    "SK": "CMP201",
                    "sessionType": "Breakout Session",
                    "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                    "PK": "ReInventSession",
                    "areas_of_interest": [
                        "Innovation on AWS",
                        "Cost Optimization",
                        "Generative AI",
                    ],
                },
            },
            {
                "SK": "2023-08-07T21:12:27.901818+00:00",
                "sessionID": "SVS309",
                "PK": "SessionMutation",
                "mutationType": "SessionAdded",
                "mutationData": {
                    "level": "300",
                    "topics": ["Serverless Compute"],
                    "roles": [
                        "DevOps Engineer",
                        "Solution/Systems Architect",
                        "Developer/Engineer",
                    ],
                    "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                    "description": "Enterprise-based serverless developers are often subject to constraints and compliance checks that can slow deployment and feedback loops. Shift-left practices can empower developers with tools that help test and validate code compliance prior to committing to repositories. In this session, learn about approaches to accelerate serverless development with faster feedback cycles. Explore best practices and tools with Capital One. Watch a live demo featuring an improved developer experience for building serverless applications while complying with enterprise governance requirements.",
                    "services": [
                        "AWS Serverless Application Model (SAM)",
                        "AWS Lambda",
                    ],
                    "trackName": "Breakout Session",
                    "title": "Improve productivity by shifting more responsibility to developers",
                    "tags": [
                        {
                            "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                            "tagName": "DevOps Engineer",
                            "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                            "parentTagName": "Role",
                        },
                    ],
                    "thirdPartyID": "SVS309",
                    "industries": [],
                    "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                    "SK": "SVS309",
                    "sessionType": "Breakout Session",
                    "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                    "PK": "ReInventSession",
                    "areas_of_interest": [],
                },
            },
        ]

    @pytest.fixture()
    def get_session_history_response(self):
        yield [
            {
                "SK": "2023-08-07T21:12:28.650860+00:00",
                "sessionID": "ADM201",
                "PK": "ADM201#SessionMutation",
                "mutationType": "SessionAdded",
                "mutationData": {
                    "level": "200",
                    "topics": ["AI/ML", "Analytics"],
                    "roles": ["Business Executive", "Data Engineer", "Data Scientist"],
                    "scheduleUid": "AB839BEB-0426-4322-B925-254B63BBC0F5",
                    "description": "<p>In this session intended for developers and data analysts, learn how companies use AWS technology to interoperate more effectively across advertising and marketing platforms. Discover how they do this by resolving related records stored across disparate channels and collaborating with other companies to enhance advertising activation and measurement without sharing the underlying data.</p>",
                    "services": ["AWS Clean Rooms"],
                    "trackName": "Breakout Session",
                    "title": "Building effective interoperability and data collaboration workflows",
                    "tags": [
                        {
                            "scheduleTagUid": "80461996-D59E-4C0F-9C3B-F76418AC905A",
                            "tagName": "Business Executive",
                            "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                            "parentTagName": "Role",
                        },
                    ],
                    "thirdPartyID": "ADM201",
                    "industries": ["Media & Entertainment", "Advertising & Marketing"],
                    "sessionUid": "E4D2B238-CDA8-4F5A-93BE-4914CFE8EC60",
                    "SK": "ADM201",
                    "sessionType": "Breakout Session",
                    "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                    "PK": "ReInventSession",
                    "areas_of_interest": [
                        "Customer Stories",
                        "Data Protection",
                        "Business Intelligence",
                    ],
                },
            }
        ]

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
        assert json.loads(response.body) == {
            "sessions": [
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
        }

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

    @staticmethod
    def test_get_session_history(get_session_history_response):
        # 1. ARRANGE
        from .. import index

        index._get_session_history = MagicMock()
        index._get_session_history.return_value = get_session_history_response

        # 2. ACT
        response = index.get_session_history("ADM201")

        # 3. ASSERT
        assert response.status_code == HTTPStatus.OK
        assert response.headers == {"Content-Type": "application/json"}
        assert response.compress is True
        assert json.loads(response.body) == {
            "mutations": [
                {
                    "sessionID": "ADM201",
                    "mutationType": "SessionAdded",
                    "mutationData": {
                        "level": "200",
                        "topics": ["AI/ML", "Analytics"],
                        "roles": [
                            "Business Executive",
                            "Data Engineer",
                            "Data Scientist",
                        ],
                        "scheduleUid": "AB839BEB-0426-4322-B925-254B63BBC0F5",
                        "description": "<p>In this session intended for developers and data analysts, learn how companies use AWS technology to interoperate more effectively across advertising and marketing platforms. Discover how they do this by resolving related records stored across disparate channels and collaborating with other companies to enhance advertising activation and measurement without sharing the underlying data.</p>",
                        "services": ["AWS Clean Rooms"],
                        "trackName": "Breakout Session",
                        "title": "Building effective interoperability and data collaboration workflows",
                        "tags": [
                            {
                                "scheduleTagUid": "80461996-D59E-4C0F-9C3B-F76418AC905A",
                                "tagName": "Business Executive",
                                "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                "parentTagName": "Role",
                            }
                        ],
                        "thirdPartyID": "ADM201",
                        "industries": [
                            "Media & Entertainment",
                            "Advertising & Marketing",
                        ],
                        "sessionUid": "E4D2B238-CDA8-4F5A-93BE-4914CFE8EC60",
                        "sessionType": "Breakout Session",
                        "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                        "areas_of_interest": [
                            "Customer Stories",
                            "Data Protection",
                            "Business Intelligence",
                        ],
                    },
                    "mutationDateTime": "2023-08-07T21:12:28.650860+00:00",
                }
            ]
        }

    @staticmethod
    def test_get_mutations(get_mutations_response):
        # 1. ARRANGE
        from .. import index

        index._get_all_mutations = MagicMock()
        index._get_all_mutations.return_value = get_mutations_response

        # 2. ACT
        response = index.get_mutations()

        # 3. ASSERT
        assert response.status_code == HTTPStatus.OK
        assert response.headers == {"Content-Type": "application/json"}
        assert response.compress is True
        assert json.loads(response.body) == {
            "mutations": [
                {
                    "sessionID": "SVS309",
                    "mutationType": "SessionAdded",
                    "mutationData": {
                        "level": "300",
                        "topics": ["Serverless Compute"],
                        "roles": [
                            "DevOps Engineer",
                            "Solution/Systems Architect",
                            "Developer/Engineer",
                        ],
                        "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                        "description": "Enterprise-based serverless developers are often subject to constraints and compliance checks that can slow deployment and feedback loops. Shift-left practices can empower developers with tools that help test and validate code compliance prior to committing to repositories. In this session, learn about approaches to accelerate serverless development with faster feedback cycles. Explore best practices and tools with Capital One. Watch a live demo featuring an improved developer experience for building serverless applications while complying with enterprise governance requirements.",
                        "services": [
                            "AWS Serverless Application Model (SAM)",
                            "AWS Lambda",
                        ],
                        "trackName": "Breakout Session",
                        "title": "Improve productivity by shifting more responsibility to developers",
                        "tags": [
                            {
                                "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                "tagName": "DevOps Engineer",
                                "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                "parentTagName": "Role",
                            }
                        ],
                        "thirdPartyID": "SVS309",
                        "industries": [],
                        "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                        "SK": "SVS309",
                        "sessionType": "Breakout Session",
                        "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                        "PK": "ReInventSession",
                        "areas_of_interest": [],
                    },
                    "mutationDateTime": "2023-08-07T21:12:27.901818+00:00",
                },
                {
                    "sessionID": "CMP201",
                    "mutationType": "SessionAdded",
                    "mutationData": {
                        "level": "200",
                        "topics": ["AI/ML", "Compute"],
                        "roles": [
                            "Data Scientist",
                            "Entrepreneur (Founder/Co-Founder)",
                            "Developer/Engineer",
                        ],
                        "scheduleUid": "AD1963B3-7991-45AB-A8D7-005C161DC952",
                        "description": "Generative AI can help you reinvent your applications, create entirely new customer experiences, and drive unprecedented levels of productivity. To help you realize the full promise of this transformative technology, Amazon EC2 provides performant, energy-efficient, and cost-effective instances. In this session, learn about the capabilities, benchmarks, and ideal use cases for each of these instances. Hear from AWS customers about how they built, deployed, and scaled large text and image generation models across various products and services using accelerated instances.",
                        "services": ["Amazon Elastic Compute Cloud (EC2)"],
                        "trackName": "Breakout Session",
                        "title": "Advancing generative AI innovation with Amazon EC2 accelerated compute",
                        "tags": [
                            {
                                "scheduleTagUid": "A633F4F0-69C9-4D21-880F-79DD248107A9",
                                "tagName": "Data Scientist",
                                "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                "parentTagName": "Role",
                            }
                        ],
                        "thirdPartyID": "CMP201",
                        "industries": ["Cross Industry"],
                        "sessionUid": "BC517DF0-1904-49B6-BB63-9D73CFBFF839",
                        "SK": "CMP201",
                        "sessionType": "Breakout Session",
                        "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                        "PK": "ReInventSession",
                        "areas_of_interest": [
                            "Innovation on AWS",
                            "Cost Optimization",
                            "Generative AI",
                        ],
                    },
                    "mutationDateTime": "2023-08-07T21:12:27.836826+00:00",
                },
            ]
        }
