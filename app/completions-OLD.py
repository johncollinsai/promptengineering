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

def generate_gpt4_response(prompt, modality, api_key):
    is_valid = validate_company_name_gpt(prompt, modality, api_key)
    if not is_valid:
        raise ValueError(f"Invalid company name: {prompt}")

    if modality == "business analyst":
        intro_sentence = f"This preliminary business analysis of {prompt} has identified the following key insights:"
        user_prompt = f"Please generate a response about {prompt} from the perspective of a business analyst. Start with this introduction sentence: '{intro_sentence}' Then list the most important business analysis insights using the bullet point format • "
    elif modality == "financial analyst":
        intro_sentence = f"This preliminary financial analysis of {prompt} reports upon its assets and liabilities, cashflows and liquidity, and provides 4 key ratios for the company:"
        user_prompt = f"""Please generate a response about {prompt} from the perspective of an financial analyst. Start with this introduction sentence: '{intro_sentence}'.  
        ASSETS & LIABILITIES
        List 4 recent and most important asset and liability facts for {prompt} using the bullet point format •
        CASHFLOWS & LIQUIDITY
        List 4 recent insights regarding cashflows and liquidity information for {prompt} using the bullet point format •
        KEY FINANCIAL RATIOS
        List the 4 most important financial ratios for {prompt} using the bullet point format •
        """
    elif modality == "investigator":
        intro_sentence = f"This preliminary investigation of {prompt} has examined general investigative, corporate, and compliance information, and compiled the following results:"
        user_prompt = f"""Please generate a response about {prompt} from the perspective of an investigator. Start with this introduction sentence: '{intro_sentence}'.
        GENERAL INVESTIGATIVE INFORMATION
        List 4 things that recent investigations have revealed for {prompt} using the bullet point format •
        CORPORATE INFORMATION
        List the 4 most important corporate facts for {prompt} using the bullet point format •
        COMPLIANCE INFORMATION
        List the 4 most important compliance findings for {prompt} using the bullet point format •
        """
    else:
        raise ValueError("Modality must be one of 'business analyst', 'investigator', or 'financial analyst'.")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a {modality}."},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.3,  # Decrease temperature to make output more conservative
    )

    print("GPT-4 Response:", response)  # print statements to see the values of variables and the response from the GPT-4 API
    final_response = response.choices[0]["message"]["content"]
    return final_response.strip()
