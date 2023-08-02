from typing import List
from pydantic import BaseModel, Field

PARENT_TAG_UIDS = {
    "AREA_OF_INTEREST": "3428EB86-4D79-4EFE-9F33-E911FCC500A4",
    "TOPIC": "F2BB2A9C-8783-4072-A0A4-5621D1A481A6",
    "SERVICES": "7A26869A-A0C9-48CC-9731-541C3AFA9DF4",
    "ROLE": "22A77ABD-348D-4E44-800F-846017E75A5D",
    "INDUSTRY": "B78A961D-DC03-42C9-A32E-DA576734A89E",
    "LEVEL": "2634F5B6-B8E0-4208-92C3-FAE426C930F7",
}

LEVEL_MAPPING = {
    "0F1F69D2-692C-4B25-AEDA-89A0919B8167": 100,
    "79C488FF-B9FC-471C-992C-DE6C35671BDE": 200,
    "2CABCC3D-F2BB-490C-9265-8CBB7660C579": 300,
    "6F2C43D3-196B-4957-82C5-9F46BAC3DE5E": 400,
}


# Define the Pydantic model
class ReInventSessionTag(BaseModel):
    schedule_tag_uid: str = Field(alias="scheduleTagUid")
    tag_name: str = Field(alias="tagName")
    parent_tag_name: str = Field(alias="parentTagName")
    parent_tag_uid: str = Field(alias="parentTagUid")


class ReInventSession(BaseModel):
    session_type: str = Field(alias="sessionType")
    session_id: str = Field(alias="thirdPartyID")
    track_name: str = Field(alias="trackName")
    schedule_track_uid: str = Field(alias="scheduleTrackUid")
    description: str = Field(alias="description")
    schedule_uid: str = Field(alias="scheduleUid")
    session_uid: str = Field(alias="sessionUid")
    title: str = Field(alias="title")
    level: int = -1
    tags: List[ReInventSessionTag]
    topics: List[str] = []
    industries: List[str] = []
    roles: List[str] = []
    areas_of_interest: List[str] = []
    services: List[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for tag in self.tags:
            if tag.schedule_tag_uid in LEVEL_MAPPING:
                self.level = LEVEL_MAPPING[tag.schedule_tag_uid]
            if tag.parent_tag_uid == PARENT_TAG_UIDS["TOPIC"]:
                self.topics.append(tag.tag_name.strip())
            if tag.parent_tag_uid == PARENT_TAG_UIDS["INDUSTRY"]:
                self.industries.append(tag.tag_name.strip())
            if tag.parent_tag_uid == PARENT_TAG_UIDS["ROLE"]:
                self.roles.append(tag.tag_name.strip())
            if tag.parent_tag_uid == PARENT_TAG_UIDS["AREA_OF_INTEREST"]:
                self.areas_of_interest.append(tag.tag_name.strip())
            if tag.parent_tag_uid == PARENT_TAG_UIDS["SERVICES"]:
                self.services.append(tag.tag_name.strip())
            if tag.parent_tag_uid not in PARENT_TAG_UIDS.values():
                print(f"Did not find Parent tag UID for '{tag.parent_tag_name}'")
