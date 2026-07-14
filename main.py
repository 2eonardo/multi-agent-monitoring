import sys
from environment import Map
from agent import Agent
import costants as c
import plots as p

def main():
    #Load map
    try:
        m = Map("sea_land_mask_10m_Cecina.npz")
        print("Map successfully loaded")
    except FileNotFoundError:
        print("Error: Map file not found.")
        sys.exit()

    #Load agents
    fleet= []
    for i in range(c.NUM_AGENTS):
        try:
            new_agent =Agent(
                start_row=c.START_ROW,
                start_col=c.START_COL,
                map_reference=m,
                sensor_range=c.SENSOR_RANGE,
                max_displacement=c.MAX_DISPLACEMENT
            )
            fleet.append(new_agent)
        except ValueError as e:
            print(f"Dettaglio: {e}")
            sys.exit()
    print(f"{len(fleet)} Agents successfully loaded")

    print("Starting simulation...")
    m.update_coverage_value()

    coverage_history = [m.coverage_value]
    print("Iteration: ", 0)
    print(f"Coverage value 0: {m.coverage_value}")

    for t in range(1, c.NUM_ITERATIONS+1):
        m.decay(c.DECAY_RATE)
        for agent in fleet:
            agent.update_position(c.NUM_SAMPLES, fleet)

        coverage_history.append(m.coverage_value)
        print("Iteration: ", t)
        print(f"Coverage value {t}: {m.coverage_value}")

    p.save_coverage_table(coverage_history,c.ITERATIONS_STEP)

    print("\nSimulation completed.")

if __name__ == "__main__":
    main()