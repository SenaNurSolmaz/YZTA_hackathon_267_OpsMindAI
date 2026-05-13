from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import os
import google.generativeai as genai
from datetime import datetime

router = APIRouter()

class ReportRequest(BaseModel):
    kpis: Optional[Dict[str, Any]] = None
    shipments: Optional[List[Any]] = None
    inventory: Optional[List[Any]] = None

def is_quota_error(err: str) -> bool:
    lowered = err.lower()
    return "429" in err or "quota" in lowered or "rate limit" in lowered or "resource exhausted" in lowered

@router.post("/report")
async def generate_report(req: ReportRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    if not api_key:
        print("[report] GEMINI_API_KEY tanımlı değil.")
        raise HTTPException(status_code=500, detail="Gemini API anahtarı tanımlı değil. .env.local dosyasını kontrol edin.")
        
    genai.configure(api_key=api_key)
    
    prompt = f"""OpsMind AI operasyon raporunu Türkçe olarak özetle. Verilen KPI, kargo ve stok verilerine göre 3-5 madde halinde aksiyon önerileri sun.

KPIs: {req.kpis or dict()}
Riskli Kargolar: {req.shipments or list()}
Kritik Stoklar: {req.inventory or list()}

Kısa, net ve aksiyona dönük yaz."""
    
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.4,
                max_output_tokens=512,
            )
        )
        return {"summary": response.text, "generatedAt": datetime.utcnow().isoformat()}
    except Exception as e:
        err = str(e)
        print("[report] Gemini hatası:", err)
        if is_quota_error(err):
            raise HTTPException(status_code=429, detail="Gemini API kota limiti aşıldı. Lütfen birkaç dakika sonra tekrar deneyin.")
        raise HTTPException(status_code=502, detail="Gemini raporu oluşturulamadı. Lütfen bağlantı ve model ayarlarını kontrol edin.")
