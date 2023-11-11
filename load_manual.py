from search import RAG
import os
'''

Usage: python load.py file1 file2 file3
'''

if __name__ == "__main__":
    questions = [
           "What did the author liken The Whole Earth Catalog to?",
           "What was Reed College great at?",
#           "What was the author diagnosed with?",
#           "What is the key lesson from this article?",
#           "What did the article say about Michael Jackson?",
           ]
    if __debug__ :
        print(" Loading...")
    import sys

    for v in range(1, len(sys.argv)):
        print(sys.argv[v])
    rag = RAG()

    if not os.path.exists("./doc/database-concepts.pdf") :
        print("not found : ./doc/database-concepts.pdf")
        exit(1)
    if not os.path.exists("./docs/oracle-database-23c-new-features-guide.pdf") :
        print("not found : ./docs/oracle-database-23c-new-features-guide.pdf") 
        exit(1)
    if not os.path.exists("./docs/visualizing-data-and-building-reports-oracle-analytics-cloud.pdf") :
        print("not found : ./docs/visualizing-data-and-building-reports-oracle-analytics-cloud.pdf")
        exit(1)
    rag.loadTxt("./doc/database-concepts.pdf")
    rag.loadTxt("./docs/oracle-database-23c-new-features-guide.pdf")
    rag.loadTxt("./docs/visualizing-data-and-building-reports-oracle-analytics-cloud.pdf")


    if __debug__ :
        print(" Finishing...")
        
