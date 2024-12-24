from dotenv import load_dotenv
from groq import Groq
import re
import os
import json
load_dotenv(verbose=True)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def get_full_details(article):
    prompt = f"""
    I am sending you information in the news
    And fill me json According to the details only
    the news: {article}
    
    The json that needs to be completed
    {{
          "summary": "",
          "attack_type": "",
          "num_perpetrators": "",
          "country": "",
          "region": "",
          "province": "",
          "city": "",
          "latitude": "",
          "longitude": "",
          "num_killed": "",
          "num_wounded": "",
          "property_damage_extent": "",
          "type": "",
          "subtype": "",
          "nationality": "",
          "group": "",
          "weapon": ""
    }}    

    Don't give me back anything but this json
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    groq_output = response.choices[0].message.content.strip()
    try:
        # Extract content between { and } using a regular expression
        match = re.search(r"\{.*\}", groq_output, re.DOTALL)
        if match:
            json_content = match.group(0)
            parsed_response = json.loads(json_content)  # Parse as dict
            if isinstance(parsed_response, dict):
                return parsed_response
        print(f"No valid JSON found in Groq output: {groq_output}")
        return {}
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing Groq response: {e}")
        print(f"Groq raw output: {groq_output}")
        return {}
