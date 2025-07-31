from agents import function_tool, RunContextWrapper

from ai.context import AgentContext
from managers.visit_manager import VisitManager
from managers.condition_manager import ConditionManager
from managers.health_measurement_manager import HealthMeasurementManager
from managers.diagnostic_procedure_manager import DiagnosticProcedureManager
from managers.medication_intake_manager import MedicationIntakeManager
from schemas.visit_schemas import VisitCreate, Visit, VisitUpdate
from schemas.condition_schemas import ConditionCreate, Condition
from schemas.health_measurement_schemas import HealthMeasurement, HealthMeasurementCreate
from schemas.diagnostic_procedure_schemas import DiagnosticProcedureCreate, DiagnosticProcedure
from schemas.medication_intake_schemas import MedicationIntake, MedicationIntakeCreate


@function_tool
async def record_doctor_visit(
    wrapper: RunContextWrapper[AgentContext],
    visit_data: VisitCreate,
) -> Visit:
    """
    Records a doctor visit with comprehensive medical information and outcomes.

    This tool captures complete doctor visit details including timing, personnel, medical findings,
    treatments, and referrals. Use it when users report any healthcare appointment or medical consultation.

    Examples of when to use:
    - "I saw my doctor today for a checkup" → reason="routine checkup", visit_datetime=today
    - "Dr. Smith diagnosed me with high blood pressure" → doctor_name="Dr. Smith", diagnosis="hypertension"
    - "The ER referred me to a cardiologist" → referred_by="Emergency Room", referred_to="Cardiologist"
    - "My physical therapy session went well" → reason="physical therapy", user_feedback="went well"

    Args:
        visit_data (DoctorVisitCreate): Comprehensive visit information containing:
            - visit_datetime (required): When the visit occurred
            - reason (required): Purpose of the visit (e.g., "routine checkup", "follow-up", "emergency")
            - location (optional): Where the visit took place (e.g., "City Hospital", "Dr. Smith's Office")
            - doctor_name (optional): Name of the healthcare provider seen
            - referred_by (optional): Who referred the patient (e.g., "Dr. Johnson", "Emergency Room")
            - observations (optional): Healthcare provider's clinical observations
            - diagnosis (optional): Medical diagnosis or assessment given
            - referred_to (optional): Any referrals made (e.g., "Specialist", "Physical Therapy")
            - treatment (optional): Treatments prescribed or administered
            - intervention (optional): Medical procedures or tests performed
            - user_feedback (optional): Patient's experience or thoughts about the visit

    Returns:
        DoctorVisit: The stored visit record with unique ID, timestamps, and all provided medical data.
        
    Raises:
        DatabaseError: If the visit record cannot be saved to the database.
        ValidationError: If required fields are missing or invalid.
    """
    return await VisitManager.insert_doctor_visit(
        visit_data, 
        wrapper.context.user_id, 
        wrapper.context.db
    )


@function_tool
async def update_doctor_visit_details(
    wrapper: RunContextWrapper[AgentContext],
    visit_id: str,
    visit_updates: VisitUpdate,
) -> Visit | None:
    """
    Updates an existing doctor visit record with new information or corrections.

    Use this tool when users want to add missing details, correct information, or update
    their feedback about a previously recorded visit.

    Examples of when to use:
    - "I forgot to mention the doctor prescribed antibiotics" → treatment="prescribed antibiotics"
    - "The test results came back - I have diabetes" → diagnosis="diabetes"
    - "I want to add that the visit was very helpful" → user_feedback="very helpful experience"

    Args:
        visit_id (str): The unique identifier of the visit to update.
        visit_updates (DoctorVisitUpdate): Fields to update (only non-None values will be updated):
            - All fields from DoctorVisitCreate are optional for updates
            - Only provided fields will be modified, others remain unchanged

    Returns:
        DoctorVisit: The updated visit record, or None if the visit was not found.
        
    Raises:
        DatabaseError: If the update cannot be performed.
        PermissionError: If the user doesn't own the visit record being updated.
    """
    return await VisitManager.update_doctor_visit(
        visit_id,
        visit_updates,
        wrapper.context.user_id, 
        wrapper.context.db
    )


@function_tool
async def report_condition(
    wrapper: RunContextWrapper[AgentContext],
    condition_data: ConditionCreate,
) -> Condition:
    """
    Records a user-reported health condition, symptom, injury, or illness.

    This tool captures health events with their timing, severity, and context. Use it when users 
    report any health-related issues, from minor symptoms to significant medical events.

    Examples of when to use:
    - "I have a headache" → name="headache", severity="mild"
    - "I broke my arm yesterday" → name="broken arm", event_date=yesterday, severity="severe"
    - "My back pain is getting better" → name="back pain", outcome="improved"
    - "The doctor diagnosed me with diabetes" → name="diabetes", source="doctor"

    Args:
        condition_data (ConditionCreate): Structured condition input containing:
            - name (required): Clear, descriptive name of the condition/symptom
            - severity (optional): "mild", "moderate", "severe", or custom description
            - description (optional): Additional context, symptoms, or details
            - outcome (optional): Current status like "resolved", "ongoing", "improved", "worsened"
            - event_date (optional): When the condition occurred/was noticed (defaults to now)
            - source (optional): Who reported it - "user", "doctor", "device" (defaults to "user")

    Returns:
        Condition: The stored condition record with unique ID, timestamps, and all provided data.
        
    Raises:
        DatabaseError: If the condition cannot be saved to the database.
    """
    return await ConditionManager.insert_condition(
        condition_data, 
        wrapper.context.user_id, 
        wrapper.context.db
    )


@function_tool
async def record_health_measurement(
    wrapper: RunContextWrapper[AgentContext],
    measurement_data: HealthMeasurementCreate,
) -> HealthMeasurement:
    """
    Records user-reported health measurements such as vital signs, weight, or other quantifiable health data.

    This tool captures objective health metrics with timing and context. Use it when users report
    measurable health data, whether from self-monitoring, medical devices, or healthcare visits.

    Examples of when to use:
    - "My blood pressure is 120/80" → measurements="BP: 120/80"
    - "I weigh 150 pounds this morning" → measurements="Weight: 150 lbs", context="morning reading"
    - "My heart rate was 85 after my run" → measurements="HR: 85 bpm", context="after exercise"
    - "The doctor measured my temperature at 99.2°F" → measurements="Temperature: 99.2°F", source="doctor"
    - "My glucose meter shows 110 mg/dL" → measurements="Glucose: 110 mg/dL", source="device"

    Args:
        measurement_data (HealthMeasurementCreate): Structured measurement input containing:
            - measurements (required): The actual measurement values and units (e.g., "BP: 120/80", "Weight: 70 kg")
            - recorded_at (optional): When the measurement was taken (defaults to now if not specified)
            - context (optional): Circumstances of measurement (e.g., "morning", "after exercise", "at clinic")
            - notes (optional): Additional observations or user comments about the measurement
            - source (optional): Who/what recorded it - "user", "device", "doctor" (defaults to "user")

    Returns:
        HealthMeasurement: The stored measurement record with unique ID, timestamps, and all provided data.
        
    Raises:
        DatabaseError: If the measurement cannot be saved to the database.
        ValidationError: If required measurement data is missing or invalid.
    """
    return await HealthMeasurementManager.insert_health_measurement(
        measurement_data,
        wrapper.context.user_id,
        wrapper.context.db
    )


@function_tool
async def record_diagnostic_procedure(
    wrapper: RunContextWrapper[AgentContext],
    procedure_data: DiagnosticProcedureCreate,
) -> DiagnosticProcedure:
    """
    Records diagnostic procedures such as lab tests, imaging studies, biopsies, and other medical examinations.

    This tool captures medical procedures performed to diagnose or monitor health conditions, including
    their results and findings. Use it when users report any diagnostic test or examination they've had done.

    Examples of when to use:
    - "I had blood work done today" → name="Complete Blood Count", type="lab"
    - "My chest X-ray showed clear lungs" → name="Chest X-Ray", type="imaging", results="clear lungs"
    - "The MRI revealed a herniated disc" → name="MRI Lumbar Spine", type="imaging", results="herniated disc L4-L5"
    - "My colonoscopy was normal" → name="Colonoscopy", type="endoscopy", results="normal findings"
    - "Blood sugar test came back at 95" → name="Glucose Test", type="lab", results="95 mg/dL"
    - "The biopsy was benign" → name="Skin Biopsy", type="biopsy", results="benign lesion"

    Args:
        procedure_data (DiagnosticProcedureCreate): Structured procedure information containing:
            - name (required): Specific name of the procedure or test (e.g., "Complete Blood Count", "Chest X-Ray")
            - procedure_datetime (optional): When the procedure was performed (defaults to now if not specified)
            - type (optional): Category of procedure - "lab", "imaging", "biopsy", "endoscopy", "cardiac" (defaults to "lab")
            - provider (optional): Who performed the procedure (e.g., "City Hospital Lab", "Dr. Smith", "Radiology Associates")
            - results (optional): Test results, findings, or outcomes from the procedure
            - notes (optional): Additional information, patient experience, or follow-up instructions

    Returns:
        DiagnosticProcedure: The stored procedure record with unique ID, timestamps, and all provided medical data.
        
    Raises:
        DatabaseError: If the procedure record cannot be saved to the database.
        ValidationError: If required procedure information is missing or invalid.
    """
    return await DiagnosticProcedureManager.insert_diagnostic_procedure(
        procedure_data,
        wrapper.context.user_id,
        wrapper.context.db
    )


@function_tool
async def record_medication_intake(
    wrapper: RunContextWrapper[AgentContext],
    intake_data: MedicationIntakeCreate,
) -> MedicationIntake:
    """
    Records when a user takes medication, including dosage, timing, and purpose.

    This tool tracks medication usage for treatment monitoring, adherence tracking, and health management.
    Use it when users report taking any medication, whether prescription, over-the-counter, or supplements.

    Examples of when to use:
    - "I took 200mg of ibuprofen for my headache" → medication_name="Ibuprofen", dosage="200mg", reason="headache"
    - "Just took my morning diabetes medication" → medication_name="Metformin", reason="diabetes management"
    - "Had to take an extra blood pressure pill today" → medication_name="Lisinopril", notes="extra dose due to high reading"
    - "Took my prescribed antibiotic" → medication_name="Amoxicillin", source="prescription"
    - "Used my inhaler during the asthma attack" → medication_name="Albuterol", reason="asthma symptoms", condition_id="<asthma_condition_id>"

    Args:
        intake_data (MedicationIntakeCreate): Structured medication intake information containing:
            - medication_name (required): Name of the medication taken (e.g., "Ibuprofen", "Metformin", "Vitamin D")
            - intake_datetime (optional): When the medication was taken (defaults to now if not specified)
            - dosage (optional): Amount taken (e.g., "200mg", "2 tablets", "10mg twice daily")
            - reason (optional): Why the medication was taken (e.g., "headache", "diabetes", "prevention")
            - condition_id (optional): UUID of related condition if linking to existing health condition
            - notes (optional): Additional information, side effects experienced, or special circumstances
            - source (optional): How medication was obtained - "user", "prescription", "doctor" (defaults to "user")

    Returns:
        MedicationIntake: The stored intake record with unique ID, timestamps, and all provided medication data.
        
    Raises:
        DatabaseError: If the medication intake cannot be saved to the database.
        ValidationError: If required medication information is missing or invalid.
        ReferenceError: If condition_id is provided but the condition doesn't exist or belong to the user.
    """
    return await MedicationIntakeManager.insert_medication_intake(
        intake_data,
        wrapper.context.user_id,
        wrapper.context.db
    )