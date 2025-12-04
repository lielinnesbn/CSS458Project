# data/parameters.py

# --- A. Population and Initial Conditions ---

# Total population size (N): Medium-sized city for simulation
N_POP = 100000 

# Initial number of infected individuals (I0) at time t=0
I0 = 100

# --- B. Epidemiological Parameters (Fixed) ---

# Baseline Recovery Rate (gamma_base): Assumes average infectious period of 14 days
# Gamma = 1 / Duration
GAMMA_BASE = 1.0 / 14.0 

# Time to run the simulation in days
DAYS = 150

# --- C. Scenario-Specific Parameters ---

# Healthcare System Capacity (C): 0.5% of the total population (500 individuals)
# This is the critical threshold for saturation.
CAPACITY_C = N_POP * 0.005 

# Baseline Transmission Rate (beta): Set to achieve a high R0 (~4.2) for a strong outbreak
# R0 = BETA / GAMMA_BASE
BETA_BASELINE = 0.3 

# Policy Transmission Rate (Policy Test Beta): 50% reduction from baseline
BETA_POLICY = BETA_BASELINE * 0.5