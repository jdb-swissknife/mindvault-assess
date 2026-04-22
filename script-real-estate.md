# Real Estate AI Assessment Script
## Industry-Specific Fork (Post-Identification)

Trigger: When prospect identifies as real estate agent, broker, property manager, or related

---

## MODIFIED SECTION 1: REAL ESTATE BUSINESS OVERVIEW

**Q1 (Replace): Business identity**
"Tell me about your real estate business—are you primarily working with buyers, sellers, investors, or renters? And are you solo or part of a team or brokerage?"

*Listen for: Agent vs broker vs property manager, niche (luxury/commercial/residential), team size*

**Q2 (Keep): Team size and structure**
"How many people are on your team? Do you have showing assistants, transaction coordinators, or is it just you?"

*Listen for: TCs, ISAs, showing agents, admin burden on lead agent*

**Q3 (Replace): Volume and pipeline**
"How many active transactions or listings are you typically juggling at once? And how many leads are you getting per month?"

*Listen for: Capacity strain, lead volume vs conversion rate*

---

## MODIFIED SECTION 3: REAL ESTATE LEAD & REVENUE LEAKS

**Q8 (Replace): Speed-to-lead and lead response**
"When a new lead comes in from Zillow, your website, or a referral—how quickly are you able to respond? And is it you or someone on your team?"

*Listen for: 5-minute rule violations, evening/weekend gaps, agent doing all follow-up*

**Q9 (Replace): Lead nurture and long-term follow-up**
"What happens to leads who aren't ready to buy or sell immediately—say, 6-12 months out? How do you stay in touch with them?"

*Listen for: Database decay, lack of nurture sequences, missed future commissions*

**Q10 (Replace): Showing coordination**
"How do you currently schedule and confirm property showings? How much back-and-forth is involved?"

*Listen for: Scheduling friction, no-shows, time wasted on logistics*

**Q11 (Replace): Transaction and listing management**
"Walk me through what happens once you get a listing or go under contract—how do you manage all the deadlines, inspections, and paperwork?"

*Listen for: Transaction coordinator reliance, missed deadlines, manual checklist management*

**Q12 (Add): Client communication during deals**
"How often are your clients asking for updates, and how are you delivering those? Are they calling you, or do you have an automated system?"

*Listen for: Reactive communication, status update burden, client anxiety*

---

## REAL ESTATE-SPECIFIC QUICK WINS (For Report)

### Quick Win 1: Speed-to-Lead AI Agent
**Problem:** Missing leads that come in after hours or when you're with clients
**Solution:** AI voice agent that responds to new inquiries in <2 minutes, 24/7
**Tools:** Synthflow, Vapi, or Bland.ai integrated with CRM
**ROI:** Response time under 5 min = 391% more likely to connect; 21x more likely to qualify
**Setup:** $500-$1,500 initial, $50-150/month

### Quick Win 2: Smart Showing Scheduler
**Problem:** Back-and-forth scheduling, no-shows, wasted time
**Solution:** Automated scheduling with qualification pre-call, reminders, lockbox codes
**Tools:** ShowingTime, Calendly + Zapier, or custom automation
**ROI:** 3-5 hours/week saved, reduced no-shows by 30-50%
**Setup:** $200-$500 initial

### Quick Win 3: Database Reactivation Campaign
**Problem:** Past clients and cold leads forgotten in CRM
**Solution:** AI-personalized nurture sequences via email/SMS with market updates
**Tools:** Lifespace AI, Hailom, or GoHighLevel campaigns
**ROI:** 10-20% of old database re-engages; $10K-$50K in recovered commissions
**Setup:** $1,000-$2,000 initial

### Quick Win 4: Listing Description Generator
**Problem:** Spending 30-60 min writing each listing description
**Solution:** AI generates first draft from property photos and basic details
**Tools:** ChatGPT + custom prompt, or Listing.ai
**ROI:** 1 hour saved per listing; 10 listings/month = 10 hours reclaimed
**Setup:** $100-$300 initial template build

---

## REAL ESTATE MID-TERM PROJECTS

### Project 1: Transaction Management Automation
**Scope:** Automated contract-to-close checklist, deadline tracking, stakeholder updates
**Tools:** Dotloop or DocuSign + automation layer
**Timeline:** 3-4 weeks
**Investment:** $3,000-$6,000
**ROI:** 5-8 hours/week saved, zero missed deadlines

### Project 2: Buyer/Seller Journey AI Assistant
**Scope:** 24/7 AI chatbot for your website answering FAQs, pre-qualifying leads, booking consultations
**Tools:** Custom GPT, Intercom, or ManyChat
**Timeline:** 4-6 weeks
**Investment:** $4,000-$8,000
**ROI:** Captures 20-30% more leads, filters tire-kickers

### Project 3: Market Report Automation
**Scope:** Personalized market updates for farm area, auto-delivered monthly
**Tools:** Gamma, SmartCharts, or custom build
**Timeline:** 2-3 weeks
**Investment:** $2,000-$4,000
**ROI:** Positions you as market expert, generates listing conversations

---

## REAL ESTATE INDUSTRY KPIs TO CALCULATE

In the assessment report, calculate:

1. **Lead Decay Cost**
   - Current response time (hours)
   - % of leads lost per hour of delay
   - Potential deals lost monthly
   - Dollar value of missed commissions

2. **Database Value**
   - Number of contacts in CRM
   - Estimated conversion rate if reactivated
   - Potential commission value

3. **Per-Listing Time Cost**
   - Hours spent on listing per month
   - Owner's effective hourly rate
   - Cost of manual listing tasks

4. **Showing Efficiency**
   - Showings per week
   - Time per showing (coordination + drive + showing)
   - No-show rate
   - Time cost of inefficient scheduling

---

## REAL ESTATE QUESTION FLOW FOR AI AGENT

After identifying as real estate, branch to this script:

1. Keep: Q4 (owner routine), Q5 (admin hours), Q6 (if only), Q7 (frustration)
2. Use modified Section 3 questions above (Q8-Q11 + new Q12)
3. Keep: Q13 (documentation), Q14 (automation), Q15 (integration)
4. Use modified Section 5 questions

Return to generic closing at Q16.
