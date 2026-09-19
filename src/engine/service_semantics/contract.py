"""Phase 4 — semantic contract for the service-facing IR boundary."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
SEMANTIC_CONTRACT_SCHEMA = "service_semantic_contract_v1"
ALLOWED_ACTIONS = frozenset({"DIRECT", "PROXY", "REJECT"})
@dataclass
class ServiceSemanticReport:
    schema: str = SEMANTIC_CONTRACT_SCHEMA
    checked_services: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)
    checked_decisions: int = 0
    duplicate_memberships: int = 0
    violations: list[str] = field(default_factory=list)
    @property
    def all_pass(self) -> bool:
        return not self.violations
    def to_dict(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "checked_services": sorted(self.checked_services, key=str.casefold),
            "checked_rules": sorted(self.checked_rules),
            "checked_decisions": self.checked_decisions,
            "duplicate_memberships": self.duplicate_memberships,
            "violations": sorted(self.violations),
            "all_pass": self.all_pass,
        }
def _add(report: ServiceSemanticReport, message: str) -> None:
    report.violations.append(message)
def validate_service_semantics(ir: dict[str, Any]) -> ServiceSemanticReport:
    report = ServiceSemanticReport()
    if not isinstance(ir, dict):
        _add(report, "IR must be an object")
        return report
    entities = ir.get("entities")
    rules = ir.get("rules")
    memberships = ir.get("memberships")
    decisions = ir.get("decisions")
    if not isinstance(entities, dict):
        _add(report, "entities must be an object")
        entities = {}
    if not isinstance(rules, list):
        _add(report, "rules must be a list")
        rules = []
    if not isinstance(memberships, dict):
        _add(report, "memberships must be an object")
        memberships = {}
    if not isinstance(decisions, list):
        _add(report, "decisions must be a list")
        decisions = []
    universe: set[str] = set()
    for group in ("services", "groups", "aggregates"):
        values = entities.get(group)
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            _add(report, f"entities.{group} must be a string list")
            continue
        normalized = [value.strip() for value in values]
        if len(normalized) != len(set(normalized)):
            _add(report, f"entities.{group} contains duplicates")
        report.checked_services.extend(normalized)
        universe.update(normalized)
    rule_map: dict[str, dict[str, Any]] = {}
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            _add(report, f"rules[{index}] must be an object")
            continue
        rid = rule.get("id")
        if not isinstance(rid, str) or not rid:
            _add(report, f"rules[{index}] missing string id")
            continue
        if rid in rule_map:
            _add(report, f"duplicate rule id: {rid}")
            continue
        rule_map[rid] = rule
        report.checked_rules.append(rid)
    membership_pairs: set[tuple[str, str]] = set()
    for entity, rule_ids in memberships.items():
        if entity not in universe:
            _add(report, f"membership references unknown entity: {entity}")
            continue
        if not isinstance(rule_ids, list):
            _add(report, f"membership for {entity} must be a list")
            continue
        for rid in rule_ids:
            if rid not in rule_map:
                _add(report, f"membership references unknown rule: {entity}:{rid}")
            pair = (entity, str(rid))
            if pair in membership_pairs:
                # Canonical membership preserves repeated source occurrences.
                # Membership semantics are set-like, so duplicate source edges
                # are evidence but not a semantic violation.
                report.duplicate_memberships += 1
            membership_pairs.add(pair)
    seen_decisions: dict[tuple[str, str], str] = {}
    for index, decision in enumerate(decisions):
        report.checked_decisions += 1
        if not isinstance(decision, dict):
            _add(report, f"decisions[{index}] must be an object")
            continue
        rid = decision.get("rule_id")
        action = decision.get("action")
        if rid not in rule_map:
            _add(report, f"decision references unknown rule: {rid}")
        if action not in ALLOWED_ACTIONS:
            _add(report, f"decision has invalid action: {action}")
        entities_for_rule = decision.get("entities", [])
        if not isinstance(entities_for_rule, list) or not all(isinstance(value, str) for value in entities_for_rule):
            _add(report, f"decision[{index}].entities must be a string list")
            entities_for_rule = []
        else:
            entities_for_rule = sorted(set(entities_for_rule), key=str.casefold)
        for entity in entities_for_rule:
            if entity not in universe:
                _add(report, f"decision references unknown entity: {entity}")
        if isinstance(rid, str) and rid in rule_map:
            source = rule_map[rid]
            if decision.get("type") != source.get("type") or decision.get("value") != source.get("value"):
                _add(report, f"decision payload drift for rule: {rid}")
        for entity in entities_for_rule:
            key = (str(rid), entity)
            previous = seen_decisions.get(key)
            if previous is not None and previous != action:
                _add(report, f"conflicting decisions for {rid} in {entity}")
            elif previous is not None:
                _add(report, f"duplicate decision for {rid} in {entity}")
            seen_decisions[key] = str(action)
    semantic_intent = ir.get("semantic_intent")
    if isinstance(semantic_intent, dict) and "applied_count" in semantic_intent:
        applied = semantic_intent.get("applied")
        if isinstance(applied, list) and semantic_intent.get("applied_count") != len(applied):
            _add(report, "semantic_intent.applied_count does not match applied length")
    return report
