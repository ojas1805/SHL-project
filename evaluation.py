from retrieval import retrieve

# -----------------------------
# Test Queries (C1-C10 inspired)
# -----------------------------
test_cases = [
    {
        "query": "Python developer with coding skills",
        "expected": ["Python (New)", "Automata Pro (New)"]
    },
    {
        "query": "Sales manager",
        "expected": ["Sales", "OPQ"]
    },
    {
        "query": "Graduate management trainee",
        "expected": ["Graduate", "Verify"]
    },
    {
        "query": "Senior leadership",
        "expected": ["Leadership", "Enterprise Leadership"]
    },
    {
        "query": "Excel administrator",
        "expected": ["Microsoft Excel", "Workplace Administration"]
    }
]


def precision_at_k(results, expected, k):
    hits = 0

    for item in results[:k]:
        name = item["name"].lower()

        for keyword in expected:
            if keyword.lower() in name:
                hits += 1
                break

    return hits / k


def reciprocal_rank(results, expected):
    for i, item in enumerate(results):

        name = item["name"].lower()

        for keyword in expected:
            if keyword.lower() in name:
                return 1 / (i + 1)

    return 0


precision5 = []
precision10 = []
mrr = []

print("=" * 60)
print("SHL RECOMMENDER EVALUATION")
print("=" * 60)

for test in test_cases:

    results = retrieve(test["query"], top_k=10)

    p5 = precision_at_k(results, test["expected"], 5)
    p10 = precision_at_k(results, test["expected"], 10)
    rr = reciprocal_rank(results, test["expected"])

    precision5.append(p5)
    precision10.append(p10)
    mrr.append(rr)

    print()
    print("Query:", test["query"])
    print("Precision@5 :", round(p5, 2))
    print("Precision@10:", round(p10, 2))
    print("MRR          :", round(rr, 2))

print("\n" + "=" * 60)
print("AVERAGE RESULTS")
print("=" * 60)

print("Average Precision@5 :", round(sum(precision5) / len(precision5), 2))
print("Average Precision@10:", round(sum(precision10) / len(precision10), 2))
print("Average MRR          :", round(sum(mrr) / len(mrr), 2))