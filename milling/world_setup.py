# [forward_speed_if_seen, turning_speed_if_seen, forward_speed_if_not_seen, turning_speed_if_not_seen]

from swarmsim.world.RectangularWorld import RectangularWorld, RectangularWorldConfig
from swarmsim.agent.MazeAgent import MazeAgent, MazeAgentConfig
from swarmsim.world.simulate import main as sim
from swarmsim.agent.control.BinaryController import BinaryController
from swarmsim.world.spawners.AgentSpawner import PointAgentSpawner
from swarmsim.metrics.Circliness import Circliness
from swarmsim.sensors.BinaryFOVSensor import BinaryFOVSensor


def simulate(speeds: list, steps: int = 1000, show=False) -> float:
    world_config = RectangularWorldConfig(
        size=[10,10],time_step=1/40,
        stop_at=steps
    )
    world = RectangularWorld(world_config)

    agent_config = MazeAgentConfig(position=(5,5), agent_radius=0.1)
    agent = MazeAgent(agent_config, world)

    sensor = BinaryFOVSensor(agent=agent,theta=0.45,distance=2.0,false_positive=0.0,false_negative=0.0,show=False)
    agent.sensors.append(sensor)

    # A = v,w when not seen B = v, when seen
    a = (speeds[2], speeds[3])
    b = (speeds[0], speeds[1])
    controller = BinaryController(a, b)
    agent.controller = controller


    # spawner = DonutAgentSpawner(world, n=6, facing="away",avoid_overlap=True, agent=agent, mode="oneshot")
    # Donut spawner doesn't work / is outdated!!

    spawner = PointAgentSpawner(world, n=6, facing="away",avoid_overlap=True, agent=agent, mode="oneshot")

    world.spawners.append(spawner)

    world.metrics = [Circliness(history=steps)]
    sim(
            world,
            show_gui=show,
        )
    return float(world.metrics[0].average)





# Average circliness longer 
# Use Binary Controller 
# Neuro Evolution - Note just considering some fixed number of ways but rather evolving some kind of graph 
# Library needs to suport Neuro Evolution 
# NEAT is one of the libraries that currently support that 
# Neural Architecture search 
# Future definition of operators such as adding a nueron