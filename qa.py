from search import RAG

if __name__ == "__main__":
    if __debug__ :
        print(" Staring...")
    rag = RAG()

    print("\n>>>>>>>>>>> from steve jobs commenecment >>>>>>>>>>.\n")
    answer, source = rag.QA("what was uncle jesse's original last name on full house")
    print("\n>>>>>>>>>>> from answers.json >>>>>>>>>>.\n")
    # see answer : https://github.com/openai/openai-cookbook/blob/main/examples/vector_databases/qdrant/QA_with_Langchain_Qdrant_and_OpenAI.ipynb
    answer, source = rag.QA("where do frankenstein and the monster first meet")
    answer, source = rag.QA("who are the actors in fast and furious")
    answer, source = rag.QA("properties of red black tree in data structure")
    answer, source = rag.QA("who designed the national coat of arms of south africa")
    answer, source = rag.QA("caravaggio's death of the virgin pamela askew")

    if __debug__ :
        print(" Finishing...")
