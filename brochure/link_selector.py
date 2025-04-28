from openai import OpenAI
import json
import os
from brochure.web_scraper import Website
from config import MODEL, OPENAI_API_KEY
import logging


openai = OpenAI(api_key=OPENAI_API_KEY)


# Define system prompt for the useful link selector agent
link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""

# Define function to generate user prompt for link selector agent
def get_links_user_prompt(website):
    logging.info("Defining user prompt for link selector agent")
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt



# Agent for selecting useful link for brochure
def get_useful_links_with_openai(url):
    website = Website(url)

    logging.info("Generating useful links with GPT-4o-mini")
    response = openai.chat.completions.create(
        model = MODEL,
        messages = [
            {"role":"system", "content":link_system_prompt},
            {"role":"user", "content":get_links_user_prompt(website)}
        ],
        response_format={"type":"json_object"}
    )
    result = response.choices[0].message.content
    logging.info("Generated object of useful links")
    return json.loads(result)
        
        

if __name__ == "__main__":
    wb_url = "https://www.rokomari.com/"
    brochure_links = get_useful_links_with_openai(wb_url)
    print(brochure_links)
    print(type(brochure_links))
 