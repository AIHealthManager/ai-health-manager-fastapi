CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sex VARCHAR(10),
    birth_date DATE,
    blood_type VARCHAR(5),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE conditions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_date TIMESTAMP NOT NULL DEFAULT now(),
    name TEXT NOT NULL,                        
    severity TEXT,
    description TEXT,
    outcome TEXT,
    source TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE doctor_visits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    visit_datetime TIMESTAMP NOT NULL,
    location TEXT,
    doctor_name TEXT,
    referred_by TEXT,
    reason TEXT NOT NULL,
    observations TEXT,
    diagnosis TEXT,
    referred_to TEXT,
    treatment TEXT,
    intervention TEXT,
    user_feedback TEXT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE health_measurements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    recorded_at TIMESTAMP NOT NULL DEFAULT now(),
    measurements TEXT NOT NULL, 
    context TEXT,
    notes TEXT,
    source TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE diagnostic_procedures (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    procedure_datetime TIMESTAMP NOT NULL DEFAULT now(),
    name TEXT NOT NULL,                     
    type TEXT DEFAULT 'lab',
    provider TEXT,                         
    results TEXT,                          
    notes TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE medication_intakes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    intake_datetime TIMESTAMP NOT NULL DEFAULT now(),
    medication_name TEXT NOT NULL,         
    dosage TEXT,                          
    reason TEXT,                     
    condition_id UUID REFERENCES conditions(id), 
    notes TEXT,
    source TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT now()
);