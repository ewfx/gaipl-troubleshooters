import os
import pytest
from unittest.mock import patch, mock_open
import code.src.backend.heal_agent as heal_agent
#from code.src.backend.heal_agent import generate_heal_script_with_model, generate_heal_script

@pytest.fixture
def mock_openai_response():
    return {
        "choices": [
            {
                "text": "#!/bin/bash\n# Stop the service\nsudo systemctl stop example-service\n# Apply fixes\necho 'Applying fixes...'\n# Restart the service\nsudo systemctl start example-service\n"
            }
        ]
    }

@pytest.fixture
def mock_gemini_response():
    class MockResponse:
        def __init__(self, text):
            self.text = text

    return MockResponse(
        "#!/bin/bash\n# Stop the service\nsudo systemctl stop example-service\n# Apply fixes\necho 'Applying fixes...'\n# Restart the service\nsudo systemctl start example-service\n"
    )

@patch("heal_agent.openai.Completion.create")
def test_generate_heal_script_with_openai(mock_openai_create, mock_openai_response):
    mock_openai_create.return_value = mock_openai_response
    issue_description = "Example issue description"
    openai_api_key = "mock_openai_api_key"

    result = generate_heal_script_with_model(issue_description, openai_api_key=openai_api_key)

    assert "#!/bin/bash" in result
    assert "sudo systemctl stop example-service" in result
    assert "sudo systemctl start example-service" in result

@patch("heal_agent.genai.GenerativeModel")
def test_generate_heal_script_with_gemini(mock_genai_model, mock_gemini_response):
    mock_model_instance = mock_genai_model.return_value
    mock_model_instance.generate_content.return_value = mock_gemini_response
    issue_description = "Example issue description"
    gemini_api_key = "mock_gemini_api_key"

    result = generate_heal_script_with_model(issue_description, gemini_api_key=gemini_api_key)

    assert "#!/bin/bash" in result
    assert "sudo systemctl stop example-service" in result
    assert "sudo systemctl start example-service" in result

@patch("heal_agent.generate_heal_script_with_model")
@patch("builtins.open", new_callable=mock_open)
@patch("os.chmod")
def test_generate_heal_script(mock_chmod, mock_file, mock_generate_heal_script_with_model):
    mock_generate_heal_script_with_model.return_value = "#!/bin/bash\necho 'Mock script'"
    issue_description = "Example issue description"

    output_file = generate_heal_script(issue_description)

    mock_generate_heal_script_with_model.assert_called_once_with(
        issue_description=issue_description,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        gemini_api_key=os.environ.get("GOOGLE_API_KEY"),
        openai_model="gpt-3.5-turbo"
    )
    mock_file.assert_called_once_with("heal_script.sh", "w")
    mock_file().write.assert_called_once_with("#!/bin/bash\necho 'Mock script'")
    mock_chmod.assert_called_once_with("heal_script.sh", 0o755)
    assert output_file == "heal_script.sh"

def test_generate_heal_script_with_no_keys():
    issue_description = "Example issue description"
    with pytest.raises(RuntimeError, match="Both OpenAI and Gemini models failed to generate the heal script."):
        generate_heal_script_with_model(issue_description)
