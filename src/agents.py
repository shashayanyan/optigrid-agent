import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from tools import run_battery_optimization

# 1. Explicitly load .env 
load_dotenv()

def run_agentic_workflow():
    # 2. Use the LiteLLM string format for Gemini
    gemini_model = "gemini/gemini-2.5-flash"

    # --- Define the Agents ---
    
    energy_analyst = Agent(
        role='Lead Energy Optimization Analyst',
        goal='Run mathematical battery optimizations and analyze the financial ROI.',
        backstory=(
            "You are a senior data scientist at Super Electric. You excel at taking "
            "raw energy data, running complex linear programming solvers, and extracting "
            "the core financial value (savings) for commercial microgrids."
        ),
        verbose=True,
        allow_delegation=False,
        llm=gemini_model, 
        tools=[run_battery_optimization]
    )

    customer_support = Agent(
        role='Client Communications Manager',
        goal='Translate complex energy math into simple, pedagogical emails for facility managers.',
        backstory=(
            "You work in Super Electric's internal customer support hub. Your job is to "
            "take technical reports from the engineering team and draft polite, clear, and "
            "encouraging emails to clients explaining how much money the AI is saving them. "
            "You avoid dense jargon and focus on data storytelling."
        ),
        verbose=True,
        allow_delegation=False,
        llm=gemini_model  
    )

    # --- Define the Tasks ---

    analyze_grid_task = Task(
        description=(
            "Use the Battery Optimization Tool to calculate the energy savings for tomorrow. "
            "Extract the original cost, the optimized cost, and the strategy used."
        ),
        expected_output="A short technical summary of the energy costs and the charging strategy.",
        agent=energy_analyst
    )

    draft_email_task = Task(
        description=(
            "Read the technical summary provided by the Energy Analyst. Draft a professional "
            "email to the client (Mr. Davis, the Facility Manager). Explain the savings we achieved "
            "for tomorrow by automatically avoiding the afternoon peak pricing. Ensure the tone is "
            "helpful, pedagogical, and clearly demonstrates the ROI of our microgrid AI."
        ),
        expected_output="A client-ready email draft.",
        agent=customer_support
    )

    # --- Assemble and Run the Crew ---
    
    microgrid_crew = Crew(
        agents=[energy_analyst, customer_support],
        tasks=[analyze_grid_task, draft_email_task],
        process=Process.sequential, 
        verbose=True
    )

    print("Starting Autonomous Agentic Workflow...")
    result = microgrid_crew.kickoff()
    
    print("\n==================================================")
    print("FINAL OUTPUT (Internal Customer Support Email):")
    print("==================================================\n")
    print(result)

if __name__ == "__main__":
    run_agentic_workflow()