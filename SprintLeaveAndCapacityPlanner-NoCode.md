# 🧠 Simple Scrum Master Agent

## 🎯 Purpose
Analyze sprint data to identify:
- Leave conflicts
- Work overload
- Dependency risks

---

## 🧾 Sample Data

### 🗓️ Leave Schedule
- John → 25-May  
- Sarah → 25-May  
- Mike → 26-May  

---

### 📊 Sprint Capacity
- John → Available: 40 hrs | Allocated: 35 hrs  
- Sarah → Available: 40 hrs | Allocated: 45 hrs  
- Mike → Available: 40 hrs | Allocated: 30 hrs  

---

### 🔗 Task Dependencies
- API Development → Owner: John | Backup: None  
- Testing → Owner: Sarah | Backup: Mike  

---

## 🔍 Agent Analysis

### ✅ Leave Conflicts
- John and Sarah are on leave on the same day → High Risk  

---

### ✅ Capacity Issues
- Sarah is overloaded (45 > 40 hrs)  

---

### ✅ Dependency Risks
- API Development has no backup → High Risk  

---

## 💡 Recommendations
- Avoid overlapping leave for critical team members  
- Assign backup for API Development  
- Balance workload across team  

---

## ✅ Conclusion
The sprint has:
- Leave conflict  
- One overloaded resource  
- One critical dependency risk  

Action is required to improve planning.