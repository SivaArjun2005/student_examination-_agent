
import pdfplumber
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def extract_text_from_pdf(uploaded_file):
    # pdfplumber accepts BytesIO-like uploaded files from Streamlit
    with pdfplumber.open(uploaded_file) as pdf:
        pages = [page.extract_text() for page in pdf.pages if page.extract_text()]
    text = "\n".join(pages)
    return text or ""

def summarize_text(text, sentences_count=5):
    # Fallback if text is short
    if not text or len(text.split()) < 50:
        return text

    # Use Sumy LexRank summarizer (extractive)
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary_sentences = summarizer(parser.document, sentences_count)
    return "\n".join([str(s) for s in summary_sentences])
