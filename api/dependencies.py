from models.chatbot_model import ChatbotModel
from models.tokenizer import ChatbotTokenizer
from inference.predictor import ChatPredictor
from utils.config import load_config

config = load_config("configs/model.yaml")

tokenizer = ChatbotTokenizer(config["model_name"])
model = ChatbotModel(
    model_name=config["model_name"],
    device=config["device"]
)

predictor = ChatPredictor(
    model=model,
    tokenizer=tokenizer,
    config=config
)
