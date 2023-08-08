import os
import json

import freezegun
import pytest
from unittest import mock
from unittest.mock import MagicMock


class TestEventGenerator:
    """Tests for the EventGenerator."""

    @pytest.fixture(autouse=True)
    def env(self):
        with mock.patch.dict(
            os.environ,
            {"EVENT_BUS_NAME": "MockEventBus"},
        ):
            yield

    @pytest.fixture
    def session_updated_v1_event_list_element_add(self):
        yield {
            "eventID": "e29fcf34cf3cce9dff441404e59cfd62",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-west-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1691353296.0,
                "Keys": {"SK": {"S": "SVS309"}, "PK": {"S": "ReInventSession"}},
                "NewImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                            {"S": "ExtraTest/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            }
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "OldImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            },
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "SequenceNumber": "21626200000000067447717181",
                "SizeBytes": 4401,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
        }

    @pytest.fixture
    def session_updated_v1_event_list_element_remove(self):
        yield {
            "eventID": "e29fcf34cf3cce9dff441404e59cfd62",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-west-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1691353296.0,
                "Keys": {"SK": {"S": "SVS309"}, "PK": {"S": "ReInventSession"}},
                "NewImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            }
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "OldImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            },
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "SequenceNumber": "21626200000000067447717181",
                "SizeBytes": 4401,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
        }

    @pytest.fixture
    def session_updated_v1_event_list_element_reorder(self):
        yield {
            "eventID": "e29fcf34cf3cce9dff441404e59cfd62",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-west-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1691353296.0,
                "Keys": {"SK": {"S": "SVS309"}, "PK": {"S": "ReInventSession"}},
                "NewImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "Developer/Engineer"},
                            {"S": "DevOps Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            }
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "OldImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            },
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "SequenceNumber": "21626200000000067447717181",
                "SizeBytes": 4401,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
        }

    @pytest.fixture
    def session_updated_v1_event_field_add(self):
        yield {
            "eventID": "e29fcf34cf3cce9dff441404e59cfd62",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-west-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1691353296.0,
                "Keys": {"SK": {"S": "SVS309"}, "PK": {"S": "ReInventSession"}},
                "NewImage": {
                    "extraLevel": {"N": "300"},
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            }
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "OldImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            },
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "SequenceNumber": "21626200000000067447717181",
                "SizeBytes": 4401,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
        }

    @pytest.fixture
    def session_updated_v1_event_field_remove(self):
        yield {
            "eventID": "e29fcf34cf3cce9dff441404e59cfd62",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-west-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1691353296.0,
                "Keys": {"SK": {"S": "SVS309"}, "PK": {"S": "ReInventSession"}},
                "NewImage": {
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            }
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "OldImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            },
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "SequenceNumber": "21626200000000067447717181",
                "SizeBytes": 4401,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
        }

    @pytest.fixture
    def session_updated_v1_event_field_change(self):
        yield {
            "eventID": "e29fcf34cf3cce9dff441404e59cfd62",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-west-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1691353296.0,
                "Keys": {"SK": {"S": "SVS309"}, "PK": {"S": "ReInventSession"}},
                "NewImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            }
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "OldImage": {
                    "level": {"N": "400"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            },
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "SequenceNumber": "21626200000000067447717181",
                "SizeBytes": 4401,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
        }

    @pytest.fixture
    def session_updated_v1_event_deep_field_change(self):
        yield {
            "eventID": "e29fcf34cf3cce9dff441404e59cfd62",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-west-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1691353296.0,
                "Keys": {"SK": {"S": "SVS309"}, "PK": {"S": "ReInventSession"}},
                "NewImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOps Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            }
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "OldImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "Serverless Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "DevOps Engineer"},
                            {"S": "Solution/Systems Architect"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                    "description": {
                        "S": "Enterprise-based serverless developers are often subject to..."
                    },
                    "services": {
                        "L": [
                            {"S": "AWS Serverless Application Model (SAM)"},
                            {"S": "AWS Lambda"},
                        ]
                    },
                    "trackName": {"S": "Breakout Session"},
                    "title": {
                        "S": "Improve productivity by shifting more responsibility to developers"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "DevOops Engineer"},
                                    "parentTagName": {"S": "Role"},
                                }
                            },
                        ]
                    },
                    "thirdPartyID": {"S": "SVS309"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": []},
                    "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                    "SK": {"S": "SVS309"},
                    "sessionType": {"S": "Breakout Session"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": []},
                },
                "SequenceNumber": "21626200000000067447717181",
                "SizeBytes": 4401,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
        }

    @pytest.fixture
    def session_removed_v1_event(self):
        yield {
            "eventID": "7bfaf1ad81d238d72a2d341d29f6d778",
            "eventName": "REMOVE",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-west-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1691351787.0,
                "Keys": {"SK": {"S": "CMP201"}, "PK": {"S": "ReInventSession"}},
                "OldImage": {
                    "level": {"N": "200"},
                    "topics": {"L": [{"S": "AI/ML"}, {"S": "Compute"}]},
                    "roles": {
                        "L": [
                            {"S": "Data Scientist"},
                            {"S": "Entrepreneur (Founder/Co-Founder)"},
                            {"S": "Developer/Engineer"},
                        ]
                    },
                    "scheduleUid": {"S": "AD1963B3-7991-45AB-A8D7-005C161DC952"},
                    "description": {
                        "S": "Generative AI can help you reinvent your applications, create entirely new customer experiences, and drive unprecedented levels of productivity. To help you realize the full promise of this transformative technology, Amazon EC2 provides performant, energy-efficient, and cost-effective instances. In this session, learn about the capabilities, benchmarks, and ideal use cases for each of these instances. Hear from AWS customers about how they built, deployed, and scaled large text and image generation models across various products and services using accelerated instances."
                    },
                    "services": {"L": [{"S": "Amazon Elastic Compute Cloud (EC2)"}]},
                    "trackName": {"S": "updated track name"},
                    "title": {
                        "S": "Advancing generative AI innovation with Amazon EC2 accelerated compute"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "A633F4F0-69C9-4D21-880F-79DD248107A9"
                                    },
                                    "parentTagUid": {
                                        "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                    },
                                    "tagName": {"S": "Data Scientist"},
                                    "parentTagName": {"S": "Role"},
                                }
                            },
                        ]
                    },
                    "thirdPartyID": {"S": "CMP201"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": [{"S": "Cross Industry"}]},
                    "sessionUid": {"S": "BC517DF0-1904-49B6-BB63-9D73CFBFF839"},
                    "SK": {"S": "CMP201"},
                    "sessionType": {"S": "updated session type"},
                    "scheduleTrackUid": {"S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {
                        "L": [
                            {"S": "Innovation on AWS"},
                            {"S": "Cost Optimization"},
                            {"S": "Generative AI"},
                        ]
                    },
                },
                "SequenceNumber": "21625900000000067445000406",
                "SizeBytes": 2870,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
        }

    @pytest.fixture
    def session_added_v1_event(self):
        yield {
            "eventID": "a4a636b8b7b19a8d89b6108b5c19a553",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-west-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1691351787.0,
                "Keys": {"SK": {"S": "AUT303"}, "PK": {"S": "ReInventSession"}},
                "NewImage": {
                    "level": {"N": "300"},
                    "topics": {"L": [{"S": "AI/ML"}]},
                    "roles": {
                        "L": [
                            {"S": "Data Scientist"},
                            {"S": "Developer/Engineer"},
                            {"S": "Solution/Systems Architect"},
                        ]
                    },
                    "scheduleUid": {"S": "C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC"},
                    "description": {
                        "S": "<p>Automakers collect hundreds of petabytes of drive data from...</p>"
                    },
                    "services": {"L": [{"S": "Amazon Bedrock"}]},
                    "trackName": {"S": "Builders' Session"},
                    "title": {
                        "S": "Using generative AI to add objects in model training scenarios in ADDF"
                    },
                    "tags": {
                        "L": [
                            {
                                "M": {
                                    "scheduleTagUid": {
                                        "S": "3DC75316-93EB-43DB-972C-594B6A06B18E"
                                    },
                                    "parentTagUid": {
                                        "S": "F2BB2A9C-8783-4072-A0A4-5621D1A481A6"
                                    },
                                    "tagName": {"S": "AI/ML"},
                                    "parentTagName": {"S": "Topic"},
                                }
                            },
                        ]
                    },
                    "thirdPartyID": {"S": "AUT303"},
                    "extraLevel": {"N": "200"},
                    "industries": {"L": [{"S": "Automotive"}]},
                    "sessionUid": {"S": "0BA440C0-4774-40FA-A9B4-582ACB8668DA"},
                    "SK": {"S": "AUT303"},
                    "sessionType": {"S": "standard"},
                    "scheduleTrackUid": {"S": "3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E"},
                    "PK": {"S": "ReInventSession"},
                    "areas_of_interest": {"L": [{"S": "Generative AI"}]},
                },
                "SequenceNumber": "21625800000000067445000336",
                "SizeBytes": 2378,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
        }

    @staticmethod
    @freezegun.freeze_time("2023-01-14")
    def test_handle_ddb_insert_event(session_added_v1_event):
        # 1. ARRANGE
        from .. import index

        index._put_events = MagicMock()

        # 2. ACT
        index.handler({"Records": [session_added_v1_event]}, None)

        # 3. ASSERT
        index._put_events.assert_called_once_with(
            source="ReInventSessionFetcher",
            detail_type="SessionAdded",
            detail=json.dumps(
                {
                    "metadata": {
                        "eventVersion": 1,
                        "eventSource": "ReInventSessionFetcher",
                        "eventType": "SessionAdded",
                        "eventDateTime": "2023-01-14T00:00:00+00:00",
                    },
                    "data": {
                        "level": "300",
                        "topics": ["AI/ML"],
                        "roles": [
                            "Data Scientist",
                            "Developer/Engineer",
                            "Solution/Systems Architect",
                        ],
                        "scheduleUid": "C50C7B1A-FF68-4C97-9AF4-00AE3D6F57BC",
                        "description": "<p>Automakers collect hundreds of petabytes of drive data from...</p>",
                        "services": ["Amazon Bedrock"],
                        "trackName": "Builders' Session",
                        "title": "Using generative AI to add objects in model training scenarios in ADDF",
                        "tags": [
                            {
                                "scheduleTagUid": "3DC75316-93EB-43DB-972C-594B6A06B18E",
                                "parentTagUid": "F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
                                "tagName": "AI/ML",
                                "parentTagName": "Topic",
                            }
                        ],
                        "thirdPartyID": "AUT303",
                        "extraLevel": "200",
                        "industries": ["Automotive"],
                        "sessionUid": "0BA440C0-4774-40FA-A9B4-582ACB8668DA",
                        "SK": "AUT303",
                        "sessionType": "standard",
                        "scheduleTrackUid": "3E4615D2-CDE9-ED11-81DB-A4AC1C44CA4E",
                        "PK": "ReInventSession",
                        "areas_of_interest": ["Generative AI"],
                    },
                }
            ),
            event_bus_name="MockEventBus",
        )

    @staticmethod
    @freezegun.freeze_time("2023-01-14")
    def test_handle_ddb_remove_event(session_removed_v1_event):
        # 1. ARRANGE
        from .. import index

        index._put_events = MagicMock()

        # 2. ACT
        index.handler({"Records": [session_removed_v1_event]}, None)

        # 3. ASSERT
        index._put_events.assert_called_once_with(
            source="ReInventSessionFetcher",
            detail_type="SessionRemoved",
            detail=json.dumps(
                {
                    "metadata": {
                        "eventVersion": 1,
                        "eventSource": "ReInventSessionFetcher",
                        "eventType": "SessionRemoved",
                        "eventDateTime": "2023-01-14T00:00:00+00:00",
                    },
                    "data": {
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
                        "trackName": "updated track name",
                        "title": "Advancing generative AI innovation with Amazon EC2 accelerated compute",
                        "tags": [
                            {
                                "scheduleTagUid": "A633F4F0-69C9-4D21-880F-79DD248107A9",
                                "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                "tagName": "Data Scientist",
                                "parentTagName": "Role",
                            }
                        ],
                        "thirdPartyID": "CMP201",
                        "extraLevel": "200",
                        "industries": ["Cross Industry"],
                        "sessionUid": "BC517DF0-1904-49B6-BB63-9D73CFBFF839",
                        "SK": "CMP201",
                        "sessionType": "updated session type",
                        "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                        "PK": "ReInventSession",
                        "areas_of_interest": [
                            "Innovation on AWS",
                            "Cost Optimization",
                            "Generative AI",
                        ],
                    },
                }
            ),
            event_bus_name="MockEventBus",
        )

    @staticmethod
    @freezegun.freeze_time("2023-01-14")
    def test_handle_ddb_update_list_element_add_event(
        session_updated_v1_event_list_element_add,
    ):
        # 1. ARRANGE
        from .. import index

        index._put_events = MagicMock()

        # 2. ACT
        index.handler({"Records": [session_updated_v1_event_list_element_add]}, None)

        # 3. ASSERT
        index._put_events.assert_called_once_with(
            source="ReInventSessionFetcher",
            detail_type="SessionUpdated",
            detail=json.dumps(
                {
                    "metadata": {
                        "eventVersion": 1,
                        "eventSource": "ReInventSessionFetcher",
                        "eventType": "SessionUpdated",
                        "eventDateTime": "2023-01-14T00:00:00+00:00",
                    },
                    "data": {
                        "old": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "new": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                                "ExtraTest/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "diff": {
                            "added_keys": {},
                            "removed_keys": {},
                            "changed_keys": {
                                "roles": {
                                    "iterable_item_added": {
                                        "root[3]": "ExtraTest/Engineer"
                                    }
                                }
                            },
                        },
                    },
                }
            ),
            event_bus_name="MockEventBus",
        )

    @staticmethod
    @freezegun.freeze_time("2023-01-14")
    def test_handle_ddb_update_list_element_remove_event(
        session_updated_v1_event_list_element_remove,
    ):
        # 1. ARRANGE
        from .. import index

        index._put_events = MagicMock()

        # 2. ACT
        index.handler({"Records": [session_updated_v1_event_list_element_remove]}, None)

        # 3. ASSERT
        index._put_events.assert_called_once_with(
            source="ReInventSessionFetcher",
            detail_type="SessionUpdated",
            detail=json.dumps(
                {
                    "metadata": {
                        "eventVersion": 1,
                        "eventSource": "ReInventSessionFetcher",
                        "eventType": "SessionUpdated",
                        "eventDateTime": "2023-01-14T00:00:00+00:00",
                    },
                    "data": {
                        "old": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "new": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": ["DevOps Engineer", "Solution/Systems Architect"],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "diff": {
                            "added_keys": {},
                            "removed_keys": {},
                            "changed_keys": {
                                "roles": {
                                    "iterable_item_removed": {
                                        "root[2]": "Developer/Engineer"
                                    }
                                }
                            },
                        },
                    },
                }
            ),
            event_bus_name="MockEventBus",
        )

    @staticmethod
    @freezegun.freeze_time("2023-01-14")
    def test_handle_ddb_update_list_element_reorder_event(
        session_updated_v1_event_list_element_reorder,
    ):
        # 1. ARRANGE
        from .. import index

        index._put_events = MagicMock()

        # 2. ACT
        index.handler(
            {"Records": [session_updated_v1_event_list_element_reorder]}, None
        )

        # 3. ASSERT
        index._put_events.assert_called_once_with(
            source="ReInventSessionFetcher",
            detail_type="SessionUpdated",
            detail=json.dumps(
                {
                    "metadata": {
                        "eventVersion": 1,
                        "eventSource": "ReInventSessionFetcher",
                        "eventType": "SessionUpdated",
                        "eventDateTime": "2023-01-14T00:00:00+00:00",
                    },
                    "data": {
                        "old": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": ["DevOps Engineer", "Developer/Engineer"],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "new": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": ["Developer/Engineer", "DevOps Engineer"],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "diff": {
                            "added_keys": {},
                            "removed_keys": {},
                            "changed_keys": {},
                        },
                    },
                }
            ),
            event_bus_name="MockEventBus",
        )

    @staticmethod
    @freezegun.freeze_time("2023-01-14")
    def test_handle_ddb_update_field_add_event(
        session_updated_v1_event_field_add,
    ):
        # 1. ARRANGE
        from .. import index

        index._put_events = MagicMock()

        # 2. ACT
        index.handler({"Records": [session_updated_v1_event_field_add]}, None)

        # 3. ASSERT
        index._put_events.assert_called_once_with(
            source="ReInventSessionFetcher",
            detail_type="SessionUpdated",
            detail=json.dumps(
                {
                    "metadata": {
                        "eventVersion": 1,
                        "eventSource": "ReInventSessionFetcher",
                        "eventType": "SessionUpdated",
                        "eventDateTime": "2023-01-14T00:00:00+00:00",
                    },
                    "data": {
                        "old": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
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
                        "new": {
                            "extraLevel": "200",
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
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
                        "diff": {
                            "added_keys": {"extraLevel": "200"},
                            "removed_keys": {},
                            "changed_keys": {},
                        },
                    },
                }
            ),
            event_bus_name="MockEventBus",
        )

    @staticmethod
    @freezegun.freeze_time("2023-01-14")
    def test_handle_ddb_update_field_remove_event(
        session_updated_v1_event_field_remove,
    ):
        # 1. ARRANGE
        from .. import index

        index._put_events = MagicMock()

        # 2. ACT
        index.handler({"Records": [session_updated_v1_event_field_remove]}, None)

        # 3. ASSERT
        index._put_events.assert_called_once_with(
            source="ReInventSessionFetcher",
            detail_type="SessionUpdated",
            detail=json.dumps(
                {
                    "metadata": {
                        "eventVersion": 1,
                        "eventSource": "ReInventSessionFetcher",
                        "eventType": "SessionUpdated",
                        "eventDateTime": "2023-01-14T00:00:00+00:00",
                    },
                    "data": {
                        "old": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "new": {
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "diff": {
                            "added_keys": {},
                            "removed_keys": {"level": "300"},
                            "changed_keys": {},
                        },
                    },
                }
            ),
            event_bus_name="MockEventBus",
        )

    @staticmethod
    @freezegun.freeze_time("2023-01-14")
    def test_handle_ddb_update_deep_field_change_event(
        session_updated_v1_event_deep_field_change,
    ):
        # 1. ARRANGE
        from .. import index

        index._put_events = MagicMock()

        # 2. ACT
        index.handler({"Records": [session_updated_v1_event_deep_field_change]}, None)

        # 3. ASSERT
        index._put_events.assert_called_once_with(
            source="ReInventSessionFetcher",
            detail_type="SessionUpdated",
            detail=json.dumps(
                {
                    "metadata": {
                        "eventVersion": 1,
                        "eventSource": "ReInventSessionFetcher",
                        "eventType": "SessionUpdated",
                        "eventDateTime": "2023-01-14T00:00:00+00:00",
                    },
                    "data": {
                        "old": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOops Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "new": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "diff": {
                            "added_keys": {},
                            "removed_keys": {},
                            "changed_keys": {
                                "tags": {
                                    "values_changed": {
                                        "root[0]['tagName']": {
                                            "new_value": "DevOps Engineer",
                                            "old_value": "DevOops Engineer",
                                        }
                                    }
                                }
                            },
                        },
                    },
                }
            ),
            event_bus_name="MockEventBus",
        )

    @staticmethod
    @freezegun.freeze_time("2023-01-14")
    def test_handle_ddb_update_field_change_event(
        session_updated_v1_event_field_change,
    ):
        # 1. ARRANGE
        from .. import index

        index._put_events = MagicMock()

        # 2. ACT
        index.handler({"Records": [session_updated_v1_event_field_change]}, None)

        # 3. ASSERT
        index._put_events.assert_called_once_with(
            source="ReInventSessionFetcher",
            detail_type="SessionUpdated",
            detail=json.dumps(
                {
                    "metadata": {
                        "eventVersion": 1,
                        "eventSource": "ReInventSessionFetcher",
                        "eventType": "SessionUpdated",
                        "eventDateTime": "2023-01-14T00:00:00+00:00",
                    },
                    "data": {
                        "old": {
                            "level": "400",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "new": {
                            "level": "300",
                            "topics": ["Serverless Compute"],
                            "roles": [
                                "DevOps Engineer",
                                "Solution/Systems Architect",
                                "Developer/Engineer",
                            ],
                            "scheduleUid": "706791CC-1EB3-4E2C-9C66-008E2342CD9C",
                            "description": "Enterprise-based serverless developers are often subject to...",
                            "services": [
                                "AWS Serverless Application Model (SAM)",
                                "AWS Lambda",
                            ],
                            "trackName": "Breakout Session",
                            "title": "Improve productivity by shifting more responsibility to developers",
                            "tags": [
                                {
                                    "scheduleTagUid": "16A05B04-62C9-45E5-A5AC-79CB47268800",
                                    "parentTagUid": "22A77ABD-348D-4E44-800F-846017E75A5D",
                                    "tagName": "DevOps Engineer",
                                    "parentTagName": "Role",
                                }
                            ],
                            "thirdPartyID": "SVS309",
                            "extraLevel": "200",
                            "industries": [],
                            "sessionUid": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4",
                            "SK": "SVS309",
                            "sessionType": "Breakout Session",
                            "scheduleTrackUid": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E",
                            "PK": "ReInventSession",
                            "areas_of_interest": [],
                        },
                        "diff": {
                            "added_keys": {},
                            "removed_keys": {},
                            "changed_keys": {
                                "level": {
                                    "values_changed": {
                                        "root": {"new_value": "300", "old_value": "400"}
                                    }
                                }
                            },
                        },
                    },
                },
            ),
            event_bus_name="MockEventBus",
        )
