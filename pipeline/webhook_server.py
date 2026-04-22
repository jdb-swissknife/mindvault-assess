#!/usr/bin/env python3
"""
MindVault AI Assessment Pipeline - Webhook Server
Receives Retell.ai webhooks and saves transcripts for manual report generation
"""

import os
import json
import re
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Header, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
class RetellWebhookPayload(BaseModel):
    event: str
    call_id: str
    agent_id: Optional[str] = None
    call_status: Optional[str] = None
    transcript: Optional[list] = None
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
                          transcript_object: list, transcript: list):
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
        f.write(f"File: {filepath}\n")
        f.write(f"="*50 + "\n\n")
        f.write(f"TRANSCRIPT\n")
        f.write(f"="*50 + "\n\n")
        f.write(transcript_text)
    
    return filepath


async def process_call_analyzed(payload: RetellWebhookPayload):
    """Process call_analyzed event and save transcript"""
    try:
        logger.info(f"Processing call {payload.call_id}")
        
        if payload.event != "call_analyzed":
            logger.info(f"Skipping {payload.event} event")
            return
        
        # Get metadata
        metadata = payload.metadata or {}
        customer_name = metadata.get("customer_name", "Unknown")
        business_name = metadata.get("business_name", "Unknown")
        industry = metadata.get("industry", "general")
        
        # Save transcript
        filepath = await save_transcript(
            call_id=payload.call_id,
            business_name=business_name,
            customer_name=customer_name,
            industry=industry,
            duration_ms=payload.duration_ms,
            transcript_object=payload.transcript_object or [],
            transcript=payload.transcript or []
        )
        
        logger.info(f"✅ Transcript saved: {filepath}")
        logger.info(f"To generate report, ask Hermes: \"Generate assessment report from {filepath}\"")
        
    except Exception as e:
        logger.error(f"❌ Error processing call {payload.call_id}: {e}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/webhook/retell")
async def retell_webhook(request: Request, background_tasks: BackgroundTasks):
    """Receive Retell.ai webhook events"""
    try:
        payload_json = await request.json()
        payload = RetellWebhookPayload(**payload_json)
        
        logger.info(f"Received {payload.event} webhook for call {payload.call_id}")
        
        if payload.event == "call_analyzed":
            background_tasks.add_task(process_call_analyzed, payload)
        
        return JSONResponse(status_code=200, content={"status": "received"})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
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


if __name__ == "__main__":
    import uvicorn
    logger.info(f"🚀 Starting webhook server")
    logger.info(f"📁 Transcripts will be saved to: {REPORTS_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
