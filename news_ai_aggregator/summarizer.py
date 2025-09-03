import os
import google.generativeai as genai

# --- IMPORTANT ---
# For the summarizer to work, you need a Google Gemini API key.
# 1. Get your key from Google AI Studio: https://aistudio.google.com/app/apikey
# 2. Set it as an environment variable named 'GEMINI_API_KEY'.
#    In your terminal, run: export GEMINI_API_KEY='YOUR_API_KEY'
#    (For Windows, use: set GEMINI_API_KEY=YOUR_API_KEY)
# -----------------

API_KEY = os.getenv("GEMINI_API_KEY")

def summarize_text(text_to_summarize: str) -> str:
    """
    Summarizes the given text using the Gemini API.
    """
    if not API_KEY:
        return "Error: GEMINI_API_KEY is not set. Please set the environment variable."

    if not text_to_summarize or not isinstance(text_to_summarize, str) or len(text_to_summarize.strip()) == 0:
        return "No text provided to summarize."

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt = (
            "You are an expert news summarizer. "
            "Provide a concise, easy-to-read summary of the following article. "
            "Focus on the key points and main takeaways. The summary should be about 3-4 sentences long."
            "\n\n---\n\n"
            f"ARTICLE: {text_to_summarize}"
        )

        response = model.generate_content(prompt)

        # Check if the response has text, otherwise return a helpful message
        if response.text:
            return response.text
        else:
            # This can happen if the content is blocked or there's another issue
            return "Summarization failed. The API returned an empty response. This could be due to content safety filters."

    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return f"Could not summarize the text due to an API error. Please check your API key and network connection."

if __name__ == '__main__':
    # This is a test block that runs when you execute the script directly
    print("Testing the summarizer...")

    # To test, you must have your GEMINI_API_KEY environment variable set.
    if not API_KEY:
        print("Cannot run test: GEMINI_API_KEY environment variable not set.")
    else:
        sample_text = """
        The tech industry saw a major shift today as a new AI model was released,
        claiming to outperform all existing models in creative writing tasks.
        The model, named 'Muse', was developed by a startup that has been operating in stealth mode for three years.
        Early benchmarks show a 40% improvement in story coherence and character consistency.
        However, some experts are skeptical, pointing out that the training data used for Muse has not been disclosed,
        raising ethical concerns about potential biases. The company plans to release a limited public beta next month.
        """
        print("\n--- Sample Article ---")
        print(sample_text)

        summary = summarize_text(sample_text)

        print("\n--- Generated Summary ---")
        print(summary)
