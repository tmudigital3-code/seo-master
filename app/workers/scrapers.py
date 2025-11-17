import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

class GoogleScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_search_results(self, keyword, country='us'):
        """
        Get Google search results for a keyword
        """
        url = f"https://www.google.com/search?q={keyword}&gl={country}&hl=en"
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract search results
            results = []
            search_results = soup.find_all('div', class_='g')
            
            for i, result in enumerate(search_results[:10]):  # Top 10 results
                title_elem = result.find('h3')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    title = title_elem.text
                    url = link_elem.get('href')
                    results.append({
                        'position': i + 1,
                        'title': title,
                        'url': url
                    })
            
            return results
        except Exception as e:
            print(f"Error scraping Google for {keyword}: {str(e)}")
            return []

class AIScraper:
    def __init__(self):
        # Setup headless browser for JavaScript-heavy sites
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
    
    def get_google_ai_overview(self, keyword):
        """
        Get Google AI Overview results for a keyword
        """
        try:
            url = f"https://www.google.com/search?q={keyword}&hl=en"
            self.driver.get(url)
            time.sleep(2)  # Wait for page to load
            
            # Look for AI Overview section
            ai_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-hveid*='CAI']")
            
            if ai_elements:
                ai_text = ai_elements[0].text
                return {
                    'included': True,
                    'content': ai_text[:500],  # Limit to first 500 chars
                    'content_length': len(ai_text)
                }
            else:
                return {
                    'included': False,
                    'content': '',
                    'content_length': 0
                }
        except Exception as e:
            print(f"Error scraping Google AI Overview for {keyword}: {str(e)}")
            return {
                'included': False,
                'content': '',
                'content_length': 0
            }
    
    def close(self):
        self.driver.quit()

class YouTubeScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_video_rankings(self, keyword):
        """
        Get YouTube video rankings for a keyword
        """
        url = f"https://www.youtube.com/results?search_query={keyword}"
        try:
            response = self.session.get(url)
            # YouTube uses dynamic loading, so we need to parse the initial data
            # This is a simplified approach - in practice, you'd use their API
            if 'var ytInitialData' in response.text:
                # Extract JSON data from response
                start = response.text.find('var ytInitialData = ') + 20
                end = response.text.find(';</script>', start)
                json_str = response.text[start:end]
                
                data = json.loads(json_str)
                videos = []
                
                # Parse video results (simplified)
                if 'contents' in data:
                    tab_contents = data['contents'].get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {})
                    section_list = tab_contents.get('sectionListRenderer', {}).get('contents', [])
                    
                    for section in section_list:
                        if 'itemSectionRenderer' in section:
                            item_renderer = section['itemSectionRenderer']
                            for content in item_renderer.get('contents', []):
                                if 'videoRenderer' in content:
                                    video = content['videoRenderer']
                                    video_data = {
                                        'title': video.get('title', {}).get('runs', [{}])[0].get('text', ''),
                                        'channel': video.get('ownerText', {}).get('runs', [{}])[0].get('text', ''),
                                        'views': video.get('viewCountText', {}).get('simpleText', ''),
                                        'duration': video.get('lengthText', {}).get('simpleText', '')
                                    }
                                    videos.append(video_data)
                
                return videos[:10]  # Return top 10
            return []
        except Exception as e:
            print(f"Error scraping YouTube for {keyword}: {str(e)}")
            return []