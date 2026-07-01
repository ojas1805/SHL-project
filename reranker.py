def rerank(results, query):
    q = query.lower()

    boosts = []

    # C1 Leadership
    if any(x in q for x in ["leadership", "leader", "executive", "director"]):
        boosts = [
            "OPQ32r",
            "OPQ Leadership Report",
            "OPQ Universal Competency Report",
            "Enterprise Leadership"
        ]

    # C2/C9 Software
    elif any(x in q for x in ["python", "java", "rust", "spring", "sql"]):
        boosts = [
            "Python",
            "Java",
            "Automata",
            "Programming",
            "Coding"
        ]

    # C3 Contact Centre
    elif any(x in q for x in ["customer", "contact centre", "call center"]):
        boosts = [
            "Customer",
            "Contact",
            "Service",
            "OPQ32r"
        ]

    # C4 Graduate Finance
    elif any(x in q for x in ["graduate", "finance"]):
        boosts = [
            "Financial",
            "Numerical",
            "OPQ32r",
            "Graduate"
        ]

    # C5 Sales
    elif "sales" in q:
        boosts = [
            "Global Skills",
            "OPQ MQ Sales",
            "Sales Transformation",
            "OPQ32r"
        ]

    # C6 Safety
    elif any(x in q for x in ["safety", "plant", "chemical"]):
        boosts = [
            "Dependability",
            "Safety",
            "Workplace Health"
        ]

    # C7 Healthcare
    elif any(x in q for x in ["health", "medical", "hipaa"]):
        boosts = [
            "HIPAA",
            "Medical",
            "Dependability",
            "OPQ32r"
        ]

    ranked = []

    for item in results:
        score = 0

        text = (
            item.get("name", "") + " " +
            item.get("description", "")
        ).lower()

        for b in boosts:
            if b.lower() in text:
                score += 1

        ranked.append((score, item))

    ranked.sort(key=lambda x: x[0], reverse=True)

    return [x[1] for x in ranked]