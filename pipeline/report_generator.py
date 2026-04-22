#!/usr/bin/env python3
"""
MindVault AI Assessment Report Generator
Processes transcripts and generates professional HTML reports using Claude
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

import anthropic
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ExtractedData:
    """Structured data extracted from transcript"""
    industry: str
    business_profile: Dict[str, Any]
    pain_points: List[Dict[str, str]]
    tech_stack: Dict[str, str]
    time_analysis: Dict[str, Any]
    revenue_leaks: Dict[str, Any]
    quick_wins: List[Dict[str, str]]
    mid_term_projects: List[Dict[str, str]]
    key_quotes: List[str]
    implementation_readiness: str


class ReportGenerator:
    """Generates AI Assessment reports from discovery call transcripts"""
    
    def __init__(self):
        self._client = None
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-7-sonnet-20250219")
        self.reports_dir = Path(os.getenv("REPORTS_DIR", "/root/projects/mindvault-assess/reports"))
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def client(self):
        """Lazy initialization of Anthropic client"""
        if self._client is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self._client = anthropic.Anthropic(api_key=api_key)
        return self._client
        
    def detect_industry(self, transcript: str, provided_industry: str = "general") -> str:
        """Detect industry from transcript content"""
        if provided_industry != "general":
            return provided_industry
            
        transcript_lower = transcript.lower()
        
        # Industry detection keywords based on agent-router.md
        industry_keywords = {
            "real-estate": ["realtor", "broker", "property", "listing", "showing", "mortgage", "real estate", "homes", "buyers", "sellers"],
            "home-services": ["roofing", "roof", "hvac", "ac repair", "plumbing", "electrical", "contractor", "solar", "windows", "concrete", "flooring", "remodeling"],
            "insurance-financial": ["insurance", "medicare", "carrier", "quote", "policy", "coverage", "agent"],
            "accounting": ["cpa", "accountant", "bookkeeping", "tax preparation"],
            "legal": ["lawyer", "attorney", "law firm", "legal services"],
            "healthcare": ["medical", "dental", "chiropractor", "practice"],
        }
        
        scores = {industry: 0 for industry in industry_keywords}
        
        for industry, keywords in industry_keywords.items():
            for keyword in keywords:
                if keyword in transcript_lower:
                    scores[industry] += 1
        
        # Return industry with highest score, or general
        best_match = max(scores, key=scores.get)
        return best_match if scores[best_match] > 0 else "general"
    
    def _get_extraction_prompt(self, industry: str) -> str:
        """Get the data extraction prompt based on industry"""
        
        base_prompt = """You are analyzing a discovery call transcript for an AI Assessment report.

BUSINESS INDUSTRY: {industry}

Extract the following information from the transcript and return it as a JSON object:

{{
    "business_profile": {{
        "industry_sub_vertical": "specific type within industry",
        "years_in_business": "stated or estimated",
        "team_size": "number and structure",
        "revenue_range": "annual revenue or volume metrics mentioned"
    }},
    "operational_pain_points": [
        {{
            "description": "clear description of pain point",
            "severity": "High/Med/Low based on emotional intensity and frequency mentioned"
        }}
    ],
    "current_tech_stack": {{
        "crm": "CRM name or None",
        "communication": "communication tools used",
        "scheduling": "scheduling tool or None",
        "project_management": "PM tool or None",
        "automation_platform": "Zapier/Make/None"
    }},
    "time_analysis": {{
        "admin_hours_per_week": "number stated",
        "owner_hourly_value": "estimated or stated",
        "biggest_time_wasters": ["list of activities"]
    }},
    "revenue_leaks": {{
        "lead_response_time": "time mentioned",
        "follow_up_system": "Y/N - is there a system?",
        "quote_close_rate": "% if mentioned",
        "referral_system": "Y/N"
    }},
    "quick_win_candidates": [
        {{
            "tool": "specific tool name",
            "addresses": "which pain point",
            "roi": "brief ROI estimate"
        }}
    ],
    "mid_term_projects": [
        {{
            "name": "project name",
            "scope": "brief description",
            "investment": "estimated cost range",
            "timeline": "estimated timeline"
        }}
    ],
    "key_quotes": ["2-3 verbatim quotes capturing pain and goals"],
    "implementation_readiness": "DIY/Guided/Full Service recommendation with one-sentence rationale"
}}

Industry Context for {industry}:
{industry_context}

Analyze the transcript thoroughly and output ONLY valid JSON with all fields populated based on what was discussed in the call.
"""
        
        # Industry-specific context from agent-router.md
        industry_contexts = {
            "real-estate": """Common pains: Speed-to-lead, database decay, showing coordination, transaction management
Quick Wins: Speed-to-lead AI, Smart Scheduler, Database reactivation, Listing automation
Tools: Follow Up Boss, kvCORE, LionDesk, Synthflow, Vapi, ListingAI
KPIs: Lead decay cost, database value, per-listing time cost""",
            
            "home-services": """Common pains: Missed emergency calls, estimate follow-up, dispatch efficiency, seasonal staffing
Quick Wins: Missed call text-back, Quote follow-up automation, Smart scheduling, Review automation
Tools: GoHighLevel, ServiceTitan, Jobber, Housecall Pro, CompanyCam
KPIs: Missed call cost, estimate leakage, dispatch efficiency""",
            
            "insurance-financial": """Common pains: Quote speed, reactive renewals, cross-sell gaps, compliance documentation
Quick Wins: Instant quote response, Renewal automation, Referral campaigns, Appointment booking
Tools: Better Agency, AgencyZoom, HawkSoft, Quoteburst, Ringy
KPIs: Quote-to-bind rate, retention rate, policies per client""",
            
            "general": """Common service business pains: Owner overwhelm, inconsistent follow-up, manual data entry, lack of visibility
Quick Wins: Meeting automation, Email management, Calendar scheduling, Basic CRM
Tools: Calendly, HubSpot, Zapier, Make, Notion"""
        }
        
        return base_prompt.format(
            industry=industry,
            industry_context=industry_contexts.get(industry, industry_contexts["general"])
        )
    
    async def extract_data(self, industry: str, transcript: str) -> ExtractedData:
        """Extract structured data from transcript using Claude"""
        
        extraction_prompt = self._get_extraction_prompt(industry)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            temperature=0.1,
            system="You are an expert business analyst extracting information from discovery call transcripts for AI readiness assessments. Be thorough and accurate.",
            messages=[
                {
                    "role": "user",
                    "content": f"{extraction_prompt}\n\nTRANSCRIPT:\n{transcript}"
                }
            ]
        )
        
        # Parse JSON from response
        try:
            json_content = response.content[0].text
            # Sometimes Claude wraps JSON in markdown code blocks
            json_match = re.search(r'```json\n(.*?)\n```', json_content, re.DOTALL)
            if json_match:
                json_content = json_match.group(1)
            
            data = json.loads(json_content)
            
            return ExtractedData(
                industry=industry,
                business_profile=data.get("business_profile", {}),
                pain_points=data.get("operational_pain_points", []),
                tech_stack=data.get("current_tech_stack", {}),
                time_analysis=data.get("time_analysis", {}),
                revenue_leaks=data.get("revenue_leaks", {}),
                quick_wins=data.get("quick_win_candidates", []),
                mid_term_projects=data.get("mid_term_projects", []),
                key_quotes=data.get("key_quotes", []),
                implementation_readiness=data.get("implementation_readiness", "Unknown")
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse extraction response: {e}")
    
    def _calculate_ai_readiness_score(self, data: ExtractedData) -> Dict[str, int]:
        """Calculate AI readiness score across 5 categories"""
        scores = {
            "Systems": 5,
            "Data": 5,
            "Processes": 5,
            "Team": 5,
            "Strategy": 5
        }
        
        # Systems score based on tech stack
        if data.tech_stack.get("crm") != "None":
            scores["Systems"] += 2
        if data.tech_stack.get("automation_platform") != "None":
            scores["Systems"] += 2
            
        # Data score
        if "documentation" in data.tech_stack.get("project_management", "").lower():
            scores["Data"] += 2
            
        # Processes score based on time analysis
        admin_hours = data.time_analysis.get("admin_hours_per_week", "20")
        try:
            admin_hours_int = int(re.search(r'\d+', str(admin_hours)).group() if re.search(r'\d+', str(admin_hours)) else 20)
            if admin_hours_int > 15:
                scores["Processes"] -= 2
            elif admin_hours_int > 10:
                scores["Processes"] -= 1
        except:
            pass
            
        # Team score
        team_size = data.business_profile.get("team_size", "5")
        try:
            size_match = re.search(r'\d+', str(team_size))
            if size_match:
                size = int(size_match.group())
                if size < 3:
                    scores["Team"] += 1
                elif size > 10:
                    scores["Team"] += 2
        except:
            pass
            
        # Strategy score based on revenue leak awareness
        if data.revenue_leaks.get("follow_up_system") == "Y":
            scores["Strategy"] += 1
        if data.revenue_leaks.get("referral_system") == "Y":
            scores["Strategy"] += 1
            
        # Clamp scores to 1-10
        for key in scores:
            scores[key] = max(1, min(10, scores[key]))
            
        return scores
    
    async def generate_html_report(
        self,
        data: ExtractedData,
        call_id: str,
        customer_name: str,
        business_name: str
    ) -> str:
        """Generate professional HTML report"""
        
        # Calculate readiness score
        readiness_scores = self._calculate_ai_readiness_score(data)
        overall_score = sum(readiness_scores.values()) // 5
        
        # Generate timestamp
        generated_at = datetime.now().strftime("%B %d, %Y")
        
        # Build HTML report
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Assessment Report - {business_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #6C5CE7;
            --primary-light: #A29BFE;
            --secondary: #00B894;
            --danger: #E17055;
            --warning: #FDCB6E;
            --dark: #2D3436;
            --gray: #636E72;
            --light-gray: #B2BEC3;
            --bg: #FAFAFA;
            --card-bg: #FFFFFF;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--dark);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: white;
            padding: 60px 40px;
            border-radius: 20px;
            margin-bottom: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .header .meta {{
            margin-top: 20px;
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        
        .score-card {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }}
        
        .score-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }}
        
        .score-circle {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
        }}
        
        .score-circle .number {{
            font-size: 2.5rem;
            font-weight: 700;
        }}
        
        .score-circle .label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .score-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        
        .score-item {{
            text-align: center;
            padding: 15px;
            background: var(--bg);
            border-radius: 10px;
        }}
        
        .score-item .value {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary);
        }}
        
        .score-item .name {{
            font-size: 0.8rem;
            color: var(--gray);
            margin-top: 5px;
        }}
        
        .section {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }}
        
        .section h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--dark);
        }}
        
        .section h3 {{
            font-size: 1.1rem;
            font-weight: 600;
            margin: 25px 0 15px 0;
            color: var(--primary);
        }}
        
        .pain-point {{
            padding: 15px;
            border-left: 4px solid var(--danger);
            background: var(--bg);
            margin-bottom: 15px;
            border-radius: 0 10px 10px 0;
        }}
        
        .pain-point.severity-high {{ border-left-color: var(--danger); }}
        .pain-point.severity-med {{ border-left-color: var(--warning); }}
        .pain-point.severity-low {{ border-left-color: var(--secondary); }}
        
        .quote {{
            font-style: italic;
            color: var(--gray);
            padding: 20px;
            background: var(--bg);
            border-radius: 10px;
            margin: 15px 0;
            position: relative;
        }}
        
        .quote::before {{
            content: '"';
            font-size: 3rem;
            color: var(--primary-light);
            position: absolute;
            top: -10px;
            left: 10px;
            font-family: serif;
        }}
        
        .quick-win {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: linear-gradient(135deg, rgba(0,184,148,0.1) 0%, rgba(0,184,148,0.05) 100%);
            border-radius: 12px;
            margin-bottom: 15px;
            border: 1px solid rgba(0,184,148,0.2);
        }}
        
        .quick-win .tool-name {{
            font-weight: 600;
            color: var(--secondary);
        }}
        
        .mid-term {{
            padding: 20px;
            background: var(--bg);
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 4px solid var(--primary);
        }}
        
        .tech-stack {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .tech-item {{
            padding: 15px;
            background: var(--bg);
            border-radius: 10px;
        }}
        
        .tech-item .label {{
            font-size: 0.8rem;
            color: var(--gray);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .tech-item .value {{
            font-weight: 600;
            margin-top: 5px;
        }}
        
        .roi-box {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: white;
            padding: 30px;
            border-radius: 16px;
            margin: 30px 0;
            text-align: center;
        }}
        
        .roi-box .number {{
            font-size: 3rem;
            font-weight: 700;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px;
            color: var(--gray);
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI Assessment Report</h1>
            <div class="subtitle">Custom Analysis for {business_name}</div>
            <div class="meta">Prepared for {customer_name} | Generated {generated_at}</div>
        </div>
        
        <div class="score-card">
            <div class="score-header">
                <div>
                    <h2>AI Readiness Score</h2>
                    <p style="color: var(--gray);">Benchmark across 5 key categories</p>
                </div>
                <div class="score-circle">
                    <div class="number">{overall_score}</div>
                    <div class="label">Overall</div>
                </div>
            </div>
            <div class="score-grid">
                {''.join([f'<div class="score-item"><div class="value">{s}</div><div class="name">{k}</div></div>' for k, s in readiness_scores.items()])}
            </div>
        </div>
"""
        
        # Add business overview section
        html += f"""
        <div class="section">
            <h2>🎯 Executive Summary</h2>
            <p><strong>Industry:</strong> {data.industry.replace('-', ' ').title()}</p>
            <p><strong>Business Profile:</strong> {data.business_profile.get('industry_sub_vertical', 'Service Business')}</p>
            <p><strong>Team Size:</strong> {data.business_profile.get('team_size', 'Unknown')}</p>
            <p><strong>Years in Business:</strong> {data.business_profile.get('years_in_business', 'Unknown')}</p>
            
            <h3 style="margin-top: 30px;">Recommended Implementation Approach</h3>
            <p>{data.implementation_readiness}</p>
        </div>
"""
        
        # Add pain points section
        html += """
        <div class="section">
            <h2>⚠️ Operational Pain Points</h2>
"""
        for pain in data.pain_points[:5]:  # Top 5 pain points
            severity = pain.get('severity', 'Med').lower()
            desc = pain.get('description', '')
            html += f'            <div class="pain-point severity-{severity}">{desc}</div>\n'
        html += "        </div>\n"
        
        # Add quotes section
        if data.key_quotes:
            html += """
        <div class="section">
            <h2>💬 Key Insights from Your Call</h2>
"""
            for quote in data.key_quotes[:3]:
                html += f'            <div class="quote">{quote}</div>\n'
            html += "        </div>\n"
        
        # Add tech stack section
        html += """
        <div class="section">
            <h2>🛠️ Current Technology Stack</h2>
            <div class="tech-stack">
"""
        for key, value in data.tech_stack.items():
            label = key.replace('_', ' ').title()
            html += f'                <div class="tech-item"><div class="label">{label}</div><div class="value">{value}</div></div>\n'
        html += """            </div>
        </div>
"""
        
        # Add time analysis
        html += f"""
        <div class="section">
            <h2>⏱️ Time Analysis</h2>
            <p><strong>Admin Hours per Week:</strong> {data.time_analysis.get('admin_hours_per_week', 'Unknown')}</p>
            <p><strong>Owner Hourly Value:</strong> {data.time_analysis.get('owner_hourly_value', 'Unknown')}</p>
        </div>
"""
        
        # Add quick wins
        html += """
        <div class="section">
            <h2>🚀 Quick Wins (0-30 Days)</h2>
            <p style="color: var(--gray); margin-bottom: 20px;">
                These tools can be implemented quickly and typically pay for the assessment within 90 days.
            </p>
"""
        for win in data.quick_wins[:5]:
            tool = win.get('tool', 'TBD')
            addresses = win.get('addresses', '')
            roi = win.get('roi', '')
            html += f"""            <div class="quick-win">
                <div>
                    <div class="tool-name">{tool}</div>
                    <div style="color: var(--gray); font-size: 0.9rem;">{addresses}</div>
                </div>
                <div style="color: var(--secondary); font-weight: 500;">{roi}</div>
            </div>
"""
        html += "        </div>\n"
        
        # Add mid-term projects
        html += """
        <div class="section">
            <h2>📋 Mid-Term Projects (30-90 Days)</h2>
"""
        for project in data.mid_term_projects[:3]:
            name = project.get('name', '')
            scope = project.get('scope', '')
            investment = project.get('investment', '')
            timeline = project.get('timeline', '')
            html += f"""            <div class="mid-term">
                <h4>{name}</h4>
                <p>{scope}</p>
                <p style="color: var(--gray); font-size: 0.9rem; margin-top: 10px;">
                    <strong>Investment:</strong> {investment} | <strong>Timeline:</strong> {timeline}
                </p>
            </div>
"""
        html += "        </div>\n"
        
        # Add ROI box
        html += """
        <div class="roi-box">
            <div style="font-size: 1.1rem; margin-bottom: 10px;">Projected Annual Savings</div>
            <div class="number">$15K-$30K+</div>
            <p style="opacity: 0.9; margin-top: 10px;">
                Based on industry benchmarks for businesses reclaiming 8-12 hours per week
            </p>
        </div>
        
        <div class="section" style="background: linear-gradient(135deg, rgba(108, 92, 231, 0.1) 0%, rgba(162, 155, 254, 0.05) 100%); border: 2px solid var(--primary);">
            <h2>💳 Ready to Implement?</h2>
            <p style="font-size: 1.1rem; margin: 15px 0;">
                Your <strong>$997 assessment fee</strong> is fully applicable as a credit toward any automation implementation project with MindVault.
            </p>
            <p style="color: var(--gray);">
                Think of this assessment as a deposit on your transformation. If you choose to work with us, you've already paid the first $997.
            </p>
        </div>
        
        <div class="footer">
            <p>Report generated by MindVault AI Studio</p>
            <p style="margin-top: 10px;">Questions? Contact us at apply@mindvaultstudio.net</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    async def generate_report(
        self,
        call_id: str,
        customer_name: str,
        business_name: str,
        industry: str,
        transcript: str,
        extracted_vars: Dict = None,
        analysis: Dict = None
    ) -> Dict[str, str]:
        """Full report generation pipeline"""
        
        # Step 1: Extract structured data
        print(f"Extracting data from transcript ({len(transcript)} chars)...")
        extracted_data = await self.extract_data(industry, transcript)
        
        # Step 2: Generate HTML report
        print("Generating HTML report...")
        html_content = await self.generate_html_report(
            data=extracted_data,
            call_id=call_id,
            customer_name=customer_name,
            business_name=business_name
        )
        
        # Step 3: Save report
        report_id = f"{call_id}_{datetime.now().strftime('%Y%m%d')}"
        report_path = self.reports_dir / f"{report_id}.html"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Report saved: {report_path}")
        
        return {
            "report_id": report_id,
            "report_path": str(report_path),
            "html_url": f"/reports/{report_id}.html",
            "industry": industry,
            "customer_name": customer_name,
            "business_name": business_name
        }


if __name__ == "__main__":
    import asyncio
    
    # Test the generator with sample data
    async def test():
        generator = ReportGenerator()
        
        sample_transcript = """
        AGENT: Tell me about your business, what industry are you in?
        
        CUSTOMER: I'm a roofer, been in business about 8 years now. We do residential and commercial roofing in the Phoenix area.
        
        AGENT: How big is your team?
        
        CUSTOMER: I've got 12 guys on the crew, plus my wife handles the office. She's overwhelmed honestly, trying to keep up with all the calls and scheduling.
        
        AGENT: What does your typical day look like?
        
        CUSTOMER: I'm out on jobs most of the day, but I spend at least 3-4 hours every evening doing admin stuff. Quotes, following up on estimates, trying to keep track of everything. It's burning me out.
        
        AGENT: What's your biggest frustration right now?
        
        CUSTOMER: The missed calls kill me. I get home from a job and have 15 voicemails. By the time I call back, they've already hired someone else. I probably lose 30% of leads just from not answering fast enough.
        
        AGENT: What tools are you using to manage everything?
        
        CUSTOMER: Gmail for email, spreadsheets for tracking jobs. We tried a CRM but it was too complicated. My wife uses a paper calendar for scheduling. It's a mess honestly.
        """
        
        result = await generator.generate_report(
            call_id="test_call_001",
            customer_name="John Smith",
            business_name="Smith Roofing Solutions",
            industry="home-services",
            transcript=sample_transcript
        )
        
        print(f"Generated report: {result}")
    
    asyncio.run(test())
