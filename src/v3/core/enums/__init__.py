"""V3 enums."""
from __future__ import annotations
from enum import Enum

class RuleType(str, Enum):
    DOMAIN = "domain"
    DOMAIN_SUFFIX = "domain_suffix"
    DOMAIN_KEYWORD = "domain_keyword"
    DOMAIN_REGEX = "domain_regex"
    IP_CIDR = "ip_cidr"
    IP_CIDR6 = "ip_cidr6"

class Action(str, Enum):
    DIRECT = "DIRECT"
    PROXY = "PROXY"
    REJECT = "REJECT"

class ViewMode(str, Enum):
    EXCLUSIVE = "exclusive"
    EFFECTIVE = "effective"
    AGGREGATE = "aggregate"

class EdgeKind(str, Enum):
    MEMBERSHIP = "membership"
    OWNERSHIP = "ownership"
    DEPENDENCY = "dependency"
    INFRASTRUCTURE = "infrastructure"
    ALIAS = "alias"
