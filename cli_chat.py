from utils.config import load_config
from models.chatbot_model import ChatbotModel
from models.tokenizer import ChatbotTokenizer
from inference.predictor import ChatPredictor
import pyttsx3
import os

def speak(txt: str):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice',voices[0].id)
    engine.setProperty("rate",155)
    engine.setProperty('volume',1.0)
    engine.say(txt)
    engine.runAndWait()

print("🔹 Loading model... Please wait.")

conversation = ""

SYSTEM_PROMPT = """
You are an accurate Chatbot type AI assistant.
Rules:
- Answer only if you are confident.
- If you do not know, say "I don't know".
- Do not make up facts.
- Keep answers concise and factual.
- Keep answers exactly like humans very natural.
- Try to keep answers in very short in one line if its like a friendly conversation.
- Don't provide any kind of url or :) or any kind of special charactersn in conversation except".","?","!".
"""

config = load_config("configs/model.yaml")

model = ChatbotModel(
    model_name=config["model_name"],
    device=config["device"]
)

tokenizer = ChatbotTokenizer(config["model_name"])

predictor = ChatPredictor(
        model=model,
        tokenizer=tokenizer,
        config=config
    )
    
def chat_once(user_input: str) -> str:
    global conversation
    conversation += f"User: {user_input}\nBot:"
        
    prompt = SYSTEM_PROMPT + "\nUser: " + user_input + "\nAssistant:"
    response = predictor.predict(prompt)
    return response


def main():


    print("✅ Chatbot ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in {"exit", "quit", "bye", "goodbye", "see you"}:
            print("👋 Goodbye!")
            break

        conversation += f"User: {user_input}\nBot:"

        
        prompt = SYSTEM_PROMPT + "\nUser: " + user_input + "\nAssistant:"
        response = predictor.predict(prompt)


        print(f"\nBot: {response}\n")
        speak(response)

        conversation += f" {response}\n"

        # Prevent context from growing forever
        conversation = conversation[-1000:]

if __name__ == "__main__":
    main()
