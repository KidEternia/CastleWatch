def calculate_risk(
    event_type: str,
    username: str | None,
    recent_event_count: int,
) -> tuple[int, str, str]:
    """
    Calculate a risk score, severity, and detection name.

    recent_event_count includes the event currently being processed.
    """

    score = 0
    detection = "Generic Security Event"

    if event_type == "authentication_failure":
        score += 10
        detection = "Authentication Failure"

        if username and username.lower() in {
            "admin",
            "administrator",
            "root",
        }:
            score += 10

        if recent_event_count >= 5:
            score += 20
            detection = "Possible Brute Force Attack"

        if recent_event_count >= 10:
            score += 20
            detection = "Probable Brute Force Attack"

        if recent_event_count >= 20:
            score += 30
            detection = "Critical Brute Force Attack"

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

    return score, severity, detection