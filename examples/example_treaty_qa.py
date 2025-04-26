
# examples/example_treaty_qa.py

from app.models.mistral_model_loader import load_mistral_model

def main():
    # Load the model
    qa_pipeline = load_mistral_model()

    # Sample treaty text
    treaty_text = '''
    RETENTION: The Cedent shall retain USD 1,000,000 each and every loss.
    LIMIT: The Reinsurer shall be liable for 90% of the amount by which each loss exceeds the retention, up to USD 4,000,000 per loss.
    REINSTATEMENTS: One reinstatement is allowed at 100% additional premium.
    '''

    # Example questions
    questions = [
        "What is the retention amount?",
        "How many reinstatements are allowed?",
        "What is the per-loss limit?"
    ]

    # Run QA
    for q in questions:
        input_text = f"Treaty Text: {treaty_text}\n\nQuestion: {q}\nAnswer:"
        answer = qa_pipeline(input_text)[0]['generated_text']
        print(f"Q: {q}\nA: {answer}\n")

if __name__ == "__main__":
    main()
