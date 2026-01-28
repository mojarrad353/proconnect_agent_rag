import os
import sys
from dotenv import load_dotenv
from rag_engine import IcebreakerRAG

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("Error: OPENAI_API_KEY is missing.")
    
    print("--- LinkedIn Icebreaker Agent (Web Search Mode) ---")
    
    # Ask for name and company to make the search accurate
    name = input("Target Name (e.g., Jensen Huang): ").strip()
    company = input("Target Company (optional): ").strip()
    
    if not name:
        print("Error: Name is required.")
        return

    try:
        bot = IcebreakerRAG()
        icebreaker = bot.generate_icebreaker(name=name, company=company)
        
        print("\n" + "="*50)
        print("Generated Icebreaker:")
        print("="*50)
        print(icebreaker)
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"Application Error: {e}")

if __name__ == "__main__":
    main()