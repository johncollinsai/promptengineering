import asyncio
import httpx
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

    if modality == "raw":
        intro_sentence = f"This response for {prompt} is a raw response from the GPT-4 model:"
        user_prompt = f"Please generate a response about {prompt} from the perspective of a business analyst. Start with this introduction sentence: '{intro_sentence}' Then list the most important business analysis insights using the bullet point format • "
    elif modality == "engineered":
        intro_sentence = f"This response for {prompt} has been engineered to provide a cleaner and more specfic response. In this case, we are seeking to obtain information regarding the financial status of {prompt}:"
        user_prompt = f"""Please generate a response about {prompt} from the perspective of an financial analyst. Start with this introduction sentence: '{intro_sentence}'.  
        ASSETS & LIABILITIES
        List 4 recent and most important asset and liability facts for {prompt} using the bullet point format •
        CASHFLOWS & LIQUIDITY
        List 4 recent insights regarding cashflows and liquidity information for {prompt} using the bullet point format •
        KEY FINANCIAL RATIOS
        List the 4 most important financial ratios for {prompt} using the bullet point format •
        """
    else:
        raise ValueError("Modality must be one of 'business analyst', 'investigator', or 'financial analyst'.")
    

    loop = asyncio.get_event_loop()
    openai.api_key = api_key

    def create_chat_completion():
        return openai.ChatCompletion.create(
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

    # Use asyncio.run() here to execute the async logic
    response = asyncio.run(loop.run_in_executor(None, create_chat_completion))

    print("GPT-4 Response:", response)  # print statements to see the values of variables and the response from the GPT-4 API

    final_response = response['choices'][0]['message']['content']
    return final_response.strip()
