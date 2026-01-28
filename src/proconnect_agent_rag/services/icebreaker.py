from typing import Dict, Optional, Tuple

from serpapi import GoogleSearch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from proconnect_agent_rag.config import get_settings
from proconnect_agent_rag.utils.logging import setup_logging

logger = setup_logging(__name__)

class IcebreakerRAG:
    def __init__(self):
        self.settings = get_settings()
        
        if not self.settings.SERPAPI_API_KEY:
            raise ValueError("Missing SERPAPI_API_KEY")
        if not self.settings.OPENAI_API_KEY:
            raise ValueError("Missing OPENAI_API_KEY")

        # Initializing LLM
        logger.debug("Initializing LLM...")
        self.llm = ChatOpenAI(
            model="gpt-4o", 
            temperature=0.7,
            api_key=self.settings.OPENAI_API_KEY
        )
        self.chain = self._build_chain()

    def _build_chain(self) -> Tuple[ChatPromptTemplate, ChatPromptTemplate]:
        # 1. Extraction & Summarization Prompt
        search_prompt = ChatPromptTemplate.from_template(
        """
            You are a research assistant. 
            Target Person: {context}
            Search Results:
            {search_results}
            
            Instructions:
            1. Identify their **Primary Current Job Title** and **Current Company Name**.
            2. Combine them into a single string format if applicable: "[Job Title] at [Company Name]" (e.g., "Senior AI Engineer at OpenAI").
            3. Summarize their key expertise, specific projects, or recent news.
            
            Output Format:
            Role_Context: <Job Title> at <Company Name>
            Summary: <concise summary of expertise and news>
            """
        )

        # 2. Writing Prompt
        writer_prompt = ChatPromptTemplate.from_template(
            """
            You are an expert networker. Write a personalized LinkedIn connection message.
            
            Input Data:
            {summary}
            
            Rules:
            - STRICT limit: less than 300 characters.
            - Tone: Professional, warm, authentic.
            - Start with a friendly greeting using the person's first name.
            
            Content Requirements:
            - **Integrate the 'Role_Context' naturally.** (e.g., "Your work as [Role_Context] caught my eye..." or "I've been following [Company Name]...").
            - Reference a specific achievement or skill mentioned in the summary.
            
            Restrictions (Strictly Avoid):
            - NO generic openers: "I hope you are well", "I came across your profile".
            - NO generic closings: "Best regards", "Sincerely", and similar phrases.
            - Do NOT leave incomplete sentence at the end
            - Do NOT sign off with your name at the end.
            
            Draft Message:
            """
        )
        return search_prompt, writer_prompt

    def _perform_search(self, query: str) -> str:
        try:
            params = {
                "engine": "google",
                "q": query,
                "api_key": self.settings.SERPAPI_API_KEY,
                "hl": "en",
                "num": 10
            }
            
            logger.info(f"Searching Google for: {query}")
            search = GoogleSearch(params)
            results = search.get_dict()
            organic_results = results.get("organic_results", [])
            
            if not organic_results:
                return "No relevant results found."
            
            linkedin_result = None
            for r in organic_results:
                if "linkedin.com/in/" in r.get("link", ""):
                    linkedin_result = r
                    break 

            if linkedin_result:
                logger.info("LinkedIn profile found. Using ONLY this source.")
                return (f"*** MATCH FOUND (LINKEDIN) ***\n"
                        f"- Title: {linkedin_result.get('title')}\n"
                        f"- Snippet: {linkedin_result.get('snippet')}\n"
                        f"- Link: {linkedin_result.get('link')}")

            return "No LinkedIn found. Using other results."
            
        except Exception as e:
            logger.error(f"SerpApi error: {e}")
            return f"Error retrieving search results: {e}"

    def generate_icebreaker(self, name: str, company: str = "") -> str:
        sanitized_name = name.strip()
        context = f"{sanitized_name} {company}".strip()
        query = f'"{sanitized_name}" {company} linkedin profile'
        
        # 1. Get Data
        raw_results = self._perform_search(query)
        
        # 2. Summarize & Extract
        search_prompt, writer_prompt = self.chain
        summary_chain = search_prompt | self.llm | StrOutputParser()
        summary = summary_chain.invoke({"search_results": raw_results, "context": context})
        
        # 3. Write Message
        final_chain = writer_prompt | self.llm | StrOutputParser()
        icebreaker = final_chain.invoke({"summary": summary})
        
        return icebreaker
