from linkedin_icebreaker.services.icebreaker import IcebreakerRAG
from linkedin_icebreaker.config import get_settings
import sys

def main():
    try:
        settings = get_settings()
        if not settings.OPENAI_API_KEY:
             sys.exit("Error: OPENAI_API_KEY is missing.")
    except Exception as e:
        sys.exit(f"Configuration Error: {e}")
    
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
