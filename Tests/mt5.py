# Load model directly
from transformers import AutoTokenizer, AutoModel

from transformers import pipeline

pipe = pipeline("text2text-generation", model="google/mt5-large")
pipe("This restaurant is awesome")
