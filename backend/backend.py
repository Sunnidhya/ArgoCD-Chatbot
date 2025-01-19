from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Initialize FastAPI
app = FastAPI()

# Load GPT-2 model and tokenizer
model_name = "gpt2"  # You can also use "gpt2-medium", "gpt2-large", etc., for better performance.
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Input schema
class Query(BaseModel):
    question: str
    context: str

@app.post("/ask")
async def ask_question(query: Query):
    try:
        # Construct the input prompt
        prompt = f"Context: {query.context}\nQuestion: {query.question}\nAnswer:"

        # Generate the response
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs, max_length=200, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract the answer portion
        answer = answer.split("Answer:")[-1].strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))