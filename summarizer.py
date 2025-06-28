from transformers import pipeline

# Load once globally
summarizer = pipeline('summarization',model="facebook/bart-large-cnn")

def summarize_paragraphs(paragraph):
    max_input_length = 1000
    if len(paragraph) > max_input_length:
        paragraph = paragraph[:max_input_length]

    summary = summarizer(paragraph, max_length=250, min_length=100, do_sample=False)
    return summary[0]['summary_text']
