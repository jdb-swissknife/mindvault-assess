#!/usr/bin/env python3
"""
MindVault AI Assessment Pipeline - Webhook Server
Receives Retell.ai webhooks and triggers report generation
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Header, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import logging

from report_generator import ReportGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MindVault AI Assessment Pipeline",
    description="Webhook receiver for Retell.ai discovery calls",
    version="1.0.0"
)

# Webhook secret for verification
WEBHOOK_SECRET = os.getenv("RETELL_WEBHOOK_SECRET", "")
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/root/projects/mindvault-assess/reports"))
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# Retell webhook event models
class RetellTranscriptTurn(BaseModel):
    role: str
    content: str


class RetellWebhookPayload(BaseModel):
    event: str  # call_started, call_ended, call_analyzed
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
    call_type: Optional[str] = None  # inbound or outbound
    metadata: Optional[Dict[str, Any]] = None
    analysis: Optional[Dict[str, Any]] = None
    extracted_variables: Optional[Dict[str, Any]] = None


# Initialize report generator
report_generator = None


@app.on_event("startup")
async def startup_event():
    global report_generator
    report_generator = ReportGenerator()
    logger.info("Report generator initialized")


async def process_call_analyzed(payload: RetellWebhookPayload):
    """Process call_analyzed event and generate report"""
    try:
        logger.info(f"Processing call {payload.call_id} - {payload.event}")
        
        # Skip if not the analyzed event (we only care about call_analyzed)
        if payload.event != "call_analyzed":
            logger.info(f"Skipping {payload.event} event")
            return
        
        # Get customer info from metadata or extract from transcript
        customer_name = "Unknown"
        business_name = "Unknown"
        industry = "general"
        
        if payload.metadata:
            customer_name = payload.metadata.get("customer_name", "Unknown")
            business_name = payload.metadata.get("business_name", "Unknown")
            industry = payload.metadata.get("industry", "general")
        
        # Build transcript text from turns
        transcript_text = ""
        if payload.transcript_object:
            for turn in payload.transcript_object:
                role = turn.get("role", "unknown")
                content = turn.get("content", "")
                transcript_text += f"{role.upper()}: {content}\n\n"
        elif payload.transcript:
            transcript_text = "\n".join(payload.transcript)
        
        if not transcript_text:
            logger.warning(f"No transcript found for call {payload.call_id}")
            return
        
        # Detect industry from transcript if not provided
        detected_industry = report_generator.detect_industry(transcript_text, industry)
        
        # Generate report
        logger.info(f"Generating report for {business_name} ({detected_industry})")
        
        report_data = await report_generator.generate_report(
            call_id=payload.call_id,
            customer_name=customer_name,
            business_name=business_name,
            industry=detected_industry,
            transcript=transcript_text,
            extracted_vars=payload.extracted_variables or {},
            analysis=payload.analysis or {}
        )
        
        logger.info(f"Report generated: {report_data['report_path']}")
        
        # Send notification email if configured
        if os.getenv("SEND_EMAIL_ON_COMPLETE", "false").lower() == "true":
            await send_report_email(report_data)
            
    except Exception as e:
        logger.error(f"Error processing call {payload.call_id}: {str(e)}")
        raise


async def send_report_email(report_data: Dict):
    """Send email with report link"""
    # TODO: Implement email sending (Himalaya or SMTP)
    logger.info(f"Would send email for report: {report_data['report_id']}")


async def verify_webhook_signature(request: Request, x_retell_signature: Optional[str] = Header(None)):
    """Verify Retell webhook signature if secret is configured"""
    if not WEBHOOK_SECRET:
        return True
    
    if not x_retell_signature:
        raise HTTPException(status_code=401, detail="Missing webhook signature")
    
    # TODO: Implement signature verification per Retell docs
    # For now, just check presence if secret is configured
    return True


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/webhook/retell")
async def retell_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
):
    """
    Receive Retell.ai webhook events
    Handles: call_started, call_ended, call_analyzed
    Only processes call_analyzed to generate reports
    """
    try:
        # Parse JSON payload
        payload_json = await request.json()
        payload = RetellWebhookPayload(**payload_json)
        
        logger.info(f"Received {payload.event} webhook for call {payload.call_id}")
        
        # Process in background to respond quickly
        if payload.event == "call_analyzed":
            background_tasks.add_task(process_call_analyzed, payload)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "received",
                "call_id": payload.call_id,
                "event": payload.event
            }
        )
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/reports/{report_id}")
async def get_report(report_id: str):
    """Retrieve a generated report"""
    report_path = REPORTS_DIR / f"{report_id}.html"
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    return JSONResponse(
        status_code=200,
        content={
            "report_id": report_id,
            "html_url": f"/reports/{report_id}.html",
            "pdf_url": f"/reports/{report_id}.pdf"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
