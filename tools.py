import logging
from livekit.agents import function_tool, RunContext
import requests
import os
from typing import Optional
import datetime
import pytz
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
# --- Configuration for Serper.dev API Key ---
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "YOUR_SERPER_API_KEY_HERE")

if SERPER_API_KEY == "YOUR_SERPER_API_KEY_HERE":
    logging.warning("Serper.dev API Key not configured. Please set SERPER_API_KEY environment variable.")

# --- Weather Function ---
@function_tool()
async def get_weather(context: RunContext, city: str) -> str:
    """
    Get the current weather for a given city.
    Args:
        city (str): The name of the city.
    """
    logging.info(f"get_weather called for city: {city}")
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."

# --- Current Date and Time Function ---
@function_tool()
async def get_current_datetime(context: RunContext) -> str:
    """
    Returns the current date and time, including the timezone.
    This tool does not require any input arguments.
    """
    print("--- get_current_datetime function HAS BEEN CALLED ---")
    logging.info(f"get_current_datetime called.")
    
    try:
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        logging.debug(f"DEBUG: UTC time before conversion: {utc_now}")
        ist_timezone = pytz.timezone('Asia/Kolkata') 
        ist_now = utc_now.astimezone(ist_timezone)
        formatted_datetime = ist_now.strftime("%A, %B %d, %Y at %I:%M %p %Z")
        
        logging.info(f"Current date and time requested: {formatted_datetime}")
        return f"The current date and time is: {formatted_datetime}"
    except Exception as e:
        logging.error(f"Error getting current date and time: {e}")
        return "I am sorry, I could not retrieve the current date and time."

# --- Web Search Function ---
async def search_web(raw_arguments: dict[str, object], context: RunContext) -> str:
    """
    Searches the web for the given query using the Serper.dev API.
    This tool is designed to be called by an LLM.
    """
    if SERPER_API_KEY == "YOUR_SERPER_API_KEY_HERE":
        return "Web search is not configured. Please set your Serper.dev API Key."

    query = raw_arguments.get('query', '').strip()
    if not query:
        logging.warning("search_web tool called without a valid 'query' argument.")
        return "I need a search query to perform a web search."

    logging.info(f"Performing web search for: '{query}' using Serper.dev")

    try:
        url = "https://serper.dev/search"
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        payload = {
            "q": query,
            "num": 3 
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        organic_results = data.get('organic', [])
        
        if organic_results:
            formatted_results = []
            for i, result in enumerate(organic_results):
                title = result.get('title', 'No Title')
                link = result.get('link', 'No URL')
                snippet = result.get('snippet', 'No Snippet')
                formatted_results.append(f"Result {i+1}: {title} (URL: {link})\nSnippet: {snippet[:150]}...")
            
            full_response = "\n---\n".join(formatted_results)
            logging.info(f"Serper.dev search completed for '{query}'.")
            return f"Search results for '{query}':\n{full_response}"
        else:
            logging.info(f"No relevant search results found for '{query}'.")
            return f"No search results found for '{query}'."

    except requests.exceptions.RequestException as e:
        logging.error(f"Network or API error during search for '{query}': {e}")
        return f"I encountered a problem connecting to the search service for '{query}'. Please try again later."
    except Exception as e:
        logging.error(f"An unexpected error occurred during search for '{query}': {e}")
        return f"An unexpected error occurred while processing the search for '{query}'."

# --- Define _raw_schema for search_web at module level ---
search_web._raw_schema = { # type: ignore
    "type": "object",
    "name": "search_web",
    "description": "Searches the web for the given query using the Serper.dev API.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query for the web search."
            }
        },
        "required": ["query"],
        "additionalProperties": False,
    }
}

# --- Send Email Function ---
async def send_email(raw_arguments: dict[str, object], context: RunContext) -> str:
    """
    Send an email through Gmail SMTP.
    Args:
        to_email (str): Recipient email address.
        subject (str): Email subject line.
        message (str): Email body content.
        cc_email (Optional[str]): Optional CC email address.
    """
    print("--- send_email function HAS BEEN CALLED ---") 
    logging.debug(f"DEBUG: send_email called with raw_arguments: {raw_arguments}")

    try:
        # Extract arguments from raw_arguments
        to_email = raw_arguments.get('to_email')
        subject = raw_arguments.get('subject')
        message = raw_arguments.get('message')
        cc_email = raw_arguments.get('cc_email')

        logging.debug(f"DEBUG: Extracted email details - To: {to_email}, Subject: {subject}, Message length: {len(message) if message else 0}, CC: {cc_email}")

        if not all([to_email, subject, message]):
            logging.error("Missing required arguments for send_email.")
            return "Email sending failed: Missing recipient, subject, or message."

        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587 # Using 587 with starttls

        # Get credentials from environment variables
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_password:
            logging.error("Gmail credentials not found in environment variables (GMAIL_USER, GMAIL_APP_PASSWORD).")
            return "Email sending failed: Gmail credentials not configured. Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables."

        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        recipients = [to_email]
        if cc_email:
            msg['Cc'] = cc_email
            recipients.append(cc_email)
        msg.attach(MIMEText(message, 'plain'))

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Connect to Gmail SMTP server using a 'with' statement for proper resource management
        with smtplib.SMTP(smtp_server, smtp_port) as server: # Use SMTP, then starttls
            server.starttls(context=context) # Enable TLS encryption with context
            server.login(gmail_user, gmail_password.replace(" ", "")) # Remove spaces from app password
            server.sendmail(gmail_user, recipients, msg.as_string())
        
        logging.info(f"Email sent successfully to {to_email}")
        return f"Email sent successfully to {to_email}"

    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"Gmail authentication failed: {e}. Please check your GMAIL_USER and GMAIL_APP_PASSWORD.")
        return "Email sending failed: Authentication error. Please check your Gmail credentials and app password."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred while sending email: {e}")
        return f"Email sending failed: SMTP error - {str(e)}"
    except Exception as e:
        logging.error(f"An unexpected error occurred while sending email: {e}")
        return f"An unexpected error occurred while sending email: {str(e)}"

# --- Define _raw_schema for send_email at module level ---
send_email._raw_schema = { # type: ignore
    "type": "object",
    "name": "send_email",
    "description": "Sends an email through Gmail SMTP.",
    "parameters": {
        "type": "object",
        "properties": {
            "to_email": {"type": "string", "description": "Recipient email address"},
            "subject": {"type": "string", "description": "Email subject line"},
            "message": {"type": "string", "description": "Email body content"},
            "cc_email": {"type": "string", "description": "Optional CC email address"}
        },
        "required": ["to_email", "subject", "message"],
        "additionalProperties": False,
    }
}

