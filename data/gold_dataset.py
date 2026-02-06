# Annotated gold dataset of clinical questions
GOLD_DATASET = [
    {
      "question": "What was the primary outcome for the original Diabetes Prevention Program (DPP)?",
      "expected": "The development of diabetes, defined by 1997 ADA criteria",
      "source_page": [13,63]
    },
    {
      "question": "Which groups were originally included in the DPP randomization, and which one was discontinued early?",
      "expected": "Participants were assigned to intensive lifestyle, metformin, or placebo ; a fourth arm, troglitazone, was discontinued in June 1998 due to potential liver toxicity.",
      "source_page": [4,63,64]
    },
    {
      "question": "What is the primary objective of DPPOS Phase 3?",
      "expected": "To evaluate the long-term effects of metformin compared with placebo on the incidence of cancer and major atherosclerotic cardiovascular events (MACE).",
      "source_page": [10,11]
    },
    {
      "question": "List the secondary objectives of DPPOS Phase 3.",
      "expected": "To evaluate effects on the further development of diabetes, microvascular and selected health outcomes, risk factors for those outcomes, and the costs and cost-utility associated with diabetes prevention.",
      "source_page": [7]
    },
    {
      "question": "Why was it critical to establish a long-term follow-up study like DPPOS after the initial DPP concluded?",
      "expected": "To determine if delaying or preventing diabetes translates into a decrease in retinopathy, nephropathy, neuropathy, and cardiovascular disease, which require more years to develop than the original DPP period.",
      "source_page": [5]
    },
    {
      "question": "What were the results of the DPP Phase 1 regarding diabetes incidence reductions?",
      "expected": "Intensive lifestyle and metformin reduced the development of diabetes by 58% and 31% risk reduction, respectively, compared to placebo.",
      "source_page": [16]
    },
    {
      "question": "Does the protocol state that the placebo group received no intervention during the DPPOS follow-up?",
      "expected": "No; at the end of the DPP, all participants, including the former placebo group, were offered a group-implemented lifestyle modification program.",
      "source_page": [5]
    },
    {
      "question": "What findings from the UKPDS study support the rationale for the 10-year follow-up in DPPOS?",
      "expected": "UKPDS showed that even after glucose control no longer differed between groups, those previously on intensive regimens had continued reductions in microvascular complications and new reductions in myocardial infarction and mortality.",
      "source_page": [22]
    },
    {
      "question": "How is the 'MACE' outcome defined in DPPOS Phase 3?",
      "expected": "It is defined as the first occurrence of nonfatal or fatal myocardial infarction or stroke, or any cardiovascular death occurring since DPP randomization.",
      "source_page": [8]
    },
    {
      "question": "What are the components of the 'composite diabetes-related microangiopathic and neuropathic outcome' used in Phase 2?",
      "expected": "The composite includes Nephropathy (increased albuminuria or renal dysfunction), Retinopathy (Photography grade 20 or greater or history of treatment), and Neuropathy (reduced monofilament sensation).",
      "source_page": [8,31]
    },
    {
      "question": "What is the diagnostic threshold for diabetic retinopathy in DPPOS Phase 3?",
      "expected": "The definition is mild diabetic retinopathy, specifically an ETDRS grade of 35 or greater, or adjudicated treatment for retinopathy.",
      "source_page": [31]
    },
    {
      "question": "How is nephropathy defined for the Phase 3 secondary outcome based on KDIGO categories?",
      "expected": "Confirmed elevated albuminuria (>= 30 mg/g), confirmed eGFR < 45 ml/min, kidney transplant, or dialysis for end-stage renal disease.",
      "source_page": [31]
    },
    {
      "question": "What is the primary difference in the visit schedule between DPPOS Phases 1 & 2 and Phase 3?",
      "expected": "During Phases 1 & 2, participants had twice-yearly scheduled visits; in Phase 3, they have one annual in-person visit and a mid-year assessment by telephone.",
      "source_page": [37,40]
    },
    {
      "question": "How are troglitazone participants handled in the DPPOS Phase 3 analysis?",
      "expected": "They are no longer followed in DPPOS and are not included in the primary Phase 3 analyses because they had limited exposure to the original intervention.",
      "source_page": [64]
    },
    {
      "question": "What are the criteria for suspending the scheduled follow-up protocol?",
      "expected": "Voluntary withdrawal by the participant or a condition that, in the opinion of the PI, makes it unsafe for the participant to continue.",
      "source_page": [41]
    },
    {
      "question": "What actions are taken for 'recovery' of inactive participants?",
      "expected": "A graded hierarchy of recovery efforts including social support, staff contact, and honorariums in recognition of time and effort.",
      "source_page": [42,43]
    },
    {
      "question": "Are participants who move away from a clinical center automatically excluded from the study?",
      "expected": "No; a 'remote visit' may be performed by a non-DPPOS staff person trained and certified in DPPOS procedures to collect outcome data.",
      "source_page": [41]
    },
    {
      "question": "What is the purpose of the annual 'lifestyle check-up' for the original ILS group?",
      "expected": "A brief (10-15 minute) review of lifestyle goals and success to reinforce lessons and promote retention.",
      "source_page": [44]
    },
    {
      "question": "Should metformin be used during pregnancy or breast-feeding?",
      "expected": "No; it is recommended that metformin be discontinued in DPPOS participants during pregnancy and for the duration of breast-feeding.",
      "source_page": [49]
    },
    {
      "question": "Does the protocol specify the use of SGLT2 inhibitors for participants with new-onset diabetes?",
      "expected": "The provided text does not mention SGLT2 inhibitors; it focuses on metformin use and a stepped care protocol for HbA1c >= 7%.",
      "source_page": [51]
    },
    {
      "question": "What is the reporting timeframe for a death or life-threatening unexpected adverse event?",
      "expected": "All deaths or life-threatening unexpected adverse events must be reported to the Coordinating Center within 24 hours of clinic notification.",
      "source_page": [52]
    },
    {
      "question": "How is the confidentiality of patient data ensured at the Coordinating Center (CoC)?",
      "expected": "Staff sign a confidentiality policy; security includes logon/password protection, SSL, encryption algorithms, and hourly virus protection updates.",
      "source_page": [55]
    },
    {
      "question": "What is the process for editing data forms once they are completed at a clinical center?",
      "expected": "Clinic staff review forms before entry; they are edited during web-based entry and again by the central data management system at the CoC.",
      "source_page": [53,55]
    },
    {
      "question": "What statistical principle is used for primary and secondary outcome analyses?",
      "expected": "The primary and secondary outcome analyses follow the 'intention to treat' principle.",
      "source_page": [10]
    },
    {
      "question": "How is the study powered to detect a hazard risk reduction in MACE?",
      "expected": "It assumes a 2.1 fold age-related increase in incidence and requires 145 placebo events for 85% power to detect a 30% hazard risk reduction .",
      "source_page": [64]
    },
    {
      "question": "What significance level is used for the primary outcome analysis in DPPOS Phase 1?",
      "expected": "An overall significance level of 0.05 (2-sided), with 0.025 level for pair-wise comparisons.",
      "source_page": [63]
    },
    {
      "question": "When did the DPPOS Phase 3 follow-up period officially commence?",
      "expected": "July 1, 2015.",
      "source_page": [6]
    },
    {
      "question": "What are the common side effects associated with Metformin mentioned in the protocol?",
      "expected": "Gastrointestinal symptoms including diarrhea, nausea, metallic taste, abdominal bloating, flatulence, or anorexia.",
      "source_page": [45]
    },
    {
      "question": "When is Metformin treatment permanently discontinued due to kidney function?",
      "expected": "If eGFR levels are < 30 mL/minute/1.73 m2, study-supplied metformin is discontinued permanently.",
      "source_page": [46,47] 
    },
    {
      "question": "What is the dosage of metformin provided to participants originally assigned to that group?",
      "expected": "Open label metformin therapy is provided at 850 mg twice per day.",
      "source_page": [7]
    }
  ]