from retrieval import Retriever

retriever = Retriever()

query = "logical reasoning test"

results = retriever.search(query)

print("\nResults:")
for r in results:
    print(r)
