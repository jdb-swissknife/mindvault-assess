# AI Assessment Agent - Industry Router
## Master Script with Branching Logic

---

## INDUSTRY DETECTION QUESTION (Q1)

**Q1: Business identification (ask before branching)**

"Before we dive in, tell me about your business—what industry are you in, and what do you specialize in?"

**Intent Classification:**

Listen for keywords and classify into:

| Keywords Detected | Industry Branch |
|-------------------|-----------------|
| agent, realtor, broker, property, listing, showing, mortgage, real estate | real-estate.md |
| roofing, roof, HVAC, AC, plumbing, electrical, contractor, solar, windows, concrete, flooring | home-services.md |
| insurance, Medicare, P&C, agent, carrier, quote, policy, coverage | insurance-financial.md |
| accounting, CPA, bookkeeper, tax | accounting.md (future) |
| lawyer, attorney, legal, firm | legal.md (future) |
| medical, dental, chiropractor, practice | healthcare.md (future) |
| restaurant, food service, catering | restaurant.md (future) |
| none of the above / unclear | Use generic script with follow-up clarification |

**Clarification follow-up (if unclear):**
"Got it. To make sure I ask the right questions—would you say you're primarily in:
- Real estate or property services
- Home services like roofing, HVAC, or contracting
- Insurance or financial services
- Something else?"

---

## INDUSTRY BRANCHING LOGIC

After industry identification, route to appropriate script module:

```
GENERIC
├─ Opening (all industries)
├─ SECTION 1: Business Overview
│  ├─ Q1a (industry detection) ┬─> real-estate.md
│  │                           ├─> home-services.md
│  │                           ├─> insurance-financial.md
│  │                           └─> accounting.md [future]
│  ├─ Q1b (industry-specific)  │
│  ├─ Q2 (team structure)      │
│  └─ Q3 (revenue/volume)      │
├─ SECTION 2: Owner's Time & Pain Points (shared)
│  ├─ Q4 (daily routine)
│  ├─ Q5 (admin burden)
│  ├─ Q6 (if only question)
│  └─ Q7 (biggest frustration)
├─ SECTION 3: Lead & Revenue Leaks
│  ├─ Q8 (industry-specific) ──┬─> real-estate.md Q8-Q12
│  ├─ Q9 (industry-specific)   ├─> home-services.md Q8-Q13
│  ├─ Q10 (industry-specific)  └─> insurance-financial.md Q8-Q13
│  ├─ Q11 (industry-specific)
│  ├─ Q12 (industry-specific - optional)
│  └─ Q13 (industry-specific - optional)
├─ SECTION 4: Systems & Tech Stack (shared)
│  ├─ Q14 (current tools)
│  ├─ Q15 (documentation)
│  ├─ Q16 (automation status)
│  └─ Q17 (integration pain)
├─ SECTION 5: Goals & Readiness (shared)
│  ├─ Q18 (6-month goals)
│  ├─ Q19 (implementation preference)
│  └─ Q20 (timeline urgency)
└─ CLOSING (all industries)
```

---

## KNOWLEDGE BASE INJECTION

Once industry is detected, load the corresponding knowledge base:

### For Real Estate Branch:
- **Industry-specific pains:** Speed-to-lead, database decay, showing coordination
- **Quick Wins:** Speed-to-lead AI, Smart Scheduler, Reactivation, Listing GEN
- **Mid-term Projects:** Transaction automation, AI chatbot, Market reports
- **KPIs:** Lead decay cost, database value, per-listing time cost
- **Tool library:** CRMs (Follow Up Boss, kvCORE), AI agents (Synthflow, Vapi), Specialty (ListingAI)

### For Home Services Branch:
- **Industry-specific pains:** Missed emergency calls, estimate follow-up, dispatch efficiency
- **Quick Wins:** Missed call text-back, quote follow-up automations, smart scheduling
- **Mid-term Projects:** End-to-end job management, maintenance memberships, damage assessment AI
- **KPIs:** Missed call cost, estimate leakage, dispatch efficiency
- **Tool library:** GoHighLevel, ServiceTitan, Jobber, Housecall Pro, CompanyCam

### For Insurance Branch:
- **Industry-specific pains:** Quote speed, reactive renewals, cross-sell gaps
- **Quick Wins:** Instant quote response, renewal automation, referral campaigns
- **Mid-term Projects:** AMS integration, cross-sell engine, client portal
- **KPIs:** Quote-to-bind rate, retention rate, policies per client
- **Tool library:** Better Agency, AgencyZoom, HawkSoft, Quoteburst

---

## DYNAMIC RECOMMENDATION ENGINE

Based on collected data, the AI should flag for the assessor report:

### Severity Indicators (Red Flags)
- Response time > 2 hours to new leads
- No CRM (spreadsheets or paper only)
- Owner spending > 15 hours/week on admin
- Zero automation currently
- No follow-up system for quotes/estimates
- 100% reactive (no proactive outreach)

### Quick Win Triggers
- Uses Gmail/Outlook without scheduling links → Recommend Calendly
- Takes notes during meetings but no transcriptions → Recommend Fathom
- Manual data entry between systems → Recommend Zapier/Make
- Inbound voicemails after hours → Recommend AI voice agent
- Scattered photos on crew phones → Recommend CompanyCam
- No review system in place → Recommend Review automation

### Mid-Term Project Triggers
- Multiple tools with no integration → Full system integration project
- Growing team with no documentation → Knowledge base + SOP project
- Seasonal volume spikes → Capacity/capability automation project
- High-value but repetitive processes → Custom AI agent project

---

## CONVERSATION RECOVERY

If the user goes off-script (which is good - means they're engaged):

**Validation Pattern:**
"That's really helpful context. To make sure I capture that for your report—would you say that [summarize their point] is one of your biggest pain points right now?"

**Redirect to Structure:**
"Great insight. I'm going to make sure that's front and center in your assessment. Let me also ask you about [next question topic]..."

**Capture Additional Context:**
When they volunteer information unprompted, the AI should note it for the data extraction prompt:
- Add to "Additional Context" section
- Flag as high-priority quote for report
- Include verbatim in pain points summary

---

## TRANSCRIPT DATA EXTRACTION PROMPT

After the call, process the transcript with industry context:

```
You are analyzing a discovery call transcript for an AI Assessment report.

BUSINESS INDUSTRY: [Detected Industry]

Extract the following:

1. BUSINESS PROFILE
   - Industry sub-vertical (specific type)
   - Years in business
   - Team size and structure
   - Revenue range or volume metrics

2. OPERATIONAL PAIN POINTS (Prioritized by severity from call)
   - Pain 1: [Description] - Severity: [High/Med/Low]
   - Pain 2: [Description] - Severity: [High/Med/Low]
   - Pain 3: [Description] - Severity: [High/Med/Low]

3. CURRENT TECH STACK
   - CRM: [Name/None]
   - Communication: [Tools]
   - Scheduling: [Tool/None]
   - Project management: [Tool/None]
   - Automation platform: [Zapier/Make/None]

4. TIME ANALYSIS
   - Admin hours/week: [Number]
   - Owner hourly value: [Estimated or stated]
   - Biggest time wasters: [List]

5. REVENUE LEAKS IDENTIFIED
   - Lead response time: [Time]
   - Follow-up system: [Y/N]
   - Quote/estimate close rate: [% if mentioned]
   - Referral system: [Y/N]

6. QUICK WIN CANDIDATES (Recommend 3-5 from industry tool library)
   Based on [Industry] context, recommend:
   - Win 1: [Tool] - Addresses [Pain Point] - ROI: [Calculated]
   - Win 2: [Tool] - Addresses [Pain Point] - ROI: [Calculated]
   - Win 3: [Tool] - Addresses [Pain Point] - ROI: [Calculated]

7. MID-TERM PROJECTS (Recommend 2-3)
   - Project 1: [Name] - Scope - Investment - Timeline
   - Project 2: [Name] - Scope - Investment - Timeline

8. IMPACT-EFFORT MATRIX
   Categorize all recommendations

9. KEY QUOTES FOR REPORT
   Pull 2-3 verbatim quotes that capture their pain and goals

10. IMPLEMENTATION READINESS
    - DIY vs Guided vs Full Service recommendation with rationale
```

---

## TECHNICAL IMPLEMENTATION NOTES

### For Retell.ai:
- Use function calling to detect industry classification
- Store detected industry in call context
- Load industry-specific prompt dynamically
- Use conditional logic for branch-dependent questions

### For Vapi:
- Pre-screener question before connecting to main agent
- Industry stored as variable, referenced throughout
- Different tools/endpoints for each industry knowledge base

### For Synthflow:
- Intent classification as first node in flow
- Branch to industry-specific conversation flows
- Merge back to common closing section

---

## FUTURE INDUSTRY EXPANSION

Priority order for additional industry scripts:

1. **Accounting/CPA Firms** - High RDI potential, clear pain points (tax season rush, client docs, year-end planning)
2. **Legal/Law Firms** - Document-heavy, time tracking essential, high hourly rates
3. **Healthcare/Dental** - Appointment optimization, patient comms, recall systems
4. **E-commerce/DTC** - Inventory, customer service, ad management automation

Each new industry requires:
- Modified Section 1 questions (business model specifics)
- Modified Section 3 questions (industry-specific leaks)
- Industry-specific Quick Wins list
- Industry-specific Mid-Term Projects
- KPI library
- Tool recommendations
