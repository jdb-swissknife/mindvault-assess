# AI Assessment Discovery Call Script
## Voice Agent Conversation Flow (15-20 minutes)

### The Goal
Gather enough information to build a complete AI Assessment report with:
- Impact-Effort Matrix
- ROI calculator  
- Quick win recommendations
- Integration roadmap

This is NOT a sales call. It's a diagnostic. The report does the selling.

---

## OPENING (1-2 minutes)

**[When they answer]**

"Hi [name], this is [your AI assistant name] from MindVault Studio. Thanks for booking the AI Assessment. This call is designed to help us understand your business operations so we can build your personalized AI roadmap. Do you have about 15-20 minutes to walk through some questions?"

**[If yes]**

"Great. First, I wanted to let you know this call will be recorded so we can capture everything accurately for your assessment report. Does that work for you?"

**[Confirm]**

"Perfect. This will be straightforward—I'll ask about your business operations, where your time goes, and what systems you're using. Then our team will build your custom assessment. We'll present it within 5 business days and send you the written report. Ready to get started?"

---

## SECTION 1: BUSINESS OVERVIEW (2-3 minutes)

**Q1: Business identity**
"Tell me about your business—what do you do, who do you serve, and how long have you been operating?"

*Listen for: Industry, years in business, customer type, business model (service/retail/etc.)*

**Q2: Team size and structure**
"How many people are on your team? Do you have employees, contractors, or is it just you?"

*Listen for: Team size, roles, administration burden on owner*

**Q3: Current revenue/sales**
"Without getting too specific—would you say you're doing under $500K, $500K to $1M, or over $1M in annual revenue?"

*Listen for: Growth stage, budget reality*

---

## SECTION 2: OWNER'S TIME & PAIN POINTS (4-5 minutes)

**Q4: Owner's daily routine**
"Walk me through a typical morning for you. What time do you start, and what are you doing in those first few hours?"

*Listen for: Administrative work, firefighting, low-value tasks, lack of focus time*

**Q5: Administrative burden**
"Roughly how many hours per week would you say you spend on admin work—emails, scheduling, data entry, paperwork—that's not revenue-generating?"

*Calculate: Hours × owner's hourly rate = immediate dollar value*

**Q6: The 'if only' question**
"If you could magically reclaim 10 hours per week, what would you actually do with that time?"

*Listen for: Revenue activities, family time, business development, strategic work*

**Q7: Biggest frustration**
"What's the most frustrating part of your current setup? The thing that bugs you on a daily or weekly basis?"

*Listen for: Repeated pain points, bottlenecks, manual work*

---

## SECTION 3: LEAD & REVENUE LEAKS (3-4 minutes)

**Q8: Lead response time**
"When someone fills out a form on your website or calls your business—how quickly does someone respond?"

*Listen for: Delay, manual process, missed opportunities*

**Q9: Follow-up consistency**
"How do you currently handle follow-ups with leads who don't respond the first time? Is it consistent?"

*Listen for: No system, owner-dependent, leads falling through cracks*

**Q10: Customer communication**
"How do you communicate with customers during a project or service? Is that manual, automated, or a mix?"

*Listen for: Text/email done manually, status updates, customer service burden*

**Q11: Reviews and referrals**
"How do you currently ask for reviews or referrals after you complete a job?"

*Listen for: Ad-hoc process, not systematic, missed opportunity*

---

## SECTION 4: SYSTEMS & TECH STACK AUDIT (3-4 minutes)

**Q12: Current tools**
"What tools are you currently using to run your business? I'm talking about your CRM, project management, email, scheduling—whatever you touch daily."

*Listen for: Tech stack inventory, gaps, outdated tools, no tools*

**Q13: Data and documentation**
"Do you have Standard Operating Procedures documented, or is most knowledge in your head or your team's heads?"

*Listen for: Documentation gaps, onboarding friction, key person risk*

**Q14: Automation status**
"Are you using any automation right now—like automatic email sequences, scheduling links, or anything that runs without you clicking buttons?"

*Listen for: Automation maturity, Zapier/Make/n8n usage, manual processes ripe for automation*

**Q15: Integration pain**
"Do your systems talk to each other, or are you copying data from one place to another by hand?"

*Listen for: Data silos, duplicate entry, integration opportunities*

---

## SECTION 5: GOALS & READINESS (2-3 minutes)

**Q16: Six-month goals**
"If we were sitting here six months from now and your business had transformed in one major way, what would that look like?"

*Listen for: Revenue targets, time goals, growth objectives*

**Q17: Implementation preference**
"When the assessment comes back with recommendations, are you someone who would want to implement things yourself, or would you prefer to have us handle setup?"

*Listen for: DIY vs full-service upsell opportunity*

**Q18: Timeline urgency**
"Is there any pressure driving this right now—a busy season coming up, or a specific pain point that's getting worse?"

*Listen for: Urgency, seasonality, burning platform*

---

## CLOSING (1 minute)

"Perfect, I have everything I need. Just to confirm:
- You'll receive your AI Assessment report via email within 5 business days
- We'll schedule a 15-20 minute video call to walk through the findings
- The report will include your personalized Impact-Effort Matrix, ROI calculations, and a clear roadmap

Do you have any questions before we wrap up?"

**[Address any questions]**

"Great. One more thing—can you confirm the best email to send the report to?"

**[Confirm email]**

"Perfect. Thank you for your time, [name]. We look forward to showing you what's possible. Have a great day."

---

## DATA CAPTURE FOR ASSESSMENT REPORT

After the call, the voice agent transcript is fed to Claude/GPT with this prompt structure:

```
Extract the following for an AI Assessment report:

BUSINESS PROFILE:
- Industry/vertical
- Years in business  
- Team size
- Revenue range
- Business model

TIME ANALYSIS:
- Hours per week on admin
- Owner's effective hourly rate (estimated)
- Annual cost of admin time [hours × rate × 50 weeks]
- High-value activities owner could reclaim time for

PAIN POINTS SCORE (1-5 each):
- Lead response speed
- Follow-up consistency
- Customer communication
- Review/referral requests
- Documentation/SOPs
- Data integration

TECH STACK INVENTORY:
- CRM: [name, maturity, gaps]
- Communication: [tools, gaps]
- Scheduling: [status]
- Project management: [status]
- Automation: [none/partial/advanced]

QUICK WIN OPPORTUNITIES:
List 3-5 low-effort, high-impact AI tools based on identified pain points.

MID-TERM PROJECTS:
List 2-3 integration/automation projects with complexity ratings.

ROI PROJECTION:
Calculate potential hours saved and dollar value for quick wins and mid-term projects.

IMPACT-EFFORT MATRIX:
Categorize all identified opportunities by effort (Low/Medium/High) and impact (Low/Medium/High).
```

---

## VOICE AGENT CONFIGURATION NOTES

If building this in Retell.ai, Vapi, or Synthflow:

1. **Use natural pauses** - Let the prospect think between sections
2. **Capture interruption gracefully** - If they go on tangents about pain points, that's gold—let them talk
3. **Don't read verbatim** - The agent should feel conversational but cover all sections
4. **Confirm contact info at end** - Critical for report delivery
5. **Set expectations clearly** - 5 business days, 30-min presentation call
6. **Optional: Real-time validation** - Confirm they understand this is a paid assessment, not free

---

## DIFFERENCES FROM STANDARD SALES DISCOVERY CALL

| Standard Sales Call | AI Assessment Call |
|---------------------|-------------------|
| Goal: Close $5K-$20K service | Goal: Gather data for $997 report |
| 30-45 minutes | 15-20 minutes |
| Qualify budget/decision maker | Assume qualified (they paid) |
| Agitate pain to create urgency | Document pain for report |
| Book next call live | 5-day turnaround, then present |
| Range pricing on call | Fixed $997 price (already paid) |
| Need case studies/credibility | Assessment report IS credibility |

