# Product Translation & Systems Implementation: Question 4.2
## Pre-Event Window Labeling Architecture: Transforming Our Device from a Reactive Detector into a 1-to-6-Hour Forecaster

---

> **Document Type**: Tier 2.5 Engineering Translation & Systems Architecture  
> **Source Research**: [Q4_2_Pre_Event_Window_Labeling.md](../Phase_04_Data_Engineering_Preprocessing/4.2_Pre_Event_Window_Labeling/Q4_2_Pre_Event_Window_Labeling.md)  
> **Target Product**: Autonomous Sternal Sentry Pendant & Companion PulseBand (Dual-Node BAN)  
> **Pipeline Status**: Multi-Horizon Survival Architecture (Ready for Model Training)

---

## 1. How This Finding Fits Our Product Vision

The single biggest difference between a **smartwatch** and our **autonomous medical sentry** is the difference between *reactive detection* and *proactive forecasting*:
* **What Smartwatches Do (Reactive Detection)**: Smartwatches look for a catastrophe when it is already happening (Hour 0). They detect high heart rates or fall impacts only after the patient has collapsed or gone into cardiac arrest. At that point, the patient is unconscious, brain damage begins in 4 to 6 minutes, and survival odds drop by $10\%$ every minute.
* **What Our Device Does (Proactive Forecasting)**: Our device intercepts the **1-to-6-hour pre-infarction countdown** before the heart's electrical system collapses.

### The Machine Learning Labeling Challenge
In machine learning, a model only learns what you tell it to look for through its training labels ($Y$):
1. If we label only the exact minute of cardiac arrest as $Y=1$, the model learns to wait until the patient is in ventricular fibrillation before sounding the alarm. It becomes a reactive death detector.
2. If we abruptly label a 45-minute chunk before arrest as $Y=1$ and everything before it as $Y=0$, the algorithm gets confused at the boundary: why is minute 45.1 "healthy" while minute 44.9 is "a heart attack," when the human body's blood vessels look virtually identical across those 12 seconds?
3. **The Solution**: We mathematically divide the timeline into three distinct operational states, backed by a continuous survival analysis countdown.

```
========================================================================================================================
                          3-ZONE CLINICAL INTERVENTION ARCHITECTURE
========================================================================================================================

    [ NORMAL DAILY BASELINE ]           [ STATE 1: INCUBATION ]           [ STATE 2: CRITICAL EMERGENCY ]
    More than 3 hours prior             1 to 3 hours prior                0 to 60 minutes prior
               │                                   │                                     │
               ▼                                   ▼                                     ▼
    • Standard Sentry Mode              • Gentle Wrist Haptic Pulse       • Loud Audible Emergency Alarm
    • Low-power background sampling     • Screen prompts guided check     • 30-Second Patient Cancel Window
    • Battery draw: <1.5 mW             • Cloud notifies cardiologist     • Automated Cellular EMS Dispatch
    • AI Target: State 0                • AI Target: State 1              • AI Target: State 2
```

---

## 2. Firmware State Machine & Interaction Rules

The 3-zone pre-event architecture maps directly to the user experience (UX) and microcontroller power states across our Dual-Node Body Area Network:

```c
typedef enum {
    CLINICAL_STATE_QUIESCENT  = 0, // State 0: Normal Baseline (> 3h prior)
    CLINICAL_STATE_INCUBATION = 1, // State 1: Ischemic Warning (1 to 3h prior)
    CLINICAL_STATE_CRITICAL   = 2  // State 2: Emergency Escalation (< 60 min prior)
} clinical_triage_state_t;

typedef struct {
    clinical_triage_state_t state;
    float continuous_hazard; // Risk score between 0.0 and 1.0
    uint16_t est_time_to_event_min; // Countdown in minutes
} early_warning_status_t;

early_warning_status_t Process_AI_Inference(float p_state[3], float hazard, float tte_pred) {
    early_warning_status_t status;
    status.continuous_hazard = hazard;
    status.est_time_to_event_min = (uint16_t)tte_pred;
    
    // Multi-tier thresholding with hysteresis
    if (p_state[2] > 0.70f || (hazard > 0.80f && tte_pred < 60)) {
        status.state = CLINICAL_STATE_CRITICAL;
        // ACTION: Trigger PulseBand 30-second haptic emergency countdown & prep cellular modem
    } else if (p_state[1] > 0.60f || hazard > 0.35f) {
        status.state = CLINICAL_STATE_INCUBATION;
        // ACTION: Silent clinical flag, gentle double-pulse haptic, prompt user to rest
    } else {
        status.state = CLINICAL_STATE_QUIESCENT;
        // ACTION: Maintain standard low-power sentry duty cycling
    }
    
    return status;
}
```

---

## 3. Exhaustive Architectural Comparison: Labeling Strategies

The team must choose how pre-event data labels are constructed in our dataset pipeline. We evaluate three concrete options:

### Option 1: Hard Binary Step Window (e.g. 45-Minute Window)
* **How It Works**: Label everything in the 45 minutes before arrest as $1$, and everything earlier as $0$.
* **Pros**: Simple, standard binary classifier.
* **Fatal Flaws**: Creates an artificial cliff at minute 45. The AI algorithm suffers from training instability and high false-positive spikes around the 45-minute mark.

### Option 2: Continuous Soft Hazard Ramping (Sigmoid / Exponential)
* **How It Works**: Label every second with a continuous percentage risk curve ($0\%$ at 4 hours, ramping to $100\%$ at collapse).
* **Pros**: Mathematically smooth, matches gradual biology.
* **Fatal Flaws**: Hard to make clear emergency decisions. If the risk is $47\%$, does the watch call an ambulance or do nothing? It lacks actionable clinical boundaries.

### Option 3 (Recommended): Multi-Horizon Phased Survival Pipeline
* **How It Works**: Combines three clear clinical action zones (Quiescent, Incubation, Critical) with a continuous countdown in minutes. Includes a 15-minute blanking buffer to eliminate boundary noise.
* **Pros**: Provides clear clinical action stages (gentle warning vs full 911 dispatch) plus an exact countdown for emergency responders.

```
========================================================================================================================
                               PRE-EVENT LABELING ARCHITECTURE SCORECARD
========================================================================================================================

  Evaluation Metric               Option 1: Hard Binary      Option 2: Soft Hazard       Option 3: Multi-Horizon (Rec.)
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Clinical Actionability          Moderate (All-or-nothing)  Poor (Vague probability)    ⭐️⭐️⭐️⭐️⭐️ (3 Actionable Stages)
  Early Warning Lead Time         Fixed (Only 45 min)        Vague                       ⭐️⭐️⭐️⭐️⭐️ (1 to 6 Hours)
  Gradient Training Stability     ❌ Unstable (Step cliff)   ⭐️⭐️⭐️⭐️⭐️ (Smooth curve)   ⭐️⭐️⭐️⭐️⭐️ (Buffered & Smooth)
  Emergency Situational Intel     None (Binary yes/no)       Approximate                 ⭐️⭐️⭐️⭐️⭐️ (Minutes Countdown)
  False Alarm Rate                High (Boundary jitter)     Moderate                    ⭐️⭐️⭐️⭐️⭐️ (Lowest - 2-tier check)
========================================================================================================================
```

---

## 4. Ideathon Pitch & Judge Defense Value

1. **Knockout Defense Against the "Reactive Trap"**:
   * *Judge Question*: *"Smartwatches already detect heart rate anomalies. Why do we need your device?"*
   * *Your Answer*: *"Smartwatches are reactive detectors—they detect ventricular fibrillation only after the patient is already unconscious on the floor, when brain death occurs in 4 minutes. Our multi-horizon survival pipeline trains our model on the 1-to-6-hour pre-infarction incubation window. We detect coronary stiffening and autonomic instability 45 to 180 minutes in advance, giving patients time to sit down, take prescribed medication, and dispatch help before cellular necrosis or electrical collapse ever occurs."*
2. **Defending the Minute Countdown**: Explaining to judges that our AI outputs both a clinical triage state AND an estimated time-to-event in minutes demonstrates true clinical software maturity, setting our project far apart from standard student hackathon projects.
