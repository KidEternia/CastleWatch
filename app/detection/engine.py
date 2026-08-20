def calculate_risk(
    event_type: str,
    username: str | None,
    recent_event_count: int,
) -> tuple[int, str, str, str | None, str | None, str | None]:
    """
    Calculate risk score, severity, detection name,
    and MITRE ATT&CK mapping.

    recent_event_count includes the event currently being processed.
    """

    score = 0
    detection_name = "Generic Security Event"

    mitre_technique_id = None
    mitre_technique_name = None
    mitre_tactic = None

    if event_type == "authentication_failure":
        score += 10
        detection_name = "Authentication Failure"

        if username and username.lower() in {
            "admin",
            "administrator",
            "root",
        }:
            score += 10

        if recent_event_count >= 5:
            score += 20
            detection_name = "Possible Brute Force Attack"

            mitre_technique_id = "T1110"
            mitre_technique_name = "Brute Force"
            mitre_tactic = "Credential Access"

        if recent_event_count >= 10:
            score += 20
            detection_name = "Probable Brute Force Attack"

        if recent_event_count >= 20:
            score += 30
            detection_name = "Critical Brute Force Attack"

    else:
        score += 5

    score = min(score, 100)

    if score >= 70:
        severity = "critical"
    elif score >= 40:
        severity = "high"
    elif score >= 20:
        severity = "medium"
    else:
        severity = "low"

    return (
        score,
        severity,
        detection_name,
        mitre_technique_id,
        mitre_technique_name,
        mitre_tactic,
    )