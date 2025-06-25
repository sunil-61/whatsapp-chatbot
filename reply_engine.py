from openai import OpenAI

client = OpenAI(
    api_key="your-api-key-here", 
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "Authorization": "Bearer your-api-key-here",  
        "HTTP-Referer": "https://openrouter.ai",  
        "X-Title": "WhatsappGPTBot"
    }
)

def get_reply(msg):
    try:
        print(f"📩 Asking OpenRouter: {msg}")
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo-0613", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that understands Hindi and Hinglish."},
                {"role": "user", "content": msg}
            ],
            temperature=0.7,
            max_tokens=100
        )
        reply = response.choices[0].message.content.strip()
        print(f"🤖 OpenRouter replied: {reply}")
        return reply

    except Exception as e:
        print("❌ OpenRouter Error:", type(e).__name__, str(e))
        return f"❗ Error: {type(e).__name__} - {str(e)}"
