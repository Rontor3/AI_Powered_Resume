from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve the Hugging Face API key from the .env file
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not found in .env file. Make sure to set it up.")

# Initialize the LLM client
def get_llm():
    """
    Initialize the InferenceClient for the Mistral-7B-Instruct model using the Hugging Face API key.
    """
    client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.3", token=API_KEY)
    return client

def extract_relevant_jd(jd_text, client, max_input_token_limit=1024, max_output_token_limit=1024):
    """
    Extract relevant parts of a Job Description (JD) for evaluating a candidate's resume.

    Parameters:
        jd_text (str): The full Job Description text.
        client (InferenceClient): The initialized Hugging Face InferenceClient.
        max_input_token_limit (int): Maximum number of input tokens allowed.
        max_output_token_limit (int): Maximum number of output tokens allowed.

    Returns:
        str: Extracted relevant content or a warning if input exceeds token limits.
    """
    prompt_template = """
    You are an expert HR assistant trained to analyze job descriptions.

    Your task is to extract ONLY the parts of a given Job Description that are relevant for evaluating a candidate's resume. These include:

    - Required skills
    - Responsibilities
    - Work experience
    - Required qualifications
    - Educational background
    - Tools, technologies, or certifications

    **Ignore** sections like:
    - About the company
    - Culture and values
    - Perks and benefits
    - Application process
    - Equal opportunity statements

    Format the extracted content as:

    **Extracted JD Content:**
    [Relevant content only]

    Here is the Job Description:

    {jd_text}
    """
    # Format the prompt
    prompt = prompt_template.format(jd_text=jd_text)
    token_count = len(prompt.split())

    if token_count > max_input_token_limit:
        return f"⚠️ JD too long ({token_count} tokens). Please reduce the input size."

    response = client.text_generation(prompt, max_new_tokens=max_output_token_limit)
    if isinstance(response, dict) and 'generated_text' in response:
        return response['generated_text']
    elif isinstance(response, str):
        return response
    else:
        return "⚠️ Unexpected response format. Check the input or model settings."

def generate_resume_feedback(resume_text, extracted_jd, similarity_score, client, max_input_token_limit=1024, max_output_token_limit=2048):
    """
    Analyze a candidate's resume against a Job Description (JD) and provide feedback.

    Parameters:
        resume_text (str): Candidate's resume text.
        extracted_jd (str): Extracted JD content.
        similarity_score (float): Semantic similarity score (0–1).
        client (InferenceClient): The initialized Hugging Face InferenceClient.
        max_input_token_limit (int): Maximum number of input tokens allowed.
        max_output_token_limit (int): Maximum number of output tokens allowed.

    Returns:
        str: Feedback or a warning if input exceeds token limits.
    """
    prompt_template = """
    You are an expert Resume Evaluator, ATS System, and Career Coach.

    Task: Analyze a candidate's resume against the extracted job description and provide:
    1. ✅ A Matching Score (0–100%) based on the similarity score and content alignment.
    2. 📋 A detailed evaluation report outlining:
        - Matching elements (skills, experience, etc.).
        - Missing elements the resume should include.
    3. ✨ Suggestions for improving the resume to better align with the job description.

    **Similarity Score**: {similarity_score:.2f}

    📄 Resume:
    {resume_text}

    📝 Extracted JD:
    {extracted_jd}
    """
    # Format the prompt
    prompt = prompt_template.format(resume_text=resume_text, extracted_jd=extracted_jd, similarity_score=similarity_score)
    token_count = len(prompt.split())

    if token_count > max_input_token_limit:
        return f"⚠️ Combined input too long ({token_count} tokens). Please reduce the input size."

    response = client.text_generation(prompt, max_new_tokens=max_output_token_limit)
    if isinstance(response, dict) and 'generated_text' in response:
        return response['generated_text']
    elif isinstance(response, str):
        return response
    else:
        return "⚠️ Unexpected response format. Check the input or model settings."

def standalone_resume_feedback(resume_text, client, max_input_token_limit=1024, max_output_token_limit=2048):
    """
    Provide ATS compatibility analysis and suggestions for improving a resume.

    Parameters:
        resume_text (str): Candidate's resume text.
        client (InferenceClient): The initialized Hugging Face InferenceClient.
        max_input_token_limit (int): Maximum number of input tokens allowed.
        max_output_token_limit (int): Maximum number of output tokens allowed.

    Returns:
        str: ATS feedback or a warning if input exceeds token limits.
    """
    prompt_template = """
    You are an ATS (Applicant Tracking System) evaluator.

Assume that every section of the resume is separated by '### Section Name ###' markers. 
These markers indicate a clear visual break in the original resume layout.

Evaluate the resume on the following:
- Content quality (skills, education, work experience)
- Logical order of sections
- Presence or absence of important sections
- Clarity and conciseness
- Overall structure, assuming each '###' represents a proper section gap
- Potential formatting issues inferred from the structure

Give a final ATS friendliness score out of 100. 
Also, suggest improvements.

Here is the resume text:
{resume_text}
    """
    # Format the prompt
    prompt = prompt_template.format(resume_text=resume_text)
    token_count = len(prompt.split())

    if token_count > max_input_token_limit:
        return f"⚠️ Resume too long ({token_count} tokens). Please reduce the input size."

    response = client.text_generation(prompt, max_new_tokens=max_output_token_limit)
    if isinstance(response, dict) and 'generated_text' in response:
        return response['generated_text']
    elif isinstance(response, str):
        return response
    else:
        return "⚠️ Unexpected response format. Check the input or model settings."