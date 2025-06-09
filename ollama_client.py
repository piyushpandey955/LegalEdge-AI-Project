import requests
import json
from typing import Generator, Dict, Any
import time
import logging
import traceback
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama2"
        self.timeout = 120  # Increased timeout to 120 seconds
        self.max_retries = 3
        self.retry_delay = 2  # Delay between retries in seconds
        self._verify_connection()

    def _verify_connection(self):
        """Verify that the Ollama server is running and accessible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            logger.info("Successfully connected to Ollama server")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Ollama server at {self.base_url}")
            logger.error(f"Error: {str(e)}")
            raise Exception(
                "Could not connect to Ollama server. Please make sure it's running by executing 'ollama serve' in a terminal."
            )

    def _generate_stream(self, prompt, system_prompt=None):
        """Generate a stream of text from the model."""
        max_retries = self.max_retries
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f"Making request to Ollama server (attempt {retry_count + 1}/{max_retries})")
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "system": system_prompt,
                        "stream": True
                    },
                    timeout=120  # Increased timeout to 120 seconds
                )
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        try:
                            json_response = json.loads(line)
                            if 'response' in json_response:
                                yield json_response['response']
                            if json_response.get('done', False):
                                break
                        except json.JSONDecodeError as e:
                            logger.error(f"Error decoding JSON response: {str(e)}")
                            logger.error(f"Raw response: {line}")
                            continue
                
                return  # Successfully completed
                
            except requests.exceptions.Timeout as e:
                retry_count += 1
                logger.error(f"Attempt {retry_count} failed: {str(e)}")
                if retry_count < max_retries:
                    logger.info(f"Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    raise Exception(f"Failed to generate response after {max_retries} attempts: {str(e)}")
                    
            except requests.exceptions.RequestException as e:
                retry_count += 1
                logger.error(f"Attempt {retry_count} failed: {str(e)}")
                if retry_count < max_retries:
                    logger.info(f"Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    raise Exception(f"Failed to generate response after {max_retries} attempts: {str(e)}")
                    
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                logger.error(f"Stack trace: {traceback.format_exc()}")
                raise

    def generate_document(self, prompt: str) -> str:
        """Generate a legal document based on the prompt."""
        logger.info(f"Starting document generation with prompt: {prompt}")
        system_prompt = """You are a legal document generator. Generate a professional legal document based on the user's requirements. 
        Include all necessary clauses and sections. Format the output in a clear, structured manner."""
        
        full_response = ""
        try:
            for chunk in self._generate_stream(prompt, system_prompt):
                if "response" in chunk:
                    full_response += chunk["response"]
                    logger.info(f"Received chunk: {chunk['response'][:100]}...")
            
            if not full_response:
                logger.error("No response generated from Ollama")
                raise Exception("No response generated from Ollama")
                
            logger.info(f"Successfully generated document of length: {len(full_response)}")
            return full_response
        except Exception as e:
            logger.error(f"Error in generate_document: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise

    def analyze_contract(self, contract_text: str) -> Dict[str, Any]:
        """Analyze a contract and extract key information."""
        system_prompt = """You are a legal contract analyzer. Analyze the provided contract and provide a response in the following JSON format:
        {
            "key_clauses": [
                {
                    "name": "clause name",
                    "purpose": "clause purpose"
                }
            ],
            "potential_risks": [
                "risk description"
            ],
            "summary": "brief summary of the contract's main points"
        }
        Ensure your response is valid JSON and follows this exact structure."""
        
        prompt = f"Analyze this contract and provide the analysis in the specified JSON format:\n\n{contract_text}"
        full_response = ""
        try:
            for chunk in self._generate_stream(prompt, system_prompt):
                if "response" in chunk:
                    full_response += chunk["response"]
            
            # Try to parse the response as JSON
            try:
                return json.loads(full_response)
            except json.JSONDecodeError:
                # If parsing fails, try to extract JSON from the response
                # Look for content between curly braces
                json_match = re.search(r'\{.*\}', full_response, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group())
                    except json.JSONDecodeError:
                        pass
                
                # If all parsing attempts fail, return a structured error response
                return {
                    "error": "Failed to parse LLM response as JSON",
                    "raw_response": full_response,
                    "key_clauses": [],
                    "potential_risks": [],
                    "summary": "Unable to analyze the contract due to formatting issues."
                }
        except Exception as e:
            logger.error(f"Error in analyze_contract: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            return {
                "error": f"Error analyzing contract: {str(e)}",
                "key_clauses": [],
                "potential_risks": [],
                "summary": "An error occurred while analyzing the contract."
            }

    def legal_assistant(self, question: str) -> str:
        """Provide legal advice or answer legal questions."""
        logger.info("Processing legal assistant request")
        system_prompt = """You are a legal assistant. Provide clear, accurate, and helpful responses to legal questions. 
        Keep responses concise and practical. Focus on the most relevant legal principles and implications."""
        
        full_response = ""
        try:
            for chunk in self._generate_stream(question, system_prompt):
                if "response" in chunk:
                    full_response += chunk["response"]
            logger.info("Successfully generated legal assistant response")
            return full_response
        except Exception as e:
            logger.error(f"Error in legal_assistant: {str(e)}")
            raise

    def check_compliance(self, legal_text: str) -> Dict[str, Any]:
        """Check legal text for compliance and required clauses."""
        system_prompt = """You are a legal compliance checker. Analyze the provided legal text and:
        1. Identify any missing required clauses
        2. List potential compliance issues
        3. Provide a checklist of recommended additions
        Format the output as a JSON object with these sections."""
        
        prompt = f"Check compliance for this legal text:\n\n{legal_text}"
        full_response = ""
        for chunk in self._generate_stream(prompt, system_prompt):
            if "response" in chunk:
                full_response += chunk["response"]
        
        try:
            return json.loads(full_response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM response as JSON"}

    def simplify_document(self, legal_text: str) -> str:
        """Convert complex legal text into plain English."""
        try:
            logger.info("Starting document simplification")
            if not legal_text or not legal_text.strip():
                raise ValueError("Legal text cannot be empty")
                
            system_prompt = """You are a legal document simplifier. Convert complex legal text into clear, plain English while maintaining the original meaning and intent. 
            Use simple language and structure the output in an easy-to-understand format."""
            
            prompt = f"Simplify this legal text:\n\n{legal_text}"
            logger.info(f"Generated prompt for simplification: {prompt[:100]}...")
            
            full_response = ""
            for chunk in self._generate_stream(prompt, system_prompt):
                if "response" in chunk:
                    full_response += chunk["response"]
                    
            if not full_response:
                raise Exception("No response generated from Ollama")
                
            logger.info("Successfully simplified document")
            return full_response
            
        except Exception as e:
            logger.error(f"Error in simplify_document: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise 