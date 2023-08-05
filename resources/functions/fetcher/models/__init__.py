from decimal import Decimal
from typing import List, Any, Dict
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
    scheduleTagUid: str
    tagName: str
    parentTagName: str
    parentTagUid: str


class ReInventSession(BaseModel):
    sessionType: str
    thirdPartyID: str
    trackName: str
    scheduleTrackUid: str
    description: str
    scheduleUid: str
    sessionUid: str
    title: str
    level: Decimal = -1
    tags: List[ReInventSessionTag]
    topics: List[str] = []
    industries: List[str] = []
    roles: List[str] = []
    areas_of_interest: List[str] = []
    services: List[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for tag in self.tags:
            if tag.scheduleTagUid in LEVEL_MAPPING:
                self.level = LEVEL_MAPPING[tag.scheduleTagUid]

            new_tag_name = tag.tagName.strip()

            # Fill lists
            if tag.parentTagUid == PARENT_TAG_UIDS["TOPIC"]:
                if new_tag_name not in self.topics:
                    self.topics.append(new_tag_name)

            if tag.parentTagUid == PARENT_TAG_UIDS["INDUSTRY"]:
                if new_tag_name not in self.industries:
                    self.industries.append(new_tag_name)

            if tag.parentTagUid == PARENT_TAG_UIDS["ROLE"]:
                if new_tag_name not in self.roles:
                    self.roles.append(new_tag_name)

            if tag.parentTagUid == PARENT_TAG_UIDS["AREA_OF_INTEREST"]:
                if new_tag_name not in self.areas_of_interest:
                    self.areas_of_interest.append(new_tag_name)

            if tag.parentTagUid == PARENT_TAG_UIDS["SERVICES"]:
                if new_tag_name not in self.services:
                    self.services.append(new_tag_name)

            # Report missing mappings
            if tag.parentTagUid not in PARENT_TAG_UIDS.values():
                print(f"Did not find Parent tag UID for '{tag.parentTagName}'")


class ReInventSessionFieldDiff(BaseModel):
    field: str
    old_value: Any
    new_value: Any


class ReInventSessionDiff(BaseModel):
    old_session: ReInventSession
    new_session: ReInventSession
    changed_fields: List[ReInventSessionFieldDiff]


class ReInventSessionListDiff(BaseModel):
    added_sessions: Dict[str, ReInventSession]
    removed_sessions: Dict[str, ReInventSession]
    updated_sessions: Dict[str, ReInventSessionDiff]
