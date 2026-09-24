# AGENTS.md — Master Working Guidelines and Project Instructions

---

> **Project**: Autonomous Sternal Medical IoT Patch for Early Prediction of Sudden Cardiac Arrest (SCA) & Acute Myocardial Ischemia  
> **Target Event**: College Medical IoT Ideathon  
> **Workspace Path**: `c:\College\Ideathon`  
> **Git Remote**: `https://github.com/Headhunte-121/Ideathon-Research.git` (Branch: `main`)  
> **Last Updated**: 2026-09-24

---

## 1. Core Purpose and Architectural Mission

This repository contains the complete systems engineering blueprint, clinical research dossier, and executive summaries for an autonomous, chest-worn medical IoT patch. 

* **The Problem**: 70% to 80% of sudden non-traumatic cardiac arrests in adults stem from acute myocardial ischemia (coronary blood starvation). Smartwatches detect events only after electrical collapse (Hour 0), while hospitals are reactive facilities where patients arrive 2 to 4 hours post-onset (after irreversible tissue death).
* **The Solution**: Continuous sternal multi-sensor monitoring (ECG biopotentials, SCG mechanical vibrations, optical PPG/SpO2, acoustic PCG/trachea, and thoracic bio-impedance) that intercepts the ordered **1-to-6-hour pre-infarction countdown** before irreversible cellular necrosis or terminal arrhythmias occur.

---

## 2. Directory Structure and Organization Rules

Every AI agent working in this repository must maintain the following directory layout:

```
c:/College/Ideathon/
├── MASTER_PRODUCT_AND_RESEARCH_HUB.md           <-- 🌟 MASTER SOURCE OF TRUTH: All Product Info & Reference Links
├── README.md                                    <-- Master Repository Overview & 3-Tier Navigation
├── AGENTS.md                                    <-- Persistent Agent Guidelines (This Document)
├── Master_Research_Questionnaire_Expanded.md    <-- 12-Phase Systems Engineering Roadmap
├── Sensor_Evaluation_Deep_Dive_Framework.md     <-- Hardware Component Scorecard
│
├── Ideathon_Poster_and_Pitch/                   <-- 🎯 LIVE COMPETITION DELIVERABLES
│   ├── A0_Poster_Modular_Canvas.md              <-- A0 Canvas: Blank Blocks with Suggested Candidate Points
│   └── Master_Pitch_and_Poster_Guide.md         <-- Master Guide: Exact Poster Copy, Pitch Scripts, Domain Ownership, & Sources
│
├── Product_Design/                              <-- 💡 PRODUCT CONCEPTS & ARCHITECTURE
│   ├── Master_Fixed_vs_Flexible_Architecture.md <-- Master Source of Truth: Locked Science vs Open Team Choices
│   └── Form_Factor_Evaluation_Pendant_vs_Patch.md <-- Biomechanical Feasibility Analysis
│
└── Research_Dossier/
    ├── README.md                                <-- Research Progress & Question Registry
    │
    ├── Takeaways/                               <-- 🟢 TIER 2: EASY-TO-READ TAKEAWAY SUMMARIES (5-Min Reads)
    │   ├── Q1_1_Takeaway.md                     <-- Plain-English Q1.1 Information Summary
    │   ├── Q2_1_Takeaway.md                     <-- Plain-English Q2.1 Information Summary
    │   └── ...                                  <-- Matching takeaway for each question
    │
    ├── Product_Translations/                    <-- 🟡 TIER 2.5: PRODUCT IMPLEMENTATION & TRANSLATION
    │   ├── Q1_1_Product_Translation.md          <-- How & Why Q1.1 is implemented in our device
    │   ├── Q2_1_Product_Translation.md          <-- How & Why Q2.1 is implemented in our device
    │   └── ...                                  <-- Matching translation for each question
    │
    ├── Phase_01_Pathophysiology_and_Biomarkers/ <-- 🔵 TIER 3: DEEP RESEARCH VAULT
    │   ├── 1.1_Pre_Infarction_Cascade/          <-- Dedicated subfolder for Question 1.1
    │   │   ├── Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md
    │   │   └── Clinical_Realities_Hospital_Barriers_and_MI_Types.md
    │   ├── 1.2_Non_Invasive_Physical_Outputs/   <-- Dedicated subfolder for Question 1.2
    │   ├── ...
    │   └── assets/                              <-- Diagrams and visual models
    │
    └── Phase_02_Signal_Acquisition_Physics/     <-- 🟣 TIER 3: DEEP RESEARCH VAULT
        ├── 2.1_Sensing_Modalities_Biomarker_Mapping/
        │   └── Q2_1_Sensing_Modalities_Biomarker_Mapping.md
        ├── 2.2_Anatomical_Sweet_Spots/
        ├── ...
        └── assets/                              <-- Hardware & physics charts
```

### Key Folder Rules:
1. **Dedicated Question Subfolders for ALL Related Research**: Every deep research question has its own dedicated numbered subfolder (e.g., `1.1_Pre_Infarction_Cascade/`, `2.1_Sensing_Modalities_Biomarker_Mapping/`, `2.2_Anatomical_Sweet_Spots/`). **STRICT RULE**: Any research, deep-dives, clinical studies, engineering calculations, follow-up questions, or supplementary documents related to a specific question or subquestion MUST be saved directly inside that question's dedicated subfolder. NEVER save orphan research files at the phase root or anywhere outside its dedicated question folder.
2. **Centralized `Takeaways/` Directory (Tier 2)**: All plain-language takeaway summaries must live in `Research_Dossier/Takeaways/`, named strictly as `Q<Phase>_<Question>_Takeaway.md`. **NEVER** save product design notes, general chat takeaways, or non-question summaries in `Takeaways/`.
3. **Centralized `Product_Translations/` Directory (Tier 2.5: The Engineering Bridge)**: All system implementation and product translation dossiers live in `Research_Dossier/Product_Translations/`, named strictly as `Q<Phase>_<Question>_Product_Translation.md`. These files bridge Tier 3 science into concrete device reality by detailing: (1) how the finding fits our idea, (2) how we use it (hardware circuits, firmware logic), and (3) why we use it over alternatives.
4. **Dedicated `assets/` Folders**: All charts, diagrams, and figures must be stored in the `assets/` subfolder within each respective Phase.
5. **Live Ideathon Deliverables (`Ideathon_Poster_and_Pitch/`)**: All competition-facing poster templates, modular A0 frameworks, pitch notes, and slide deck copy live in `Ideathon_Poster_and_Pitch/`.
   - **Crucial Rule**: The team has NOT yet decided what each final part will be. Do NOT make up or lock in arbitrary decisions for the team.
   - The poster file must be structured as an **A0-sized modular canvas covering all 12 Phases (plus additional research)**, clearly leaving sections open/blank with **suggested candidate points, candidate tables, and evidence options** that the team can pick, choose, and customize as they see fit.
5. **Auto-Saving Chat Research, Brainstorming & Product Decisions**:
   - Whenever any in-depth research or technical discussion occurs relating to a specific question, save it directly inside that question's dedicated subfolder.
   - Whenever product-related research, form factor debates, or high-level architecture decisions occur, save them inside `Product_Design/`.
   - Maintain [`Master_Fixed_vs_Flexible_Architecture.md`](Product_Design/Master_Fixed_vs_Flexible_Architecture.md) as the single source of truth tracking what physical realities are locked in by science versus what design options remain open for team decision.
6. **Maintain `MASTER_PRODUCT_AND_RESEARCH_HUB.md` as the Primary Product Window**:
   - The primary entry point for anyone wanting to understand what the device actually is, what we have built, and what we know is [`MASTER_PRODUCT_AND_RESEARCH_HUB.md`](MASTER_PRODUCT_AND_RESEARCH_HUB.md).
   - Every time a question is completed or an engineering milestone is reached, update this Master Hub so that every single product feature has a direct reference link to its plain-English takeaway AND its deep-dive research dossier.
   - Deep-dive research files in `Phase_XX/` must NEVER be the sole accessible record—they are the underlying evidence layer.

## 3. Writing Rules for Takeaway Files (`Research_Dossier/Takeaways/`)

All files written in the `Takeaways/` folder must adhere to these strict user constraints:

1. **Simple, Plain-English Language**:
   - Use everyday words and clear, accessible sentences.
   - Do NOT bury the reader in heavy medical or engineering jargon.
   - When a technical term is necessary, explain it immediately in plain language (e.g., *Heart Rate Variability = the natural millisecond variation between heartbeats*).
2. **Strictly Informative Tone (NO Coaching)**:
   - Do **NOT** sound like a coach, pitch trainer, or debate teacher.
   - Absolutely **NO** lines like *"Here is what you tell judges"*, *"Your winning answer"*, *"When an investor asks you"*, or *"Rookie teams write dumb code"*.
   - Present the material purely as objective, structured, authoritative information.
3. **100% Heart-Centered (NO Car / Engine Analogies)**:
   - **Never** use mechanical, car, engine, or automotive analogies.
   - Keep all explanations strictly grounded in human cardiac biology: coronary blood vessels, heart muscle cramping and stiffening, oxygen starvation, electrical wiring, and fluid backpressure into the lungs.
4. **Mandatory "How This Helps Us" Section**:
   - Every single takeaway file MUST include a prominent section titled:  
     `## How This Helps Us: Direct Engineering & Project Value`  
     (or numbered equivalent like `## 3. How This Helps Us: Direct Engineering & Project Value`).
   - This section must explicitly detail how the research findings translate directly into hardware component selection, circuit architecture, false-alarm rejection software, and competitive clinical differentiation over smartwatches and hospitals.
5. **"Just Enough Detail"**:
   - Do not make it a 1-sentence elevator pitch, and do not make it a 50-page paper.
   - Standard structure for every takeaway file:
     1. *Core Scientific Finding*: What biological reality was discovered.
     2. *The Heart's Step-by-Step Struggle / Anatomical Reality*: Plain-language chronological or physical breakdown.
     3. *How This Helps Us: Direct Engineering & Project Value*: Explicit hardware, software, and clinical impact.
     4. *Hardware Sensor Mapping*: Which chip on the chest patch catches each step and why.
     5. *Software Detection Logic*: How algorithms check events in sequence or cross-verify modalities to eliminate false alarms.
     6. *Why Hospitals and Smartwatches Fail*: Clear structural explanations of competitor blind spots.
     7. *Different Kinds of Heart Attacks / Demographic Realities* (where applicable).
     8. *Key Takeaways in Brief*: Clean bulleted summary.

---

## 4. Writing Rules for Deep-Dive Research Files (`Phase_XX/`)

All master research files within question subfolders must follow the established Phase 1 academic standard:

1. **Standard Header Block**:
   ```markdown
   # Phase X: <Phase Name>
   ## Question X.Y: <Question Title>
   ### <Subtitle Detailing Scope>
   
   ---
   
   > **Ideathon Research Dossier Reference**: `Phase X -> Question X.Y`  
   > **Topic**: <Exact prompt question>  
   > **Status**: Verified Clinical & Engineering Synthesis (<N> Peer-Reviewed Sources + Cross-Reference Verification Matrix)
   ```
2. **Executive Summary & Systems Engineering Architecture**:
   - Chronological / Transduction ASCII diagram.
   - Embedded verified diagrams from `assets/`.
3. **Numbered Sections with Line-Level Verification**:
   - Every section must start with `*Mapped Sources: [...]` and a `> 🔎 **Exact Source Section Verification**:` callout detailing specific sections, tables, and figures from cited papers.
   - In-place definitions for medical terms in parentheses.
   - Governing mathematical and physical equations (LaTeX formatted).
   - Component-level analog front-end (AFE) specifications (ADS1292R, LSM6DSOX, MAX86141, etc.).
   - Exact clinical trial metrics (AUROC, RMSE, sensitivity, specificity, p-values, odds ratios).
4. **Section-to-Source Cross-Reference Verification Matrix**:
   - A structured markdown table mapping every claim to its exact citation, authority, and section/figure location.
5. **Complete Annotated Master Bibliography**:
   - Every source must be numbered, hyperlinked with full active URLs, and annotated with author, title, and subsection details.
6. **Strict Dedicated Subfolder Containment**:
   - Every master research file, supplementary study, clinical context document, or subquestion investigation MUST reside inside its specific dedicated numbered question subfolder (e.g., `1.1_Pre_Infarction_Cascade/`, `2.1_Sensing_Modalities_Biomarker_Mapping/`, `2.2_Anatomical_Sweet_Spots/`). Loose research files in the phase root folder are strictly forbidden.

---

## 5. Git and Version Control Protocols

1. **Frequent Remote Pulls & Local Synchronization (`git pull`)**:
   - The local repository must be kept frequently updated with the remote origin.
   - Execute `git pull origin main` (or `git pull --rebase origin main`) frequently—especially at the start of a session, before starting a new question phase, or when synchronizing local work—to prevent drift, stale branches, or merge conflicts with GitHub.
   - Always inspect `git status` beforehand to ensure uncommitted local changes are clean and safe.

2. **Batched Milestone Commits & Pushes (`git push`)**:
   - **DO NOT commit or push after every single file touch or minor line edit**:
     - The user has explicitly instructed: *"and stop using git agter eveu cahnge"*.
     - Keep active drafting and micro-edits local on disk.
   - **When to Commit & Push**:
     - Group commits into logical, complete milestones (e.g., upon finishing a full research question dossier + matching takeaway summary, completing a phase, or when explicitly commanded by the user).
     - Once a milestone batch is verified on disk and registries are updated, stage the relevant files (`git add`), create a structured commit, and execute `git push origin main` to keep the remote GitHub repository safely backed up.

3. **Standardized Commit Message Format**:
   - Always use clear, conventional commit prefixes:
     - `Docs: ...` for research questions, takeaways, and documentation updates.
     - `Feat: ...` for new scripts, hardware schematics, or simulation models.
     - `Refactor: ...` for folder restructurings, subfolder migrations, and guideline updates.
     - `Chore: ...` for registry synchronization and repo maintenance.

4. **Repository Cleanliness**:
   - Keep `git status` clean and verified at each milestone.
   - Ensure all files reside in their strictly assigned dedicated subfolders before staging.

---

## 6. Communication and Markdown Standards

1. **Clickable Links for All Files**:
   - Always create clickable markdown links using the `file:///` URI scheme with forward slashes for Windows:
     - `[filename](file:///c:/College/Ideathon/path/to/file.md)`
2. **Concise, Direct Responses**:
   - Keep conversational answers concise and structured.
   - Avoid unnecessary preambles or repeating the full contents of artifacts in the chat.
3. **Keep Registries Synchronized**:
   - Keep `README.md` and `Research_Dossier/README.md` updated as new question files and takeaways are created.
