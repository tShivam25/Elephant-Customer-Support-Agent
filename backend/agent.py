import os
import json
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
from groq import Groq
from backend.tools import TOOLS_SCHEMA, execute_tool
from backend.memory import MemoryManager

# Use the environment variable, but set a fallback for the Groq client if not provided
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "mock_key"))
MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b") # Better default for tool calling

memory_manager = MemoryManager()

SYSTEM_PROMPT = """You are ResolveMind, an advanced customer support AI for a SaaS billing/invoicing company.
Your goal is to solve customer problems efficiently. 
You have access to tools to look up customer data, search the Knowledge Base, check system status, create tickets, and escalate to humans.
Be polite, professional, and empathetic. 

When you receive relevant memory facts from previous interactions, YOU MUST USE THEM.
Never suggest a fix that is marked as 'failed' in the customer's history. 
If an issue repeats or a fix fails multiple times, escalate it instead of guessing.
Adapt your tone based on the customer's known preferences.
Always explain your reasoning briefly to the user if you are skipping a step because it failed before.
"""

def extract_facts(messages: List[Dict[str, Any]]) -> List[str]:
    """Uses LLM to extract 1-3 useful facts from the conversation to retain."""
    transcript = "\n".join([f"{m['role']}: {m.get('content', '')}" for m in messages if m['role'] in ['user', 'assistant'] and m.get('content')])
    
    prompt = f"""
    Based on the following customer support transcript, extract 1 to 3 distinct, concise facts that would be useful for a support agent to remember in the future.
    Only extract facts about: the issue, the root cause, what fix was attempted and its outcome, customer preferences, or open promises.
    Do not store small talk. If nothing useful was discussed, return an empty list.
    Respond with a JSON object containing a single key "facts" which is a list of strings.
    
    Transcript:
    {transcript}
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return data.get("facts", [])
    except Exception as e:
        print(f"Extraction error: {e}")
        return []

def run_agent(customer_id: str, user_message: str, use_memory: bool = True) -> Dict[str, Any]:
    memories_used = []
    tools_used = []
    facts_stored = []
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if use_memory:
        recalled = memory_manager.recall(customer_id, user_message)
        if recalled:
            memories_used = [r.get("content", str(r)) for r in recalled[:3]] # limit to top 3
            memory_context = "Relevant Customer Memories:\n" + "\n".join([f"- {m}" for m in memories_used])
            messages.append({"role": "system", "content": memory_context})

    messages.append({"role": "user", "content": user_message})
    
    loop_count = 0
    max_loops = 4
    
    while loop_count < max_loops:
        loop_count += 1
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                temperature=0.2
            )
        except Exception as e:
            return {"reply": f"Error calling AI model: {e}", "memories": memories_used, "tools": tools_used, "facts_stored": facts_stored}

        msg = response.choices[0].message
        
        # Check if we got a normal reply
        if not msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content})
            break
            
        # Add the tool calls message to history
        messages.append(msg)
        
        # Execute tools
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            try:
                args = json.loads(tool_call.function.arguments)
            except:
                args = {}
                
            tools_used.append({"name": fn_name, "args": args})
            result = execute_tool(fn_name, args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": fn_name,
                "content": json.dumps(result)
            })

    # Final reply is the last assistant message
    final_reply = messages[-1].get("content", "")
    
    if use_memory:
        new_facts = extract_facts([{"role": "user", "content": user_message}, {"role": "assistant", "content": final_reply}])
        for fact in new_facts:
            success = memory_manager.retain(customer_id, fact)
            if success:
                facts_stored.append(fact)

    return {
        "reply": final_reply,
        "memories": memories_used,
        "tools": tools_used,
        "facts_stored": facts_stored,
        "decision_summary": f"Agent ran {loop_count} iterations, using {len(tools_used)} tools."
    }
