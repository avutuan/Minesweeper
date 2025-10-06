# Project Time Log and Estimates for Maintenance

Document for time log entires and estimatants for Maintenance phase of Minesweeper project. 

---

# Clock Log (Team session entries) 

## 2025-09-26
Aiden: 10:30 - 2:30
Alejandro: 10:30 - 2:30
Jorge: 10:30 - 1:30
Liam: 10:30 - 1:30
Pashia: 10:30 - 1:30
Reem: 10:30 - 12:00


## 2025-10-03
Aiden: 10:30 - 1:00
Alejandro: 10:30 - 1:00
Jorge: 10:30 - 1:00
Liam: 10:30 - 2:00
Pashia: 10:30 - 2:00
Reem: 10:30 - 12:00

## 2025-10-10
Aiden: 10:30 - 2:00
Alejandro: 10:30 - 2:00
Jorge: 10:30 - 1:00
Liam: 10:30 - 1:00
Pashia: 10:30 - 2:00
Reem: 10:30 - 12:00


---

## Project Overview
This section tracks the estimated vs actual time spent on implementing features for phase 2 of the Minesweeper game project. All times are in hours.


## Core Maintenance & Stabilization

### 1. Environment & Build Setup (inherited repo)
**Description**: Fork, branch, run locally; verify asset/module paths  
- **Estimated Time**: 3.0 hours  
- **Actual Time Spent**: 3.0 hours  
- **Variance**: 0.0 hours (0% on estimate)  
- **Notes**: Setup matched expectations

### 2. P1 Feature Audit & Bug Fixes
**Description**: Ensure grid init, reveal/flag, flood-fill, win/lose per P1 spec; fix regressions  
- **Estimated Time**: 6.0 hours  
- **Actual Time Spent**: 9.0 hours  
- **Variance**: +3.0 hours (50% over estimate)  
- **Notes**: Inherited-code quirks increased debugging time

---

## AI Solver

### 3. AI Easy (Random hidden click, avoids revealed/flagged)
**Description**: Randomly uncover a covered, unflagged cell  
- **Estimated Time**: 2.0 hours  
- **Actual Time Spent**: 2.0 hours  
- **Variance**: 0.0 hours (0% on estimate)  
- **Notes**: Straightforward implementation

### 4. AI Medium (Two rules + random fallback)
**Description**: Flag-all when hidden == number; open-others when flagged == number; else random  
- **Estimated Time**: 5.0 hours  
- **Actual Time Spent**: 7.0 hours  
- **Variance**: +2.0 hours (40% over estimate)  
- **Notes**: Edge cases around neighbor counts

### 5. AI Hard (Add 1-2-1 pattern + medium rules)
**Description**: Detect horizontal/vertical 1-2-1; flag outers, open inner; fallback to medium/random  
- **Estimated Time**: 5.0 hours  
- **Actual Time Spent**: 8.0 hours  
- **Variance**: +3.0 hours (60% over estimate)  
- **Notes**: Pattern detection & indexing fixes

### 6. AI Integration Modes (interactive / auto-solve)
**Description**: Toggle human/AI turns; UI controls; status updates  
- **Estimated Time**: 3.0 hours  
- **Actual Time Spent**: 4.0 hours  
- **Variance**: +1.0 hour (33% over estimate)  
- **Notes**: Extra UI wiring and state sync

---

## Custom Addition

### 7. Audio & SFX
**Description**: Music added; In game sound effects added
- **Estimated Time**: 3.0 hours  
- **Actual Time Spent**: 3.0 hours  
- **Variance**: 0.0 hours (0% on estimate)  
- **Notes**: Uses user-gesture to satisfy autoplay rules

### 8. Color Themes
**Description**: Added color themes to game  
- **Estimated Time**: 2.0 hours  
- **Actual Time Spent**: 2.5 hours  
- **Variance**: +0.5 hours (25% over estimate)  
- **Notes**: Extra polish on contrast/readability for numbered cells

### 9. Video Overlay (pywebview)
**Description**: Optional embedded window during gameplay via pywebview; menu to choose “1) YouTube Shorts” or “2) The Web”  
- **Estimated Time**: 4.0 hours  
- **Actual Time Spent**: 3.5 hours  
- **Variance**: -0.5 hours (12.5% under estimate)  
- **Notes**: Added basic controls; ensured game input focus remains responsive

---

---

## Summary Statistics






