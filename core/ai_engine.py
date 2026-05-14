import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
API_URL = "https://api.mistral.ai/v1/chat/completions"

async def get_ai_review(code_text: str, mode: str, model: str):
    prompts = {
        "Стандартный": "Ты Senior Developer. Оцени качество кода от 1 до 10. В ПЕРВОЙ строке ответа напиши строго: 'Оценка: [число]/10'. 10 - идеально, 1 - ужасно. Затем распиши ошибки и PEP8.",
        "Безопасность": "Ты эксперт по безопасности. Оцени защищенность от 1 до 10. В ПЕРВОЙ строке напиши строго: 'Оценка: [число]/10'. 1 - критические уязвимости, 10 - полная защита. Найди дыры в защите.",
        "Оптимизация": "Ты эксперт по производительности. Оцени эффективность от 1 до 10. В ПЕРВОЙ строке напиши строго: 'Оценка: [число]/10'. 1 - медленный код, 10 - максимальная скорость. Предложи ускорение."
    }

    headers = {
        "Authorization": f"Bearer {MISTRAL_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system", 
                "content": f"{prompts.get(mode, 'Стандартный')} Отвечай на русском языке. Будь строг, не завышай оценки."
            },
            {
                "role": "user", 
                "content": f"Проанализируй этот код:\n\n{code_text}"
            }
        ],
        "temperature": 0.1 
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, headers=headers, json=payload, timeout=30) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result['choices'][0]['message']['content']
                else:
                    return f"Ошибка API {resp.status}"
        except Exception as e:
            return f"Ошибка соединения: {str(e)}"