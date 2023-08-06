from typing import Any, Dict
from models import ReInventSession


def map_session_to_slack_block(
    session: ReInventSession, change_type: str
) -> Dict[str, Any]:
    match change_type:
        case "SessionUpdated":
            change_type = ":recycle: Updated"
        case "SessionAdded":
            change_type = ":star: Added"
        case "SessionRemoved":
            change_type = ":red_circle: Removed"
        case _:
            raise ValueError(f"Unknown change_type: {change_type}")
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{change_type}:\n {session.title}",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*TrackName* - {session.trackName}"},
                    {
                        "type": "mrkdwn",
                        "text": f"*ThirdPartyID* - {session.thirdPartyID}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*SessionType* - {session.sessionType}",
                    },
                    {"type": "mrkdwn", "text": f"*Level* - {session.level}"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Services* - {', '.join(session.services)}",
                    },
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description*\n{session.description}",
                },
            },
        ]
    }
