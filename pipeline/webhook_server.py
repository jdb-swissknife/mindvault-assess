#!/usr/bin/env python3
"""
MindVault AI Assessment Pipeline - Webhook Server
Receives Retell.ai webhooks and forwards to Hunter's VPS CRM
"""

import os
import json
import re
import asyncio
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union

from fastapi import FastAPI, HTTPException, Header, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hunter's VPS configuration
HUNTER_INTAKE_URL = os.getenv("HUNTER_INTAKE_URL", "https://app.mindvaultstudio.net/api/intake")
INTAKE_SECRET = os.getenv("INTAKE_SECRET", "de7d6f7b8bb07cb90fb14fc7f6f9db3bd249a0993db4b858")

# Initialize FastAPI
app = FastAPI(
    title="MindVault AI Assessment Pipeline",
    description="Webhook receiver for Retell.ai discovery calls",
    version="1.0.0"
)

# Configuration
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/root/projects/mindvault-assess/reports"))
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# Models
class RetellCallData(BaseModel):
    call_id: str
    agent_id: Optional[str] = None
    call_status: Optional[str] = None
    transcript: Optional[Union[str, list]] = None
    transcript_object: Optional[list] = None
    recording_url: Optional[str] = None
    start_timestamp: Optional[int] = None
    end_timestamp: Optional[int] = None
    duration_ms: Optional[int] = None
    customer_number: Optional[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    call_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    analysis: Optional[Dict[str, Any]] = None
    extracted_variables: Optional[Dict[str, Any]] = None

class RetellWebhookPayload(BaseModel):
    event: str
    call: Optional[RetellCallData] = None
    # Support flat structure too
    call_id: Optional[str] = None
    agent_id: Optional[str] = None
    call_status: Optional[str] = None
    transcript: Optional[Union[str, list]] = None
    transcript_object: Optional[list] = None
    recording_url: Optional[str] = None
    start_timestamp: Optional[int] = None
    end_timestamp: Optional[int] = None
    duration_ms: Optional[int] = None
    customer_number: Optional[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    call_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    analysis: Optional[Dict[str, Any]] = None
    extracted_variables: Optional[Dict[str, Any]] = None


async def save_transcript(call_id: str, business_name: str, customer_name: str, 
                          industry: str, duration_ms: Optional[int],
                          transcript_object: list, transcript: list, metadata: dict = None):
    """Save transcript to file for manual report generation"""
    
    # Build transcript text
    transcript_text = ""
    if transcript_object:
        for turn in transcript_object:
            role = turn.get("role", "unknown")
            content = turn.get("content", "")
            transcript_text += f"{role.upper()}: {content}\n\n"
    elif transcript:
        transcript_text = "\n".join(transcript)
    
    if not transcript_text:
        raise ValueError("No transcript content found")
    
    # Extract email from metadata if exists
    contact_email = metadata.get("contact_email") if metadata else None
    contact_phone = metadata.get("contact_phone") if metadata else None
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_business = re.sub(r'[^\w\s-]', '', business_name).replace(' ', '_')[:30]
    filename = f"{safe_business}_{timestamp}_{call_id[:8]}.txt"
    filepath = REPORTS_DIR / filename
    
    # Write file with metadata
    with open(filepath, 'w') as f:
        f.write(f"CALL METADATA\n")
        f.write(f"="*50 + "\n")
        f.write(f"Business: {business_name}\n")
        f.write(f"Customer: {customer_name}\n")
        f.write(f"Industry: {industry}\n")
        f.write(f"Call ID: {call_id}\n")
        f.write(f"Date: {datetime.now().isoformat()}\n")
        if duration_ms:
            f.write(f"Duration: {duration_ms // 1000}s\n")
        if contact_email:
            f.write(f"Contact Email: {contact_email}\n")
        if contact_phone:
            f.write(f"Contact Phone: {contact_phone}\n")
        f.write(f"File: {filepath}\n")
        f.write(f"="*50 + "\n\n")
        f.write(f"TRANSCRIPT\n")
        f.write(f"="*50 + "\n\n")
        f.write(transcript_text)
    
    return filepath, transcript_text


async def forward_to_hunter(payload: dict) -> bool:
    """Forward transcript to Hunter's VPS CRM intake endpoint using curl"""
    def _curl_forward():
        try:
            # Write payload to temp file to avoid shell escaping issues
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(payload, f)
                temp_path = f.name
            
            cmd = [
                'curl', '-s', '-X', 'POST',
                HUNTER_INTAKE_URL,
                '-H', 'Content-Type: application/json',
                '-H', f'X-Intake-Secret: {INTAKE_SECRET}',
                '-d', f'@{temp_path}',
                '--max-time', '30'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            if result.returncode == 0 and 'intake_id' in result.stdout:
                return True
            else:
                logger.error(f"❌ Curl failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error forwarding to Hunter: {e}")
            return False
    
    # Run blocking curl in thread pool
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _curl_forward)
    
    if result:
        logger.info(f"✅ Forwarded to Hunter's VPS: {payload.get('company_name')}")
    return result


async def process_call_analyzed(payload: RetellWebhookPayload):
    """Process call_analyzed event, save locally and forward to Hunter's VPS"""
    try:
        # Handle nested structure (Retell format: {"event": "...", "call": {...}})
        if payload.call:
            call_data = payload.call
            call_id = call_data.call_id
            transcript_object = call_data.transcript_object or call_data.transcript or []
            duration_ms = call_data.duration_ms
            metadata = call_data.metadata or {}
        else:
            # Handle flat structure
            call_id = payload.call_id
            transcript_object = payload.transcript_object or payload.transcript or []
            duration_ms = payload.duration_ms
            metadata = payload.metadata or {}
        
        logger.info(f"Processing call {call_id}")
        
        if payload.event != "call_analyzed":
            logger.info(f"Skipping {payload.event} event")
            return
        
        # Extract metadata from Retell (prioritize extracted_variables, fallback to metadata)
        extracted = call_data.extracted_variables if hasattr(call_data, 'extracted_variables') and call_data.extracted_variables else {}
        
        customer_name = extracted.get("contact_name") or metadata.get("customer_name", "Unknown")
        business_name = extracted.get("business_name") or metadata.get("business_name", "Unknown")
        industry = metadata.get("industry", "general")
        contact_email = extracted.get("contact_email") or metadata.get("contact_email", "")
        contact_phone = extracted.get("contact_phone") or metadata.get("contact_phone", "")
        
        # Save transcript locally (backup)
        filepath, transcript_text = await save_transcript(
            call_id=call_id,
            business_name=business_name,
            customer_name=customer_name,
            industry=industry,
            duration_ms=duration_ms,
            transcript_object=transcript_object,
            transcript=[],
            metadata=metadata
        )
        
        logger.info(f"✅ Transcript saved locally: {filepath}")
        
        # Format duration as mm:ss
        if duration_ms:
            mins = duration_ms // 60000
            secs = (duration_ms % 60000) // 1000
            call_duration = f"{mins}:{secs:02d}"
        else:
            call_duration = "Unknown"
        
        # Build payload for Hunter's VPS
        hunter_payload = {
            "company_name": business_name,
            "contact_name": customer_name,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "call_id": call_id,
            "call_duration": call_duration,
            "transcript": transcript_text,
            "industry": industry,
            "notes": f"AI Interview completed. Transcript saved to {filepath}"
        }
        
        # Forward to Hunter's VPS
        forwarded = await forward_to_hunter(hunter_payload)
        
        if forwarded:
            logger.info(f"🎯 Client {business_name} forwarded to Hunter for CRM tracking")
        else:
            logger.warning(f"⚠️  Forward failed for {business_name}, but local backup exists")
        
    except Exception as e:
        logger.error(f"❌ Error processing call: {e}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/webhook/retell")
async def retell_webhook(request: Request, background_tasks: BackgroundTasks):
    """Receive Retell.ai webhook events"""
    try:
        payload_json = await request.json()
        
        # DEBUG: Log what we received
        logger.info(f"RAW WEBHOOK RECEIVED: {json.dumps(payload_json, indent=2)[:500]}")
        
        payload = RetellWebhookPayload(**payload_json)
        
        logger.info(f"Received {payload.event} webhook")
        
        if payload.event == "call_analyzed":
            background_tasks.add_task(process_call_analyzed, payload)
        
        return JSONResponse(status_code=200, content={"status": "received"})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        logger.error(f"Failed payload: {json.dumps(payload_json, indent=2)[:500]}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/reports")
async def list_transcripts():
    """List all saved transcripts"""
    files = sorted(REPORTS_DIR.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)
    return {
        "transcripts": [
            {
                "filename": f.name,
                "path": str(f),
                "size": f.stat().st_size,
                "created": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
            }
            for f in files[:20]
        ]
    }


from fastapi.responses import FileResponse, HTMLResponse

APP_REPORTS_DIR = Path("/root/projects/mindvault-assess/app/reports")

@app.get("/reports/view/{filename}", response_class=HTMLResponse)
async def view_report(filename: str):
    """View an HTML report"""
    filepath = APP_REPORTS_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    with open(filepath, 'r') as f:
        content = f.read()
    return content


@app.get("/reports/download/{filename}")
async def download_report(filename: str):
    """Download an HTML report"""
    filepath = APP_REPORTS_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(filepath, media_type='text/html', filename=filename)


if __name__ == "__main__":
    import uvicorn
    logger.info(f"🚀 Starting webhook server")
    logger.info(f"📁 Transcripts will be saved to: {REPORTS_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
