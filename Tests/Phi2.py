# # Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM
#
# device = "cuda"
#
# tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", trust_remote_code=True)
#
#
# inputs = tokenizer('''def print_prime(n):
#    """
#    Print all primes between 1 and n
#    """''', return_tensors="pt", return_attention_mask=False)
#
# outputs = model.generate(**inputs, max_length=200)
# text = tokenizer.batch_decode(outputs)[0]
# print(text)
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the finetuned model
finetuned_model = AutoModelForCausalLM.from_pretrained("Manoj21k/microsoft-phi-2-finetuned", trust_remote_code=True)

# Tokenize input with instruction and generate output
tokenizer = AutoTokenizer.from_pretrained("Manoj21k/microsoft-phi-2-finetuned")
input_text = "Instruct: Issue with the delivered product"
inputs = tokenizer(input_text, return_tensors="pt", return_attention_mask=False)
output = finetuned_model.generate(**inputs, max_length=200)

# Decode and print the generated text
decoded_output = tokenizer.batch_decode(output)[0]
print(decoded_output)
