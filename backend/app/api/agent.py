from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import google.generativeai as genai

router = APIRouter()

class AgentRequest(BaseModel):
    prompt: str
    context: Optional[str] = None

def is_quota_error(err: str) -> bool:
    lowered = err.lower()
    return "429" in err or "quota" in lowered or "rate limit" in lowered or "resource exhausted" in lowered

@router.post("/agent")
async def generate_agent_response(req: AgentRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    if not api_key or api_key == "SIMULATION_KEY" or api_key.strip() == "":
        print("[agent] GEMINI_API_KEY tanımlı değil veya simülasyon modunda. Simülasyon yanıtı üretiliyor.")
        return {"result": f"Simulasyon yaniti: Bilgi tabaninda '{req.prompt}' ile ilgili asagidaki bilgileri buldum: {req.context[:100]}..."}
        
    genai.configure(api_key=api_key)
    
    system_context = f"Bağlam:\n{req.context}\n\n" if req.context else ""
    full_prompt = f"{system_context}{req.prompt}"
    
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.5,
                max_output_tokens=512,
            )
        )
        return {"result": response.text}
    except Exception as e:
        err = str(e)
        print("[agent] Gemini hatası:", err)
        if is_quota_error(err):
            raise HTTPException(status_code=429, detail="Gemini API kota limiti aşıldı. Lütfen birkaç dakika sonra tekrar deneyin.")
        raise HTTPException(status_code=502, detail="Gemini yanıtı oluşturulamadı. Lütfen bağlantı ve model ayarlarını kontrol edin.")
