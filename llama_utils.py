import ollama

def get_llama_response(prompt):
    response = ollama.chat(
        model="mistral",  # ✅ switched from "llama3" to "mistral"
        messages=[
            {"role": "user", "content": f"Explain this topic in simple terms: {prompt}"}
        ],
        options={"num_predict": 150}  # Optional: Limit output size
    )
    return response['message']['content']
