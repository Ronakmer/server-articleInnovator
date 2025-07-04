import os
from typing import Dict, Any, Optional
from openai import OpenAI
import json
from django.conf import settings


class AIProvider:
    def __init__(self):
        """Initialize the AI provider with Novita/Deepseek configuration"""
        self.api_key = os.getenv('NOVITA_API_KEY')
        self.api_url = os.getenv('NOVITA_API_URL', 'https://api.novita.ai/v3/openai')
        self.model = os.getenv('NOVITA_MODEL', 'deepseek/deepseek_v3')
        
        if not self.api_key:
            raise ValueError("NOVITA_API_KEY environment variable is required")
            
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_url
            )
            print("Successfully initialized AI provider")
        except Exception as e:
            print(f"Error initializing AI provider: {str(e)}")
            raise

    def extract_selectors(self, html_content: str, domain: str) -> Dict[str, str]:
        """
        Extract selectors from HTML content using AI
        
        Args:
            html_content: The HTML content to analyze
            domain: The domain name for context
            
        Returns:
            Dictionary containing selectors for different elements
        """
        try:
            system_prompt = """Extract CSS selectors from HTML. Return ONLY valid JSON."""

            user_prompt = f"""Analyze the HTML content from {domain} and provide CSS selectors for the following elements:
            Sometimes, the value is in an attribute - so mention the attribute name if applicable, else keep it null. Also, mention `multiple: true` if multiple values are expected.

            1. source_title
            2. source_categories
            3. source_tags
            4. source_author
            5. source_published_date
            6. source_content - (Remove .entry-header, ads, scripts, breadcrumbs, social links, etc.)
            7. source_featured_image
            8. source_meta_title
            9. source_meta_description
            10. source_meta_keywords
            11. source_outline - Extract text content of all H1 to H6 headings, if they repeat, include all
            12. source_faqs - Extract original FAQ text content (questions and answers)

            Return ONLY a JSON object with these exact keys:
            {{
                "source_title": {{
                    "name": "source_title",
                    "selector": "selector here",
                    "attribute": "",
                    "multiple": false,
                    "remove_selectors": []
                }},
                "source_content": {{
                    "name": "source_content",
                    "selector": "selector here",
                    "attribute": "",
                    "multiple": false,
                    "remove_selectors": ["selector here", "selector here"]
                }},
                "source_categories": {{
                    "name": "source_categories",
                    "selector": "selector here",
                    "attribute": "",
                    "multiple": false,
                    "remove_selectors": []
                }},
                "source_tags": {{
                    "name": "source_tags",
                    "selector": "selector here",
                    "attribute": "",
                    "multiple": true,
                    "remove_selectors": []
                }},
                "source_author": {{
                    "name": "source_author",
                    "selector": "selector here",
                    "attribute": "",
                    "multiple": false,
                    "remove_selectors": []
                }},
                "source_published_date": {{
                    "name": "source_published_date",
                    "selector": "selector here",
                    "attribute": "",
                    "multiple": false,
                    "remove_selectors": []
                }},
                "source_featured_image": {{
                    "name": "source_featured_image",
                    "selector": "selector here",
                    "attribute": "src",
                    "multiple": false,
                    "remove_selectors": []
                }},
                "source_meta_title": {{
                    "name": "source_meta_title",
                    "selector": "meta[name='title']",
                    "attribute": "content",
                    "multiple": false,
                    "remove_selectors": []
                }},
                "source_meta_description": {{
                    "name": "source_meta_description",
                    "selector": "meta[name='description']",
                    "attribute": "content",
                    "multiple": false,
                    "remove_selectors": []
                }},
                "source_meta_keywords": {{
                    "name": "source_meta_keywords",
                    "selector": "meta[name='keywords']",
                    "attribute": "content",
                    "multiple": false,
                    "remove_selectors": []
                }},
                "source_outline": {{
                    "name": "source_outline",
                    "selector": "h1, h2, h3, h4, h5, h6",
                    "attribute": null,
                    "multiple": true,
                    "remove_selectors": []
                }},
                "source_faqs": {{
                    "name": "source_faqs",
                    "selector": "[class*='faq'], [id*='faq'], .question, .answer, .accordion",
                    "attribute": null,
                    "multiple": true,
                    "remove_selectors": []
                }}
            }}

            Important:
            - Use `null` if a field is not found.
            - For links, extract all matching anchors.
            - For outline, extract all heading texts even if repeated.

            HTML Content:
            {html_content[:10000]}"""

            print(f"Starting AI API call for {domain}")
            print(f"Using model: {self.model}")
            print(f"API URL: {self.api_url}")
            print(f"System prompt length: {len(system_prompt)}")
            print(f"User prompt length: {len(user_prompt)}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            print(f"AI API call completed successfully for {domain}")
            
            # Get the response content
            print(f"Processing AI response for {domain}")
            response_text = response.choices[0].message.content
            print(f"Raw response length: {len(response_text) if response_text else 0}")
            
            if not response_text:
                print(f"Empty response from AI API for {domain}")
                return self._get_fallback_selectors()
            
            # Parse JSON response
            try:
                print(f"Cleaning and parsing JSON response for {domain}")
                response_text = response_text.replace("```json", "")
                response_text = response_text.replace("```", "")
                response_text = response_text.strip()
                
                print(f"Cleaned response length: {len(response_text)}")
                print(f"Response preview: {response_text[:500]}...")
                
                selectors = json.loads(response_text)
                print(f"Successfully parsed JSON selectors for {domain}")
                
                # Add fixed internal and external link selectors
                selectors["source_internal_links"] = {
                    "name": "source_internal_links",
                    "selector": "a",
                    "multiple": True,
                    "attribute": "href",
                    "link_type": "internal",
                    "remove_selectors": []
                }
                
                selectors["source_external_links"] = {
                    "name": "source_external_links",
                    "selector": "a",
                    "multiple": True,
                    "attribute": "href",
                    "link_type": "external",
                    "remove_selectors": []
                }
                
                return selectors
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response for {domain}: {str(e)}")
                print(f"Invalid JSON: {response_text}")
                return self._get_fallback_selectors()
            
        except Exception as e:
            print(f"Error in AI extraction for {domain}: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {repr(e)}")
            return self._get_fallback_selectors()

    def _get_fallback_selectors(self):
        """Return fallback selector structure when AI API fails"""
        print("Generating fallback selectors")
        return {
            "source_title": {
                "name": "source_title",
                "selector": None,
                "attribute": None,
                "multiple": False,
                "remove_selectors": []
            },
            "source_content": {
                "name": "source_content",
                "selector": None,
                "attribute": None,
                "multiple": False,
                "remove_selectors": []
            },
            "source_categories": {
                "name": "source_categories",
                "selector": None,
                "attribute": None,
                "multiple": False,
                "remove_selectors": []
            },
            "source_tags": {
                "name": "source_tags",
                "selector": None,
                "attribute": None,
                "multiple": True,
                "remove_selectors": []
            },
            "source_author": {
                "name": "source_author",
                "selector": None,
                "attribute": None,
                "multiple": False,
                "remove_selectors": []
            },
            "source_published_date": {
                "name": "source_published_date",
                "selector": None,
                "attribute": None,
                "multiple": False,
                "remove_selectors": []
            },
            "source_featured_image": {
                "name": "source_featured_image",
                "selector": None,
                "attribute": None,
                "multiple": False,
                "remove_selectors": []
            },
            "source_meta_title": {
                "name": "source_meta_title",
                "selector": None,
                "attribute": None,
                "multiple": False,
                "remove_selectors": []
            },
            "source_meta_description": {
                "name": "source_meta_description",
                "selector": None,
                "attribute": None,
                "multiple": False,
                "remove_selectors": []
            },
            "source_meta_keywords": {
                "name": "source_meta_keywords",
                "selector": None,
                "attribute": None,
                "multiple": False,
                "remove_selectors": []
            },
            "source_outline": {
                "name": "source_outline",
                "selector": None,
                "attribute": None,
                "multiple": True,
                "remove_selectors": []
            },
            "source_faqs": {
                "name": "source_faqs",
                "selector": None,
                "attribute": None,
                "multiple": True,
                "remove_selectors": []
            },
            "source_internal_links": {
                "name": "source_internal_links",
                "selector": "a",
                "multiple": True,
                "attribute": "href",
                "link_type": "internal",
                "remove_selectors": []
            },
            "source_external_links": {
                "name": "source_external_links",
                "selector": "a",
                "multiple": True,
                "attribute": "href",
                "link_type": "external",
                "remove_selectors": []
            }
        }
