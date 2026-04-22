# MindVault AI Assessment Pipeline

**Automated report generation from Retell.ai discovery calls**

Receives webhook events from Retell voice agents, extracts structured data using Claude, and generates professional HTML assessment reports.

## Architecture

```
Retell Voice Agent → Webhook → FastAPI Server → Claude Data Extraction → HTML Report → Client Delivery
```

## Quick Start

### 1. Setup Environment

```bash
cd /root/projects/mindvault-assess/pipeline
cp .env.example .env
# Edit .env with your API keys
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
python webhook_server.py
```

Server starts on `http://0.0.0.0:8000`

### 4. Configure Retell Webhook

In your Retell dashboard:
- Go to **Monitoring → Webhooks**
- Add endpoint: `http://your-server:8000/webhook/retell`
- Select events: `call_analyzed`

## API Endpoints

### Webhooks

- `POST /webhook/retell` - Receive Retell call events
- `GET /health` - Health check

### Reports

- `GET /reports/{report_id}` - Get report metadata
- Static HTML files served from `/reports/` directory

## Report Generation Flow

1. **Call Completed** - Retell sends `call_analyzed` webhook
2. **Transcript Received** - Server extracts transcript + metadata
3. **Industry Detection** - Auto-detect industry from keywords
4. **Data Extraction** - Claude analyzes transcript → structured data
5. **Score Calculation** - AI readiness score across 5 categories
6. **HTML Generation** - Professional styled report generated
7. **File Saved** - Report stored in `/reports/{call_id}_{date}.html`

## Industry Detection

Automatically detects from transcript keywords:

- **Real Estate**: realtor, broker, property, listing, showing
- **Home Services**: roofing, HVAC, plumbing, solar, contractor
- **Insurance**: insurance, Medicare, policy, quote, carrier
- **+ more in report_generator.py**

## Data Extraction

Claude extracts:

- Business profile (size, revenue, years)
- Operational pain points (scored by severity)
- Current technology stack
- Time analysis (admin hours, hourly value)
- Revenue leaks (response time, follow-up systems)
- Quick win recommendations
- Mid-term project roadmap
- Key quotes from the call

## Report Template

Generated reports include:

- Executive summary with business profile
- AI Readiness Score (1-10 across 5 categories)
- Identified pain points with severity
- Key insights/quotes from call
- Current tech stack analysis
- Quick wins (0-30 day implementations)
- Mid-term projects (30-90 days)
- Projected ROI ($15K-$30K+ annually)

## Testing

Run with test transcript:

```bash
python report_generator.py
```

Test webhook endpoint:

```bash
curl -X POST http://localhost:8000/webhook/retell \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Claude API key | Yes |
| `CLAUDE_MODEL` | Model to use (default: claude-3-7-sonnet) | No |
| `RETELL_WEBHOOK_SECRET` | Webhook verification secret | No |
| `REPORTS_DIR` | Where to save reports | No |
| `PORT` | Server port | No |

## Directory Structure

```
pipeline/
├── webhook_server.py        # FastAPI webhook receiver
├── report_generator.py      # Claude analysis + HTML generation
├── .env.example             # Configuration template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Next Steps

- [ ] Add email notifications (Himalaya or SMTP)
- [ ] Add PDF generation from HTML
- [ ] Add report URL delivery to client
- [ ] Add error handling with retry logic
- [ ] Add webhook signature verification

## Support

Questions? `apply@mindvaultstudio.net`
