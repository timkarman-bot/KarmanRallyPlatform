from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Dict, Optional

DEFAULT_WAIVER_TEMPLATE = """
WAIVER AND HOLD HARMLESS AGREEMENT

By participating in this event, I acknowledge and agree to the following:

1. Assumption of Risk
I understand that participation in a car show, cruise, parade, exhibition, meet, or related event involves inherent risks, including but not limited to personal injury, property damage, vehicle damage, theft, fire, weather-related hazards, road or surface conditions, and the acts or omissions of other participants, spectators, vendors, volunteers, or third parties. I voluntarily assume all such risks.

2. Release of Liability
In consideration of being permitted to participate in this event, I release, waive, discharge, and hold harmless {{ release_parties }} and each of their respective owners, officers, directors, members, managers, employees, agents, representatives, volunteers, successors, assigns, sponsors, and affiliates from and against any and all claims, liabilities, damages, losses, demands, causes of action, costs, and expenses arising out of or related to my participation in the event, including claims for personal injury, death, property damage, or economic loss, to the fullest extent permitted by law.

3. Indemnification
I agree to indemnify, defend, and hold harmless {{ release_parties }} and the other released parties from and against any claim, demand, suit, loss, liability, damage, cost, or expense, including reasonable attorney fees, arising out of or related to my acts, omissions, conduct, vehicle, passengers, or participation in the event.

4. Vehicle Responsibility
I certify that any vehicle I bring or operate at the event is under my lawful control, is properly insured as required by applicable law, and is in reasonably safe operating condition. I agree to operate my vehicle safely and responsibly at all times.

5. Rules and Compliance
I agree to follow all posted rules, event instructions, venue requirements, and applicable local, state, and federal laws. I understand that unsafe, reckless, disruptive, or non-compliant behavior may result in removal from the event without refund.

6. No Custody or Bailment
I understand that no released party is assuming custody, control, storage responsibility, or bailment obligations for my vehicle or personal property.

7. Photography and Media Release
I grant permission for photographs, video, and other media depicting me, my passengers, and/or my vehicle at the event to be used for lawful promotional, editorial, archival, and marketing purposes without compensation.

{% if charity_name %}
8. Charity Acknowledgment
I understand that this event includes or supports {{ charity_name }}{% if charity_description %} ({{ charity_description }}){% endif %}. I understand that any charitable, fundraising, or donation-related component of the event is subject to event rules and applicable law, and no guarantee is made as to fundraising outcome.
{% endif %}

9. Venue and Premises
I understand that this event is taking place at {{ venue_name }}{% if venue_address_full %}, located at {{ venue_address_full }}{% endif %}. I agree to respect the venue, its personnel, its policies, and the safety of all persons on or near the premises.

10. Right to Refuse or Remove
The event organizer reserves the right to refuse entry to, or remove, any participant, vehicle, guest, or related person for safety, misconduct, rule violations, legal compliance concerns, or conduct inconsistent with the event.

11. Binding Agreement
I have read this waiver carefully. I understand that by signing it, I am giving up important legal rights. I sign it voluntarily and intend it to be binding on me, my heirs, estate, legal representatives, and assigns.

Organizer: {{ organizer_name }}
Venue: {{ venue_name }}{% if venue_address_full %} — {{ venue_address_full }}{% endif %}
{% if charity_name %}Charity: {{ charity_name }}{% if charity_description %} — {{ charity_description }}{% endif %}{% endif %}
"""

DEFAULT_BUILDER_CONFIG: Dict[str, Any] = {
    "preset_key": "standard",
    "include_assumption_of_risk": True,
    "include_release_of_liability": True,
    "include_indemnification": True,
    "include_vehicle_responsibility": True,
    "include_rules_compliance": True,
    "include_no_custody": True,
    "include_media_release": True,
    "include_charity_clause": True,
    "include_venue_clause": True,
    "include_right_to_remove": True,
    "custom_clause": "",
    "use_advanced_editor": False,
}

PRESET_LABELS = {
    "standard": "Standard Car Show",
    "charity": "Charity Show",
    "parade": "Parade / Cruise",
    "vendor": "Vendor",
    "volunteer": "Volunteer",
}


def _clean(value: Optional[Any]) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_builder_config(raw: Any) -> Dict[str, Any]:
    cfg: Dict[str, Any] = dict(DEFAULT_BUILDER_CONFIG)
    parsed: Dict[str, Any] = {}
    if isinstance(raw, dict):
        parsed = raw
    elif isinstance(raw, str) and raw.strip():
        try:
            loaded = json.loads(raw)
            if isinstance(loaded, dict):
                parsed = loaded
        except Exception:
            parsed = {}

    for key, default in DEFAULT_BUILDER_CONFIG.items():
        value = parsed.get(key, default)
        if isinstance(default, bool):
            cfg[key] = bool(value)
        else:
            cfg[key] = _clean(value)

    preset = cfg.get("preset_key") or "standard"
    if preset not in PRESET_LABELS:
        cfg["preset_key"] = "standard"
    return cfg


def builder_config_to_json(config: Dict[str, Any]) -> str:
    return json.dumps(normalize_builder_config(config), separators=(",", ":"), sort_keys=True)


def sample_preview_show(include_charity: bool = True) -> Dict[str, str]:
    return {
        "id": 0,
        "organizer_name": "Sample Organizer LLC",
        "venue_name": "Sample Venue",
        "venue_address_line1": "123 Main Street",
        "venue_address_line2": "",
        "venue_city": "Kansas City",
        "venue_state": "MO",
        "venue_zip": "64101",
        "charity_name": "Saving 22" if include_charity else "",
        "charity_description": "Veteran suicide awareness" if include_charity else "",
    }


def waiver_context_from_show(show: Dict[str, Any]) -> Dict[str, str]:
    organizer_name = _clean(show.get("organizer_name"))
    venue_name = _clean(show.get("venue_name"))
    charity_name = _clean(show.get("charity_name"))
    charity_description = _clean(show.get("charity_description"))
    address_parts = [
        _clean(show.get("venue_address_line1")),
        _clean(show.get("venue_address_line2")),
        _clean(show.get("venue_city")),
        _clean(show.get("venue_state")),
        _clean(show.get("venue_zip")),
    ]
    venue_address_full = ", ".join([p for p in address_parts if p])
    release_parties_list = [p for p in [organizer_name, venue_name, charity_name] if p]
    release_parties = ", ".join(release_parties_list)
    return {
        "organizer_name": organizer_name,
        "venue_name": venue_name,
        "venue_address_full": venue_address_full,
        "charity_name": charity_name,
        "charity_description": charity_description,
        "release_parties": release_parties,
    }


def validate_waiver_show_fields(show: Dict[str, Any]) -> Optional[str]:
    if not _clean(show.get("organizer_name")):
        return "Organizer name is required."
    if not _clean(show.get("venue_name")):
        return "Venue name is required."
    if not _clean(show.get("venue_address_line1")):
        return "Venue address line 1 is required."
    if not _clean(show.get("venue_city")):
        return "Venue city is required."
    if not _clean(show.get("venue_state")):
        return "Venue state is required."
    if not _clean(show.get("venue_zip")):
        return "Venue ZIP is required."
    return None


def _numbered_section(num: int, heading: str, body: str) -> str:
    return f"{num}. {heading}\n{body.strip()}"


def build_waiver_template_from_builder(config: Dict[str, Any]) -> str:
    cfg = normalize_builder_config(config)
    sections = []
    n = 1

    if cfg["include_assumption_of_risk"]:
        sections.append(_numbered_section(n, "Assumption of Risk", "I understand that participation in a car show, cruise, parade, exhibition, meet, or related event involves inherent risks, including but not limited to personal injury, property damage, vehicle damage, theft, fire, weather-related hazards, road or surface conditions, and the acts or omissions of other participants, spectators, vendors, volunteers, or third parties. I voluntarily assume all such risks."))
        n += 1

    if cfg["include_release_of_liability"]:
        sections.append(_numbered_section(n, "Release of Liability", "In consideration of being permitted to participate in this event, I release, waive, discharge, and hold harmless {{ release_parties }} and each of their respective owners, officers, directors, members, managers, employees, agents, representatives, volunteers, successors, assigns, sponsors, and affiliates from and against any and all claims, liabilities, damages, losses, demands, causes of action, costs, and expenses arising out of or related to my participation in the event, including claims for personal injury, death, property damage, or economic loss, to the fullest extent permitted by law."))
        n += 1

    if cfg["include_indemnification"]:
        sections.append(_numbered_section(n, "Indemnification", "I agree to indemnify, defend, and hold harmless {{ release_parties }} and the other released parties from and against any claim, demand, suit, loss, liability, damage, cost, or expense, including reasonable attorney fees, arising out of or related to my acts, omissions, conduct, vehicle, passengers, or participation in the event."))
        n += 1

    if cfg["include_vehicle_responsibility"]:
        sections.append(_numbered_section(n, "Vehicle Responsibility", "I certify that any vehicle I bring or operate at the event is under my lawful control, is properly insured as required by applicable law, and is in reasonably safe operating condition. I agree to operate my vehicle safely and responsibly at all times."))
        n += 1

    if cfg["include_rules_compliance"]:
        sections.append(_numbered_section(n, "Rules and Compliance", "I agree to follow all posted rules, event instructions, venue requirements, and applicable local, state, and federal laws. I understand that unsafe, reckless, disruptive, or non-compliant behavior may result in removal from the event without refund."))
        n += 1

    if cfg["include_no_custody"]:
        sections.append(_numbered_section(n, "No Custody or Bailment", "I understand that no released party is assuming custody, control, storage responsibility, or bailment obligations for my vehicle or personal property."))
        n += 1

    if cfg["include_media_release"]:
        sections.append(_numbered_section(n, "Photography and Media Release", "I grant permission for photographs, video, and other media depicting me, my passengers, and/or my vehicle at the event to be used for lawful promotional, editorial, archival, and marketing purposes without compensation."))
        n += 1

    if cfg["include_charity_clause"]:
        sections.append("{% if charity_name %}\n" + _numbered_section(n, "Charity Acknowledgment", "I understand that this event includes or supports {{ charity_name }}{% if charity_description %} ({{ charity_description }}){% endif %}. I understand that any charitable, fundraising, or donation-related component of the event is subject to event rules and applicable law, and no guarantee is made as to fundraising outcome.") + "\n{% endif %}")
        n += 1

    if cfg["include_venue_clause"]:
        sections.append(_numbered_section(n, "Venue and Premises", "I understand that this event is taking place at {{ venue_name }}{% if venue_address_full %}, located at {{ venue_address_full }}{% endif %}. I agree to respect the venue, its personnel, its policies, and the safety of all persons on or near the premises."))
        n += 1

    if cfg["include_right_to_remove"]:
        sections.append(_numbered_section(n, "Right to Refuse or Remove", "The event organizer reserves the right to refuse entry to, or remove, any participant, vehicle, guest, or related person for safety, misconduct, rule violations, legal compliance concerns, or conduct inconsistent with the event."))
        n += 1

    custom_clause = _clean(cfg.get("custom_clause"))
    if custom_clause:
        sections.append(_numbered_section(n, "Additional Event Terms", custom_clause))
        n += 1

    sections.append(_numbered_section(n, "Binding Agreement", "I have read this waiver carefully. I understand that by signing it, I am giving up important legal rights. I sign it voluntarily and intend it to be binding on me, my heirs, estate, legal representatives, and assigns."))

    footer = "Organizer: {{ organizer_name }}\nVenue: {{ venue_name }}{% if venue_address_full %} — {{ venue_address_full }}{% endif %}\n{% if charity_name %}Charity: {{ charity_name }}{% if charity_description %} — {{ charity_description }}{% endif %}{% endif %}"

    return _normalize_rendered_text("\n\n".join([
        "WAIVER AND HOLD HARMLESS AGREEMENT",
        "By participating in this event, I acknowledge and agree to the following:",
        "\n\n".join(sections),
        footer,
    ]))


def preview_text_from_builder(config: Dict[str, Any]) -> str:
    cfg = normalize_builder_config(config)
    template = build_waiver_template_from_builder(cfg)
    show = sample_preview_show(include_charity=cfg.get("include_charity_clause", True))
    return render_waiver_text(template, show)


def _render_conditionals(template: str, context: Dict[str, str]) -> str:
    pattern = re.compile(r"{%\s*if\s+([a-zA-Z0-9_]+)\s*%}(.*?){%\s*endif\s*%}", flags=re.DOTALL)
    while True:
        match = pattern.search(template)
        if not match:
            break
        key = match.group(1)
        block = match.group(2)
        replacement = block if _clean(context.get(key)) else ""
        template = template[:match.start()] + replacement + template[match.end():]
    return template


def _render_placeholders(template: str, context: Dict[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        return _clean(context.get(key))

    return re.sub(r"{{\s*([a-zA-Z0-9_]+)\s*}}", repl, template)


def _normalize_rendered_text(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    out = []
    blank_streak = 0
    for line in lines:
        if line.strip():
            out.append(line)
            blank_streak = 0
        else:
            blank_streak += 1
            if blank_streak <= 1:
                out.append("")
    return "\n".join(out).strip()


def render_waiver_text(template_body: str, show: Dict[str, Any]) -> str:
    context = waiver_context_from_show(show)
    rendered = _render_conditionals(template_body, context)
    rendered = _render_placeholders(rendered, context)
    return _normalize_rendered_text(rendered)


def waiver_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
