import asyncio
import sys
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

from utils.exception import CustomException
from utils.logger import logging

class Website:
    def __init__(self, url):
        logging.info("Initializing Website object")
        self.url = url
        self.title = ""
        self.text = ""
        self.links = []
        asyncio.run(self._scrape_website())

    async def _scrape_website(self):  
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                await page.goto(self.url, timeout=60000)
                html = await page.content()   
                soup = BeautifulSoup(html, 'html.parser')
                logging.info(f"Successfully parsed html sections")
                
                self.title = soup.title.string if soup.title else "No title found"
                
                if soup.body:
                    for element in soup.body(["script", "style", "img", "input"]):
                        element.decompose()
                    self.text = soup.body.get_text(separator="\n", strip=True)
                
                links = [link.get("href") for link in soup.find_all('a')]
                self.links = [link for link in links if link]
                logging.info("Extracted text and links")
            except Exception as e:
                # CustomException(sys, e) 
                raise str(e)

            finally:
                await browser.close() 

    def get_content(self):
        logging.info("Creating website content")
        return f"Webpage Title:\n{self.title}\nWebpage Content:\n{self.text}\n"
    
    
    
    
if __name__ == "__main__":
    wb_link = "https://www.rokomari.com"
    try:
        wb = Website(wb_link)
    
        if wb:
            print(f"Title: {wb.title}")
            links = wb.links
            print(f"Total Number of Links: {len(links)}")
            print(f"Content: {wb.get_content()[:300]}")
            print(links[:10])
        else:
            print("No website found")
    except Exception as e:
        raise Exception(e)
        