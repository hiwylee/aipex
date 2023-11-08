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

    if not os.path.exists("steve-jobs-commencement.txt") :
        print("steve-jobs-commencement.txt not exist")
        exit(1)
    if not os.path.exists("answers.json") :
        print("answers.json not exist")
        exit(1)
    if not os.path.exists("FY23_insurance.pdf") :
        print("FY23_insurance.pdf not exist")
        exit(1)
    rag.loadTxt("answers.json")
    rag.loadTxt("steve-jobs-commencement.txt")
    rag.loadTxt("FY23_insurance.pdf")


    if __debug__ :
        print(" Finishing...")
        
