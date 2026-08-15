def calculate_compatibility_score(profile, candidate):
    preference = getattr(profile, "preference", None)
    if preference is None:
        return 0, {"note": "No partner preference configured."}

    score = 0
    breakdown = {"age": 0, "religion": 0, "community": 0, "location": 0}

    if candidate.age and preference.min_age <= candidate.age <= preference.max_age:
        breakdown["age"] = 30
        score += 30

    if preference.preferred_religion:
        if candidate.religion and candidate.religion.lower() == preference.preferred_religion.lower():
            breakdown["religion"] = 25
            score += 25
    else:
        breakdown["religion"] = 15
        score += 15

    if preference.preferred_community:
        candidate_community = candidate.community.name if candidate.community else ""
        if candidate_community.lower() == preference.preferred_community.lower():
            breakdown["community"] = 20
            score += 20
    else:
        breakdown["community"] = 10
        score += 10

    if preference.preferred_location:
        candidate_location = candidate.current_location.city if candidate.current_location else ""
        if candidate_location.lower() == preference.preferred_location.lower():
            breakdown["location"] = 25
            score += 25
    else:
        breakdown["location"] = 10
        score += 10

    return min(score, 100), breakdown
