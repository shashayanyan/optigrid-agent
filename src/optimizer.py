import pulp
import pandas as pd
import numpy as np
from typing import Tuple

class BatteryOptimizer:
    """
    A Linear Programming engine to optimize battery charge/discharge schedules
    against dynamic grid pricing to minimize commercial energy costs.
    """
    def __init__(self, capacity_kwh: float = 500.0, max_power_kw: float = 100.0, efficiency: float = 0.95):
        self.capacity_kwh = capacity_kwh
        self.max_power_kw = max_power_kw
        self.efficiency = efficiency  # Energy lost during charge/discharge round-trip

    def solve(self, forecast_df: pd.DataFrame) -> Tuple[pd.DataFrame, float, float]:
        """
        Takes a DataFrame containing 'predicted_load_kwh' and 'grid_price_usd'.
        Returns the optimized schedule, original cost, and optimized cost.
        """
        time_steps = forecast_df.index.tolist()
        
        # 1. Initialize the Linear Programming Problem
        prob = pulp.LpProblem("Microgrid_Cost_Minimization", pulp.LpMinimize)

        # 2. Define Variables (Using the new PuLP 4.0 syntax)
        charge = prob.add_variable_dicts("Charge", time_steps, lowBound=0, upBound=self.max_power_kw, cat='Continuous')
        discharge = prob.add_variable_dicts("Discharge", time_steps, lowBound=0, upBound=self.max_power_kw, cat='Continuous')
        soc = prob.add_variable_dicts("SOC", time_steps, lowBound=self.capacity_kwh * 0.1, upBound=self.capacity_kwh, cat='Continuous')

        # 3. Define the Objective Function (Minimize Cost)
        # Cost = (Building Load + Battery Charge - Battery Discharge) * Grid Price
        prob += pulp.lpSum(
            (forecast_df.loc[t, 'predicted_load_kwh'] + charge[t] - discharge[t]) * forecast_df.loc[t, 'grid_price_usd']
            for t in time_steps
        )

        # 4. Define Constraints (The Physics of the Battery)
        for i, t in enumerate(time_steps):
            if i == 0:
                # Initial state: assume battery starts at 50%
                prob += soc[t] == (self.capacity_kwh * 0.5) + (charge[t] * self.efficiency) - (discharge[t] / self.efficiency)
            else:
                # Energy conservation: Current SOC = Previous SOC + Charge - Discharge
                prev_t = time_steps[i-1]
                prob += soc[t] == soc[prev_t] + (charge[t] * self.efficiency) - (discharge[t] / self.efficiency)

        # 5. Solve the optimization matrix (Using bundled solver and silencing upstream deprecations)
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            prob.solve(pulp.PULP_CBC_CMD(msg=False))

        if pulp.LpStatus[prob.status] != 'Optimal':
            raise ValueError("Solver could not find an optimal solution.")

        # 6. Extract Results & Vectorized Financial Calculations
        results = forecast_df.copy()
        results['charge_kwh'] = [charge[t].varValue for t in time_steps]
        results['discharge_kwh'] = [discharge[t].varValue for t in time_steps]
        results['soc_kwh'] = [soc[t].varValue for t in time_steps]
        
        # Calculate new net grid load
        results['net_grid_load_kwh'] = results['predicted_load_kwh'] + results['charge_kwh'] - results['discharge_kwh']
        
        # Vectorized cost calculation (NumPy handles this implicitly via Pandas)
        original_cost = (results['predicted_load_kwh'] * results['grid_price_usd']).sum()
        optimized_cost = (results['net_grid_load_kwh'] * results['grid_price_usd']).sum()

        return results, original_cost, optimized_cost