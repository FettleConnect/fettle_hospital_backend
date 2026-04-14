**1️⃣ 🔹 KEY OUTCOMES** 

| KPI | Value (Example) | Calculation Logic |
| ----- | ----- | ----- |
| Total Patient Interactions Handled | 5,240 | Total inbound calls \+ outbound calls \+ chatbot interactions |
| Avg Call Resolution Time (seconds) | 95 sec | (Total duration of all completed calls) ÷ (Total calls handled) |
| Appointment Conversion Rate (%) | 42% | (Appointments booked ÷ Total appointment inquiry calls) × 100 |
| No-Show Rate (%) | 11% | (Patients who did not attend ÷ Total booked appointments) × 100 |
| Patient Satisfaction (CSAT) | 4.7 / 5 | (Sum of ratings ÷ Total responses) |
| Automated Follow-ups Completed | 3,120 | Count of successfully completed automated follow-up calls/messages |

---

# **2️⃣ 📊 MEASURABLE GAINS** 

|  | KPI | Value (Example) | Calculation Logic |
| ----- | ----- | ----- | ----- |
|  | Avg Response Time (seconds) | 22 sec | (Total wait time of all answered calls) ÷ (Total calls answered) |
|  | First Response SLA Compliance (%) | 94% | (Calls answered within 30 sec ÷ Total calls) × 100 |
|  | Call Handling Coverage (%) | 96% | (Total calls handled ÷ Total incoming calls) × 100 |
|  | 24/7 Availability Uptime (%) | 99.9% | (Total uptime minutes ÷ Total minutes in month) × 100 |

# 

# 

# **3️⃣ 💰 FINANCIAL & REVENUE INTELLIGENCE** 

---

## **A. Revenue Generated via Fettle Connect**

| KPI | Value (Example) | Calculation Logic |
| ----- | ----- | ----- |
| Appointments Booked via AI | 2,180 | Count of bookings created through AI system |
| Avg Revenue per Appointment (₹) | ₹850 | (Total revenue from completed appointments ÷ Total completed appointments) |
| **Total Revenue Influenced (₹)** | ₹18.5 Lakhs | (Appointments booked via AI × Avg revenue per appointment) |

---

## **B. Revenue Leakage Prevented**

| KPI | Value (Example) | Calculation Logic |
| ----- | ----- | ----- |
| No-Show Reduction Revenue Recovered (₹) | ₹2.1 Lakhs | (Reduction in no-show % × Total booked appointments × Avg revenue per appointment) |
| Missed Call Capture (Patients) | 1,200 | (Total incoming calls − missed calls) |
| Revenue from Missed Call Capture (₹) | ₹5.4 Lakhs | (Additional patients handled × Conversion rate × Avg revenue per appointment) |
| Follow-up Driven Revisit Revenue (₹) | ₹3.2 Lakhs | (Revisit patients from follow-ups × Avg revenue per revisit) |

---

## **C. Operational Cost Efficiency**

| KPI | Value (Example) | Calculation Logic |
| ----- | ----- | ----- |
| Staff Hours Saved (hrs/month) | 210 hrs | (Total AI handled call duration in minutes ÷ 60\) |
| Equivalent FTE Freed | 2.1 FTE | (Staff hours saved ÷ 100 hrs per staff per month) |
| Cost per Staff per Month (₹) | ₹40,000 | HR payroll average |
| **Cost Efficiency Value (₹)** | ₹84,000 | (FTE freed × Cost per staff per month) |

---

## **D. Revenue Efficiency Metrics**

| KPI | Value (Example) | Calculation Logic |
| ----- | ----- | ----- |
| Revenue per Call Handled (₹) | ₹350 | (Total revenue influenced ÷ Total calls handled) |
| Revenue per Follow-up (₹) | ₹220 | (Revenue from revisit patients ÷ Total follow-ups completed) |
| Conversion per 100 Calls | 42 bookings | (Appointments booked ÷ Total calls) × 100 |

---

# **4️⃣ 🏥 DEPARTMENT-WISE PERFORMANCE BREAKDOWN**

| KPI | Calculation Logic |
| ----- | ----- |
| Interactions Handled (per department) | Count of calls tagged to that department |
| Appointments Booked | Count of bookings tagged to department |
| Conversion Rate (%) | (Appointments booked ÷ Department inquiry calls) × 100 |
| Revenue Generated (₹) | (Appointments booked × Avg revenue per appointment in that department) |
| CSAT | (Sum of ratings for department ÷ Total responses for department) |

---

### **Example Table**

| Department | Interactions | Bookings | Conversion % | Revenue (₹) | CSAT |
| ----- | ----- | ----- | ----- | ----- | ----- |
| General Medicine | 1,820 | 720 | 39% | ₹6.1L | 4.6 |
| Cardiology | 920 | 310 | 33% | ₹4.4L | 4.8 |
| Pediatrics | 760 | 280 | 37% | ₹2.3L | 4.7 |

---

# **5️⃣ 📈 SYSTEM PERFORMANCE HEALTH** 

| KPI | Value (Example) | Calculation Logic |
| ----- | ----- | ----- |
| AI Call Handling Accuracy (%) | 96% | (Correctly handled calls ÷ Total AI handled calls) × 100 |
| Escalation Rate to Human (%) | 4% | (Calls transferred to human ÷ Total calls handled) × 100 |
| Emergency Detection Success (%) | 100% | (Emergency cases correctly detected ÷ Total emergency cases) × 100 |
| System Uptime (%) | 99.9% | (Total uptime minutes ÷ Total minutes in period) × 100 |
| Multilingual Usage Split (%) | Eng 42 / Hin 37 / Tel 21 | (Calls per language ÷ Total calls) × 100 |

---

# **7️⃣ 🧾 TOP PATIENT INTENTS** 

| KPI | Calculation Logic |
| ----- | ----- |
| Appointment Booking % | (Booking related calls ÷ Total calls) × 100 |
| Lab Report Queries % | (Lab report calls ÷ Total calls) × 100 |
| Follow-up / Revisit % | (Follow-up calls ÷ Total calls) × 100 |
| Prescription Queries % | (Prescription calls ÷ Total calls) × 100 |
| Emergency Routing % | (Emergency calls ÷ Total calls) × 100 |

---

# **8️⃣ 📌 KEY HIGHLIGHTS OF THE MONTH** 

| Highlight | Selection Logic |
| ----- | ----- |
| Highest Performing Department | Department with highest revenue generated |
| Best CSAT Department | Department with highest CSAT score |
| Peak Call Volume Day | Date with maximum calls handled |
| Most Used Language | Language with highest % usage  |

1. Ensure the call logging/running the agent logic (by pressing call or whatever is in sync with the inbound/outbound agent- hospital/clinic etc. must be able to run their own agent.  
2. “Call details only include timestamp; no conversation or outcome recorded” This and other remarks should be populated based on the outbound/inbound webhook endpoints at /api/webhooks/vobiz/inbound and /api/webhooks/vobiz/outbound.  
3. In call logging, we are currently showing connected, not connected, and queued. Show status “In progress” based on the api fields or endpoints available from the vobiz or voice agent as well.