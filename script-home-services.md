# Home Services / Roofing / HVAC / Trades AI Assessment Script
## Industry-Specific Fork (Post-Identification)

Trigger: When prospect identifies as roofing, HVAC, plumbing, electrical, solar, or home services contractor

---

## MODIFIED SECTION 1: TRADES BUSINESS OVERVIEW

**Q1 (Replace): Business identity**
"Tell me about your company—are you focused on residential, commercial, or both? And are you primarily doing repairs, replacements, new installs, or all of the above?"

*Listen for: Service mix (repair vs replacement), residential vs commercial, specialization*

**Q2 (Replace): Team and field operations**
"How many crew members do you have in the field? And do you have office staff, or are you handling scheduling and dispatch yourself?"

*Listen for: Field crew count, office/admin support ratio, owner doing dispatch*

**Q3 (Replace): Lead volume and seasonality**
"How many estimates or service calls are you doing per week? And do you have busy seasons where volume spikes?"

*Listen for: Capacity planning, seasonal overflow, estimate-to-close ratio*

---

## MODIFIED SECTION 3: TRADES LEAD & REVENUE LEAKS

**Q8 (Replace): Emergency response and speed-to-lead**
"When someone calls with an emergency leak or AC out—how fast can you get someone there? And how does that call get to you or your crew?"

*Listen for: After-hours coverage, dispatch delays, missed emergency calls*

**Q9 (Replace): Estimate follow-up**
"After you give someone an estimate, what happens next? How do you follow up if they don't call back?"

*Listen for: No formal follow-up system, owner-dependent, lost estimates

**Q10 (Replace): Scheduling and dispatch**
"Walk me through how you schedule jobs and dispatch your crews. Are you doing it manually, or do you have a system?"

*Listen for: Whiteboard/paper systems, double-booking, inefficient routing, travel time waste*

**Q11 (Replace): Job site documentation**
"How do you handle photos, measurements, and documentation from job sites? Is that centralized or scattered across phones and texts?"

*Listen for: Photo management chaos, no central repository, lost documentation*

**Q12 (Add): Warranty and maintenance recalls**
"For completed jobs—do you have a system for warranty tracking or reaching out for maintenance?"

*Listen for: No follow-up revenue, missed maintenance contracts, warranty claims surprise*

**Q13 (Add): Reviews and referrals**
"How are you getting reviews right now? Is it 'remember to leave us a review' or do you have a system?"

*Listen for: Ad-hoc requests, low review count, missed referral opportunities*

---

## TRADES-SPECIFIC QUICK WINS

### Quick Win 1: Missed Call Text Back + AI Agent
**Problem:** Calls go to voicemail after hours, losing emergency jobs worth $5K-$20K+
**Solution:** Instant text reply with AI conversation to qualify and schedule
**Tools:** GoHighLevel, CallRail + AI layer, or Callin.io
**ROI:** Capture 30-50% of after-hours calls; each emergency job = $3K-$15K
**Setup:** $500-$1,500 initial, $100-200/month

### Quick Win 2: Automated Estimate Follow-Up
**Problem:** 60-80% of estimates never close; no follow-up system
**Solution:** 7-touch automated sequence via text/email after estimate
**Tools:** GoHighLevel, JobNimbus, or AccuLynx automations
**ROI:** 15-25% increase in close rate; $50K-$200K additional annual revenue
**Setup:** $800-$1,500 initial

### Quick Win 3: Smart Scheduling + Route Optimization
**Problem:** Manual dispatch, crews driving all over town, inefficient routes
**Solution:** Automated booking with route optimization, customer notifications
**Tools:** Housecall Pro, ServiceTitan, or Jobber + route logic
**ROI:** 10-15% more jobs per day; 2-3 hours/day saved on dispatch
**Setup:** $1,000-$2,500 initial

### Quick Win 4: Job Site Photo to CRM Auto-Flow
**Problem:** Photos stuck on crew phones, lost documentation, insurance headaches
**Solution:** Dedicated app or text-to-CRM system auto-organizing photos by job
**Tools:** CompanyCam, GoHighLevel forms, or custom automation
**ROI:** Zero lost photos, faster insurance claims, better customer updates
**Setup:** $500-$1,000 initial

---

## TRADES MID-TERM PROJECTS

### Project 1: End-to-End Job Management System
**Scope:** CRM + dispatch + invoicing + payment processing; integrate with accounting
**Tools:** GoHighLevel, ServiceTitan, Jobber, or AccuLynx
**Timeline:** 4-6 weeks
**Investment:** $5,000-$10,000
**ROI:** Streamlined operations, real-time job visibility, faster billing

### Project 2: Maintenance Membership Automation
**Scope:** Automated membership sales, scheduling, reminders, and recurring billing
**Tools:** GoHighLevel membership module or field service platform
**Timeline:** 3-4 weeks
**Investment:** $3,000-$6,000
**ROI:** Recurring revenue base; $50-$200/mo per member adds up fast

### Project 3: AI-Powered Damage Assessment
**Scope:** Photo upload → AI pre-assessment → instant estimate range → customer gets immediate response
**Tools:** Custom computer vision model + CRM integration
**Timeline:** 6-8 weeks
**Investment:** $8,000-$15,000
**ROI:** Instant engagement, filter out non-jobs, book more qualified appointments

---

## TRADES INDUSTRY KPIs TO CALCULATE

In the assessment report, calculate:

1. **Missed Call Cost**
   - Calls after hours/week
   - % that are actual opportunities
   - Average job value
   - Annual revenue lost to missed calls

2. **Estimate Leakage**
   - Estimates given per month
   - Current close rate
   - Industry benchmark (30-40% for trades)
   - Revenue lost to no follow-up

3. **Dispatch Efficiency**
   - Current jobs per crew per day
   - Average drive time between jobs
   - Potential jobs gained from better routing
   - Fuel and labor savings

4. **Review Velocity**
   - Current reviews per month
   - Impact on Google ranking and call volume
   - Cost of low review count in lost leads

5. **Seasonal Capacity**
   - Peak season call volume overflow
   - % of calls that go unanswered in busy times
   - Revenue lost to capacity constraints

---

## TRADES TOOL RECOMMENDATIONS LIBRARY

**CRM/Field Service Platforms (choose based on size/complexity):**

**GoHighLevel** - Best for: All-in-one, strong automation, good for 1-10 crew
- Pros: Unlimited users, powerful marketing automation, great for lead gen
- Cons: Learning curve, may need customization for complex dispatch

**ServiceTitan** - Best for: Larger operations, 20+ crew, detailed job costing
- Pros: Industry standard, robust reporting, integrates with accounting
- Cons: Expensive, complex setup

**Jobber** - Best for: Small-medium, easy onboarding
- Pros: Simple, good mobile app, reasonable price
- Cons: Limited automation, basic reporting

**Housecall Pro** - Best for: Dispatch-heavy operations
- Pros: Strong scheduling, route optimization
- Cons: Marketing features weaker than GHL

**AccuLynx** - Best for: Roofing-specific
- Pros: Built for roofing workflows, insurance supplement integration
- Cons: Roofing only, expensive for small operations

---

## TRADES QUESTION FLOW FOR AI AGENT

After identifying as home services/trades, branch to this script:

1. Use modified Section 1 questions (Q1-Q3)
2. Keep: Q4 (owner routine), Q5 (admin hours), Q6 (if only), Q7 (frustration)
3. Use modified Section 3 questions (Q8-Q13 - note extra Q12/Q13)
4. Keep: Q14 (documentation), Q15 (automation), Q16 (integration)
5. Use modified Section 5 questions

Return to generic closing at Q16.
