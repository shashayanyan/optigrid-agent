import pandas as pd
from crewai.tools import tool
from optimizer import BatteryOptimizer

@tool("Battery Optimization Tool")
def run_battery_optimization() -> str:
    """
    Runs the Linear Programming optimizer on the next 24 hours of grid data.
    Use this tool to calculate energy costs and battery savings.
    Returns a financial summary of the original cost, optimized cost, and total savings.
    """
    # 1. Generate the 24-hour forecast data (Using our synthetic scenario)
    dates = pd.date_range("2026-01-01", periods=24, freq="h")
    df = pd.DataFrame(index=dates)
    df['predicted_load_kwh'] = 50.0
    
    # Grid prices: Cheap at night ($0.05), expensive in afternoon ($0.40)
    prices = [0.05] * 6 + [0.10] * 8 + [0.40] * 6 + [0.10] * 4
    df['grid_price_usd'] = prices

    # 2. Run the optimizer
    optimizer = BatteryOptimizer(capacity_kwh=200.0, max_power_kw=50.0, efficiency=1.0)
    results, original_cost, optimized_cost = optimizer.solve(df)
    savings = original_cost - optimized_cost

    # 3. Return the mathematical result as a string for the LLM to read
    return (
        f"Optimization Complete. "
        f"Cost without battery: ${original_cost:.2f}. "
        f"Cost with optimized battery scheduling: ${optimized_cost:.2f}. "
        f"Total Daily Savings: ${savings:.2f}. "
        f"Strategy: Charged during $0.05 off-peak hours, discharged during $0.40 peak hours."
    )