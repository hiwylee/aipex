from search import RAG

if __name__ == "__main__":
    if __debug__ :
        print(" Staring...")
    rag = RAG()

    answer = rag.chat("oracle 23c new features")
    print(answer)

    if __debug__ :
        print(" Finishing...")
