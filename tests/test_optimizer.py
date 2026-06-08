import pytest
import pandas as pd
import numpy as np
from src.optimizer import BatteryOptimizer

def test_battery_optimizer_logic():
    # 1. Setup: Create a synthetic 24-hour forecast
    dates = pd.date_range("2026-01-01", periods=24, freq="h")
    df = pd.DataFrame(index=dates)
    
    # Constant building load of 50 kW
    df['predicted_load_kwh'] = 50.0
    
    # Dynamic Pricing: 
    # $0.05 (cheap) from midnight to 6 AM
    # $0.10 (average) from 6 AM to 2 PM
    # $0.40 (expensive peak) from 2 PM to 8 PM
    # $0.10 (average) from 8 PM to midnight
    prices = [0.05] * 6 + [0.10] * 8 + [0.40] * 6 + [0.10] * 4
    df['grid_price_usd'] = prices

    # 2. Execution: Initialize with a 200kWh battery, max charge rate of 50kW
    # We use 100% efficiency (1.0) here purely to make the math assertions perfectly clean
    optimizer = BatteryOptimizer(capacity_kwh=200.0, max_power_kw=50.0, efficiency=1.0)
    results, original_cost, optimized_cost = optimizer.solve(df)

    # 3. Assertions: Financials
    assert optimized_cost < original_cost, "The battery should save money compared to doing nothing."
    
    # 4. Assertions: Physics and Constraints
    assert results['soc_kwh'].max() <= 200.0, "Battery exceeded maximum capacity!"
    assert results['soc_kwh'].min() >= 20.0, "Battery dropped below the 10% minimum safety limit!"
    assert results['charge_kwh'].max() <= 50.0, "Charge rate exceeded max power constraint!"
    assert results['discharge_kwh'].max() <= 50.0, "Discharge rate exceeded max power constraint!"

    # 5. Assertions: Optimization Logic
    # During the cheap night hours (first 6 hours), it should charge to prepare for the day
    assert results.iloc[0:6]['charge_kwh'].sum() > 0, "Failed to charge during cheap off-peak hours."
    
    # During the expensive peak afternoon hours (e.g., 4 PM / 16:00), it should be discharging
    assert results.iloc[16]['discharge_kwh'] > 0, "Failed to discharge to offset expensive peak hours."

    print(f"\nOriginal Cost: ${original_cost:.2f}")
    print(f"Optimized Cost: ${optimized_cost:.2f}")
    print(f"Total Savings: ${(original_cost - optimized_cost):.2f}")