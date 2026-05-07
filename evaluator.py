from llm import client
import re

def evaluate(query, answers, models):
    if not answers:
        return {"error": "No valid responses generated."}

    formatted = ""
    for i, a in enumerate(answers):
        formatted += f"Model {i+1} ({models[i]}):\n{a}\n\n"

    # Precise multi-metric prompt
    prompt = f"""
    You are an AI judge evaluating model responses for a technical ensemble.
    
    Query: {query}
    Answers: {formatted}

    Task:
    For each model, provide a score (1-10) for:
    1. Accuracy (Factuality)
    2. Completeness (Depth of response)
    3. Relevance (Alignment with query)
    4. Efficiency (Conciseness vs. Value)
    5. Cost (Estimated token efficiency/complexity)

    Return your response in this EXACT format:
    WINNER: [Model Name]
    REASONING: [Brief justification]
    SCORES: [Model 1 Name]:[Average %], [Model 2 Name]:[Average %], [Model 3 Name]:[Average %]
    """

    res = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = res.choices[0].message.content
    
    try:
        # Extract Winner
        winner_match = re.search(r"WINNER:\s*(.*)", content)
        winner = winner_match.group(1) if winner_match else "Tie"
        
        # Extract Reasoning
        reasoning_match = re.search(r"REASONING:\s*(.*)", content)
        reasoning = reasoning_match.group(1) if reasoning_match else "Analysis complete."
        
        # Extract Scores for the Race Track UI
        scores_raw = re.search(r"SCORES:\s*(.*)", content).group(1)
        score_map = {}
        for item in scores_raw.split(','):
            name, val = item.split(':')
            # Extract the numeric percentage
            score_num = int(re.search(r'\d+', val).group())
            score_map[name.strip()] = score_num
            
        return {"winner": winner, "reasoning": reasoning, "scores": score_map}
    except Exception as e:
        # Fallback if parsing fails
        return {
            "winner": "System Error", 
            "reasoning": f"Parsing failed. Raw Judge Output: {content}", 
            "scores": {m: 50 for m in models}
        }