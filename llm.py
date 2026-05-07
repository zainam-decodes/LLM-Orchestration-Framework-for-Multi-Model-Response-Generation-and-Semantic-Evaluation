import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Pool of backup models for fallback
RESERVE_MODELS = [
    "anthropic/claude-3-haiku",
    "google/gemini-flash-1.5",
    "meta-llama/llama-3.1-8b-instruct",
    "perplexity/sonar-small-online"
]

def call_model(model, query, task_context):
    system_msg = f"Task Context: {task_context}. Provide a detailed, technical, and comprehensive response."
    try:
        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": query}
            ],
            timeout=15.0 # Set timeout to trigger fallback faster
        )
        return res.choices[0].message.content, None
    except Exception as e:
        return None, str(e)

def run_models(query, selected_models, task_context):
    responses = []
    used_models = []
    
    # Keep track of models currently in the "active" set to avoid duplicates during fallback
    all_attempted = set(selected_models)

    for m in selected_models:
        ans, err = call_model(m, query, task_context)
        
        # --- FALLBACK LOGIC ---
        if err:
            fallback_success = False
            # Iterate through reserves to find one not already selected
            for backup in RESERVE_MODELS:
                if backup not in all_attempted:
                    all_attempted.add(backup)
                    ans_fb, err_fb = call_model(backup, query, task_context)
                    
                    if not err_fb:
                        responses.append(f"(FALLBACK ACTIVE: {backup})\n\n{ans_fb}")
                        used_models.append(backup)
                        fallback_success = True
                        break
            
            if not fallback_success:
                responses.append(f"Critical Failure: {m} and all fallbacks failed.")
                used_models.append(m)
        else:
            responses.append(ans)
            used_models.append(m)

    return responses, used_models