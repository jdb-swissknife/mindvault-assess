#!/usr/bin/env python3
"""
Test report generation WITHOUT API key
Uses mock data to verify HTML template and styling
"""

from report_generator import ReportGenerator, ExtractedData
from datetime import datetime
import asyncio

async def test_mock_report():
    """Generate a sample report with mock data"""
    
    # Create mock extracted data
    mock_data = ExtractedData(
        industry="home-services",
        business_profile={
            "industry_sub_vertical": "Roofing / Residential & Commercial",
            "years_in_business": "8 years",
            "team_size": "13 (12 crew + 1 office)",
            "revenue_range": "$2M-$3M annually (estimated)"
        },
        pain_points=[
            {
                "description": "Losing 30% of leads due to slow response time - voicemails pile up while on jobs",
                "severity": "High"
            },
            {
                "description": "Owner spending 3-4 hours every evening on admin work - 'second shift' burnout",
                "severity": "High"
            },
            {
                "description": "Office manager (wife) overwhelmed juggling calls, scheduling, and follow-up manually",
                "severity": "Med"
            },
            {
                "description": "No CRM - using Gmail, spreadsheets, and paper calendar - duplicate data entry",
                "severity": "Med"
            },
            {
                "description": "Zero automation - everything manual between tools",
                "severity": "Med"
            }
        ],
        tech_stack={
            "crm": "None (spreadsheets)",
            "communication": "Gmail",
            "scheduling": "Paper calendar",
            "project_management": "Spreadsheets",
            "automation_platform": "None"
        },
        time_analysis={
            "admin_hours_per_week": "15-20 hours",
            "owner_hourly_value": "$75-100/hr",
            "biggest_time_wasters": ["Evening admin work", "Manual follow-up", "Duplicate data entry", "Scheduling coordination"]
        },
        revenue_leaks={
            "lead_response_time": "2-8 hours (often next day)",
            "follow_up_system": "N",
            "quote_close_rate": "Unknown (low tracking)",
            "referral_system": "N"
        },
        quick_wins=[
            {
                "tool": "AI Missed Call Text-Back",
                "addresses": "30% lead loss from slow response",
                "roi": "Capture 8-12 additional leads/month = $24K-48K annually"
            },
            {
                "tool": "Smart Scheduling (Calendly + SMS)",
                "addresses": "Scheduling coordination burden",
                "roi": "Save 5+ hrs/week on phone tag = $15K annually"
            },
            {
                "tool": "Quote Follow-Up Automation",
                "addresses": "No systematic quote follow-up",
                "roi": "Close 15-20% more estimates = $30K+ annually"
            },
            {
                "tool": "CompanyCam Integration",
                "addresses": "Photo chaos on crew phones",
                "roi": "Faster estimates, professional proposals = $10K annually"
            },
            {
                "tool": "Review Automation",
                "addresses": "No systematic review generation",
                "roi": "More 5-star reviews = higher close rates"
            }
        ],
        mid_term_projects=[
            {
                "name": "End-to-End Job Management",
                "scope": "Implement Jobber or Housecall Pro for full workflow automation",
                "investment": "$3K-5K setup + $200-400/mo",
                "timeline": "60-90 days"
            },
            {
                "name": "AI Voice Agent for Inbound",
                "scope": "24/7 AI answering service with appointment booking",
                "investment": "$2K-3K setup + $0.15/min",
                "timeline": "45-60 days"
            },
            {
                "name": "Maintenance Membership Program",
                "scope": "Automated recurring inspections with AI scheduling",
                "investment": "$1.5K-2.5K",
                "timeline": "30-45 days"
            }
        ],
        key_quotes=[
            "The missed calls kill me. I get home from a job and have 15 voicemails. By the time I call back, they've already hired someone else.",
            "I spend at least 3-4 hours every evening doing admin stuff. It's burning me out. It's like working two jobs.",
            "I just want my evenings back. I'd love to spend time with my kids instead of drowning in spreadsheets."
        ],
        implementation_readiness="Guided Setup recommended - business has clear pain points and owner is motivated, but no current automation foundation. Owner needs hands-on help with initial setup and training."
    )
    
    # Create generator (will fail on API calls, but we can use the HTML gen directly)
    generator = ReportGenerator()
    
    # Generate HTML directly with mock data
    html_content = await generator.generate_html_report(
        data=mock_data,
        call_id="demo_call_001",
        customer_name="Mike",
        business_name="Desert Peak Roofing"
    )
    
    # Save report
    report_path = f"/root/projects/mindvault-assess/reports/demo_report_{datetime.now().strftime('%Y%m%d')}.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Demo report generated: {report_path}")
    return report_path

if __name__ == "__main__":
    path = asyncio.run(test_mock_report())
    print(f"\nOpen in browser: file://{path}")
