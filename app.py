import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables from .env file for API keys
load_dotenv()  # ensure there is a .env file in the same directory with OPENAI_API_KEY
openai_api_key = os.getenv("OPENAI_API_KEY")

# Validate that API key is provided
if openai_api_key is None or openai_api_key.strip() == "":
    raise RuntimeError("OpenAI API key not found. Please set OPENAI_API_KEY in the .env file.")

# Initialize the ChatOpenAI model (from LangChain) with the API key
# Using a moderate temperature for creative responses (like jokes)
chat_model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7)

def is_valid_email(email: str) -> bool:
    """
    Basic email validation: checks if email contains "@" and "." characters.
    This is a simple check and not a full RFC5322 validation.
    """
    if "@" not in email or "." not in email:
        return False
    return True

def classify_intent(user_message: str) -> str:
    """
    Classify the user's intent based on keyword matching.
    Returns one of: "INFO", "JOKE", "TASK", "UNKNOWN".
    """
    msg = user_message.lower()
    if any(keyword in msg for keyword in ["joke", "funny", "laugh"]):
        return "JOKE"
    if any(keyword in msg for keyword in ["book", "schedule", "appointment", "meet"]):
        return "TASK"
    if any(keyword in msg for keyword in ["info", "information", "tell me about", "help", "service"]):
        return "INFO"
    return "UNKNOWN"

def main():
    # Greet the user and collect basic information
    print("Bot: Hello! I'm here to assist you.")
    # Collect user's name
    name = input("Bot: May I have your name? \nYou: ").strip()
    if name == "":
        name = "Guest"
    # Collect user's email with validation
    email = ""
    while True:
        email = input(f"Bot: Hi {name}, please provide your email address: \nYou: ").strip()
        if is_valid_email(email):
            break
        else:
            print("Bot: That doesn't look like a valid email. Please try again.")
    print(f"Bot: Thank you, {name}! How can I assist you today?")

    # Start the conversation loop
    while True:
        user_input = input("You: ").strip()
        if user_input == "":
            # Skip empty inputs
            continue

        # Convert input to lower-case for exit check
        normalized_input = user_input.lower()
        # Check for exit keywords
        if normalized_input in ["bye", "goodbye", "exit", "quit"]:
            print("Bot: Goodbye! Have a great day.")
            break

        # Determine the intent of the user's request
        intent = classify_intent(user_input)

        try:
            if intent == "INFO":
                # Provide an informational response (static or AI-generated as needed)
                # For demonstration, we use a static response for info intent.
                print("Bot: I am a helpful assistant. I can tell you jokes or help schedule appointments. Let me know what you need!")
            elif intent == "JOKE":
                # Use the ChatOpenAI model to generate a joke
                prompt = f"Tell me a joke about {name}."
                messages = [HumanMessage(content=prompt)]
                response = chat_model.invoke(messages)  # get the AI response&#8203;:contentReference[oaicite:0]{index=0}&#8203;:contentReference[oaicite:1]{index=1}
                joke = response.content.strip()
                print("Bot: " + (joke if joke else "Sorry, I couldn't fetch a joke this time."))
            elif intent == "TASK":
                # Handle booking an appointment
                print("Bot: Sure, I can help with appointments.")
                print("Bot: Would you like to book an appointment now? (yes/no)")
                confirm = input("You: ").strip().lower()
                if confirm in ["yes", "y"]:
                    # In a real application, you'd collect details like date/time here
                    print("Bot: Great! I've scheduled an appointment for you. (This is a demo, so no real booking was made.)")
                else:
                    print("Bot: Alright, I won't book an appointment. Let me know if you need anything else.")
            else:  # UNKNOWN intent
                print("Bot: I'm sorry, I didn't understand that. Could you rephrase or try a different request?")
        except Exception as e:
            # Handle any errors from the LLM (API call failures, etc.)
            print("Bot: Oops, something went wrong while generating a response. Please try again.")

        # After responding, check if the user wants anything else
        print("Bot: Can I help you with anything else? (yes/no)")
        again = input("You: ").strip().lower()
        if again in ["no", "n", "nope"]:
            print("Bot: Alright. Thank you for chatting! Goodbye.")
            break
        else:
            print("Bot: Sure, I'm here to help. What else can I do for you?")

if __name__ == "__main__":
    main()
