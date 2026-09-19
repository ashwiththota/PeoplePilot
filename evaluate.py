"""
Run the correctness evaluation and 
upload the results to LangSmith

Run with : python evaluate.py
"""

from hr_assistant.evaluation import run_evaluation

def main():
    print("RUNNING THE HR POLICY ASSISTANT EVAL....")
    results = run_evaluation()
    print("Done — open your LangSmith and see your experiment in LangSmith")
    print(results)

if __name__ == "__main__":
    main()