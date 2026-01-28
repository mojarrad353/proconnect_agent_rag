import pytest
from unittest.mock import MagicMock, patch
from proconnect_agent_rag.services.icebreaker import IcebreakerRAG

@pytest.fixture
def mock_settings():
    with patch("proconnect_agent_rag.services.icebreaker.get_settings") as mock:
        mock.return_value.OPENAI_API_KEY = "test_openai_key"
        mock.return_value.SERPAPI_API_KEY = "test_serpapi_key"
        yield mock

@pytest.fixture
def mock_llm():
    with patch("proconnect_agent_rag.services.icebreaker.ChatOpenAI") as mock:
        yield mock

@pytest.fixture
def mock_google_search():
    with patch("proconnect_agent_rag.services.icebreaker.GoogleSearch") as mock:
        yield mock

def test_icebreaker_initialization(mock_settings, mock_llm):
    rag = IcebreakerRAG()
    assert rag.chain is not None
    mock_llm.assert_called_once()

def test_perform_search_no_results(mock_settings, mock_llm, mock_google_search):
    rag = IcebreakerRAG()
    
    # Mock empty results
    mock_instance = mock_google_search.return_value
    mock_instance.get_dict.return_value = {"organic_results": []}
    
    result = rag._perform_search("test query")
    assert result == "No relevant results found."

def test_perform_search_linkedin_found(mock_settings, mock_llm, mock_google_search):
    rag = IcebreakerRAG()
    
    # Mock linkedin result
    mock_instance = mock_google_search.return_value
    mock_instance.get_dict.return_value = {
        "organic_results": [
            {
                "link": "https://www.linkedin.com/in/jensen-huang",
                "title": "Jensen Huang - CEO",
                "snippet": "CEO of NVIDIA"
            }
        ]
    }
    
    result = rag._perform_search("test query")
    assert "*** MATCH FOUND (LINKEDIN) ***" in result
    assert "Jensen Huang" in result

def test_generate_icebreaker_flow(mock_settings, mock_llm, mock_google_search):
    rag = IcebreakerRAG()
    
    # Mock search
    rag._perform_search = MagicMock(return_value="Mocked Search Result")
    
    # Mock chains
    mock_summary_chain = MagicMock()
    mock_summary_chain.invoke.return_value = "Mocked Summary"
    
    mock_writer_chain = MagicMock()
    mock_writer_chain.invoke.return_value = "Mocked Icebreaker Message"
    
    # We need to mock the chain components because we're mocking the entire chain execution flow
    # This is a bit complex due to the LCEL pipe syntax, so for a unit test, 
    # we might just want to verify the invoke calls if we could inspect the chain.
    # However, since _build_chain returns prompts, and we use those in generate_icebreaker...
    
    # Let's mock the chain building to return mocks we can control or inspecting the result
    # For simplicity, let's just mock the invoke calls on the chain objects created in generate_icebreaker
    # BUT generate_icebreaker constructs the chains on the fly: 
    # summary_chain = search_prompt | self.llm | StrOutputParser()
    
    # A cleaner integration test would allow the chain to construct but mock the LLM's invoke.
    # Let's try mocking the LLM invoke.
    
    mock_llm_instance = mock_llm.return_value
    mock_llm_instance.invoke.return_value.content = "Mocked LLM Response" # ChatOpenAI returns a message
    
    # We also need to mock StrOutputParser because `invoke` on LLM returns a BaseMessage, and StrOutputParser takes that.
    # Actually, ChatOpenAI invokes return BaseMessage.
    
    # To properly unit test without making real calls:
    with patch("proconnect_agent_rag.services.icebreaker.StrOutputParser") as mock_parser:
        # The parser invoke returns the string
        mock_parser.return_value.invoke.return_value = "Parsed String"
        
        # We need to make sure the pipe | works. 
        # Mocking LCEL is hard. 
        # Strategy: verifying that _perform_search is called and it returns something.
        
        result = rag.generate_icebreaker("Test Name", "Test Company")
        
        rag._perform_search.assert_called_with('"Test Name" Test Company linkedin profile')
        # If the code runs without error and returns the result of the chain (which eventually comes from the mocks), pass.
