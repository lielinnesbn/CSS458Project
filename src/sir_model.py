# src/sir_model.py

import numpy as np

class ResourceConstrainedSIR:
    """
    Implements a discrete-time Susceptible-Infectious-Recovered (SIR) model
    with a capacity-dependent recovery rate.
    
    The twist in this model is the 'Resource Constraint':
    If infections exceed capacity (C), the recovery rate (gamma) drops,
    simulating a strictly limited healthcare system (e.g., lack of ICU beds).
    """

    def __init__(self, N, I0, beta, gamma_base, capacity_C):
        """
        Initializes the simulation parameters.
        
        Args:
            N (float): Total Population size.
            I0 (float): Initial number of Infected individuals.
            beta (float): The transmission rate (how contagious the virus is).
            gamma_base (float): The ideal recovery rate (1 / duration_of_illness) 
                                assuming hospitals are NOT full.
            capacity_C (float): The healthcare system capacity (max simultaneous patients).
        """
        # --- 1. System State Initialization ---
        self.N = float(N)
        
        # Lists to store the history of the simulation (State Vectors)
        # S: Susceptible (Healthy but can get sick)
        # I: Infectious (Currently sick and spreading)
        # R: Recovered (Healed or Removed, immune)
        self.S = [N - I0]  
        self.I = [I0]      
        self.R = [0.0]     
        
        # --- 2. Parameter Setup ---
        self.beta = beta
        self.gamma_base = gamma_base
        self.C = float(capacity_C)
        
        # Time tracking
        self.time_steps = [0]
        # To analyze how the recovery rate changed over time
        self.gamma_eff_history = []
        
        # Counter for how long the hospital system was overwhelmed
        self.breach_days = 0 

    def run_simulation(self, days):
        """
        Runs the simulation loop for a set number of days.
        Uses discrete time steps (t -> t+1).
        """
        
        for t in range(days):
            # Get the state at the current time step (the last item in the lists)
            S_t = self.S[-1]
            I_t = self.I[-1]
            R_t = self.R[-1]

            # --- 3. Dynamic Recovery Logic (The Resource Constraint) ---
            # Standard SIR models have a constant recovery rate. 
            # Here, gamma changes if hospitals are full.
            
            if I_t > self.C:
                # CAPACITY EXCEEDED:
                # The effective recovery rate decreases because resources are split.
                # Formula: gamma_new = gamma_base * (Capacity / Current_Infections)
                # As I_t gets larger, gamma_eff gets smaller (people stay sick longer).
                gamma_eff = self.gamma_base * (self.C / I_t)
                self.breach_days += 1
            else:
                # CAPACITY OK:
                # Hospitals are under capacity; recovery proceeds at normal speed.
                gamma_eff = self.gamma_base
                
            # Log the gamma used for this step for later plotting
            self.gamma_eff_history.append(gamma_eff)
            
            # --- 4. The Math of Transmission (Differential Equations) ---
            
            # INFECTION (S -> I):
            # New infections = Transmission Rate * Susceptible * (Probability of contact with Infected)
            # Probability of contact = I_t / N
            delta_I_new = self.beta * S_t * (I_t / self.N)
            
            # RECOVERY (I -> R):
            # New recoveries = Effective Recovery Rate * Current Infected count
            delta_R_new = gamma_eff * I_t
            
            # --- 5. Update State for Next Time Step ---
            
            # Susceptible decreases by the number of new infections
            S_next = S_t - delta_I_new
            
            # Infected increases by new infections, decreases by recoveries
            I_next = I_t + delta_I_new - delta_R_new
            
            # Recovered increases by new recoveries
            R_next = R_t + delta_R_new
            
            # Append results to history lists. 
            # We use max(0, val) to prevent math errors from creating negative people
            # (which can happen in discrete steps if numbers get very small).
            self.S.append(max(0, S_next))
            self.I.append(max(0, I_next))
            self.R.append(max(0, R_next))
            self.time_steps.append(t + 1)
        
        # Return the history as NumPy arrays to make graphing easy later
        return np.array(self.S), np.array(self.I), np.array(self.R)

    def get_metrics(self):
        """
        Analyzes the simulation history to extract key performance indicators (KPIs).
        Useful for comparing different scenarios (e.g., "Flattening the Curve").
        """
        # Convert lists to arrays for easier math operations
        I_array = np.array(self.I)
        R_array = np.array(self.R)
        Time_array = np.array(self.time_steps)
        
        # 1. Peak Infections: The highest number of people sick at once
        I_max = np.max(I_array)
        
        # 2. Peak Time: On which day did the peak occur?
        T_peak_index = np.argmax(I_array)
        T_peak = Time_array[T_peak_index]
        
        # 3. Total recovered (Cumulative cases) at the end of the simulation
        R_infinity = R_array[-1]
        
        # 4. End of Pandemic: Find the first day where Infections drop below 1
        # np.where returns indices where the condition is true
        T_end_index = np.where(I_array < 1)[0]
        
        # Check if the pandemic actually ended, or if we ran out of time
        if len(T_end_index) > 0:
            T_end = Time_array[T_end_index[0]]
        else:
            T_end = Time_array[-1] # Pandemic was still ongoing at end of sim

        return {
            'I_max': I_max,                  # Highest height of the curve
            'T_peak': T_peak,                # Day of the peak
            'T_breach': self.breach_days,    # Days hospitals were overloaded
            'R_infinity': R_infinity,        # Total people who got sick and recovered
            'T_end': T_end,                  # Day the virus died out
            'Final_N_Check': self.S[-1] + self.I[-1] + self.R[-1] # Sanity check (should close to N)
        }