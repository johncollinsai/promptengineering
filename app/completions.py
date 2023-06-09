import requests
import os
import openai
import re
from .validatename import validate_company_name_gpt

def get_api_key():
    api_key = os.environ["OPENAI_API_KEY"]
    openai.api_key = api_key    # set api key for the openai library
    return api_key

api_key = get_api_key()

def generate_gpt4_response_raw(prompt, api_key):
    print("About to call validate_company_name_gpt")
    is_valid = validate_company_name_gpt(prompt, "raw", api_key)
    if not is_valid:
        raise ValueError(f"Invalid company name: {prompt}")

    intro_sentence = f"This response for {prompt} is a raw response from the GPT-4 model:"
    user_prompt = f"Please generate a response about {prompt}. Start with this introduction sentence: '{intro_sentence}'"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.3,  # Decrease temperature to make output more conservative
    )

    print("GPT-4 Response:", response)
    final_response = response.choices[0]["message"]["content"]
    return final_response.strip()


def generate_gpt4_response_engineered(prompt, api_key):
    print("About to call validate_company_name_gpt")
    is_valid = validate_company_name_gpt(prompt, "engineered", api_key)
    if not is_valid:
        raise ValueError(f"Invalid company name: {prompt}")

    intro_sentence = f"This response for {prompt} has been engineered to provide a more targeted response. In this case, we are seeking to obtain information regarding the financial status of {prompt}:"
    user_prompt = f"""Please generate a response about {prompt} from the perspective of an financial analyst. Start with this introduction sentence: '{intro_sentence}'.  
    ASSETS & LIABILITIES
    List 4 recent and most important asset and liability facts for {prompt} using the bullet point format •
    CASHFLOWS & LIQUIDITY
    List 4 recent insights regarding cashflows and liquidity information for {prompt} using the bullet point format •
    KEY FINANCIAL RATIOS
    List the 4 most important financial ratios for {prompt} using the bullet point format •
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.3,  # Decrease temperature to make output more conservative
    )

    print("GPT-4 Response:", response)
    final_response = response.choices[0]["message"]["content"]
    return final_response.strip()


