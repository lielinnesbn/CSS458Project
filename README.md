# CSS458Project
Cadence Smith and Liel Ben Noon's project for CSS 458 Autumn Quarter 2025. 

Simulating Healthcare Saturation
Model Type: System Dynamics (Discrete-Time Compartmental Model)

This project implements a System Dynamics (SD) model to simulate the spread of an infectious disease within a community. Unlike the classic SIR model, this simulation incorporates a critical resource constraint: a fixed Healthcare Capacity (C).The primary objective is to study the consequences of system saturation, where the recovery rate (gamma) dynamically slows down whenever the number of active cases (I) exceeds C. This allows us to quantify the cost of overwhelmed hospitals on the total epidemic size and duration.

The project is designed to answer critical public health questions:
Duration of Crisis: We want to calculate the total number of days the healthcare system operates beyond its defined capacity C.
Policy Effectiveness: We want to determine the required percentage reduction in the infection rate (beta) needed to prevent capacity breach entirely.
Cost of Saturation: We want to quantify how much the total **Attack Rate ($R_{\infty}$) ** increases when recovery is slowed due to resource constraints.
