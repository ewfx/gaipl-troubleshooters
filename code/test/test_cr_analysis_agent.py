import pytest
from unittest.mock import patch, MagicMock

import sys
# Import os module for interacting with the operating system
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code.src.backend.cr_analysis_agent import analyze_cr_with_model, analyze_cr

@pytest.fixture
def mock_incident_details():
    return {
        "issue": "Application crash",
        "application_affected": "Payment Gateway",
        "start_date": "2023-10-01",
        "priority": "High"
    }

@pytest.fixture
def mock_change_requests():
    return [
        {
            "change_id": "CR001",
            "description": "Database schema update",
            "affected_components": ["Database", "Backend"],
            "implementation_date": "2023-09-30"
        },
        {
            "change_id": "CR002",
            "description": "Frontend UI update",
            "affected_components": ["Frontend"],
            "implementation_date": "2023-09-29"
        }
    ]

@patch("cr_analysis_agent.genai.GenerativeModel")
def test_analyze_cr_with_model_gemini(mock_gen_model, mock_incident_details, mock_change_requests):
    mock_response = MagicMock()
    mock_response.text = "### Change Requests that could've led to this incident\n- **Change ID**: CR001\n  - **Reason for Impact**: Database schema update caused issues."
    mock_gen_model.return_value.generate_content.return_value = mock_response

    result = analyze_cr_with_model(
        incident_details=mock_incident_details,
        change_requests=mock_change_requests,
        gemini_api_key="mock_gemini_api_key"
    )

    assert "Change Requests that could've led to this incident" in result
    assert "**Change ID**: CR001" in result

@patch("cr_analysis_agent.genai.GenerativeModel")
def test_analyze_cr_with_model_gemini_failure(mock_gen_model, mock_incident_details, mock_change_requests):
    mock_gen_model.return_value.generate_content.side_effect = Exception("Gemini API error")

    result = analyze_cr_with_model(
        incident_details=mock_incident_details,
        change_requests=mock_change_requests,
        gemini_api_key="mock_gemini_api_key"
    )

    assert result == "Gemini model failed to analyze the incident and change requests."

def test_analyze_cr(mock_incident_details, mock_change_requests):
    with patch("cr_analysis_agent.analyze_cr_with_model") as mock_analyze_cr_with_model:
        mock_analyze_cr_with_model.return_value = "Mocked analysis result"
        result = analyze_cr(mock_incident_details, mock_change_requests)

        assert result == "Mocked analysis result"
        mock_analyze_cr_with_model.assert_called_once_with(
            incident_details=mock_incident_details,
            change_requests=mock_change_requests,
            gemini_api_key="AIzaSyALENrXIslUHsrTlwHqV_qpItxC17J08co"
        )

def test_analyze_cr_with_empty_inputs():
    result = analyze_cr_with_model(
        incident_details={},
        change_requests=[],
        gemini_api_key="mock_gemini_api_key"
    )

    assert result == "Gemini model failed to analyze the incident and change requests."