# [forward_speed_if_seen, turning_speed_if_seen, forward_speed_if_not_seen, turning_speed_if_not_seen]

from swarmsim.world.RectangularWorld import RectangularWorld, RectangularWorldConfig
from swarmsim.agent.MazeAgent import MazeAgent, MazeAgentConfig
from swarmsim.world.simulate import main as sim
from swarmsim.agent.control.Controller import AbstractController
from swarmsim.world.spawners.DonutSpawner import DonutAgentSpawner
from swarmsim.world.spawners.AgentSpawner import PointAgentSpawner
from swarmsim.metrics.Circliness import Circliness
from swarmsim.sensors.BinaryFOVSensor import BinaryFOVSensor


class milling(AbstractController):
    def __init__(self, parent=None, speeds: list=None):
        super().__init__(parent)
        self.speeds=speeds

    
    def get_actions(self, agent):
        if agent.agent_in_sight:
            return self.speeds[0], self.speeds[1]
        else:
            return self.speeds[2], self.speeds[3] 
    

def simulate(speeds: list, steps: int = 100) -> float:
    world_config = RectangularWorldConfig(size=[10,10],time_step=1/40)
    world = RectangularWorld(world_config)

    agent_config = MazeAgentConfig(position=(5,5), agent_radius=0.1) 
    agent = MazeAgent(agent_config, world)

    sensor = BinaryFOVSensor(agent=agent,theta=0.45,distance=2.0,false_positive=0.0,false_negative=0.0,show=False)
    agent.sensors.append(sensor)

    controller = milling(agent, speeds)
    agent.controller = controller


    # spawner = DonutAgentSpawner(world, n=6, facing="away",avoid_overlap=True, agent=agent, mode="oneshot")
    # Donut spawner doesn't work / is outdated!!

    spawner = PointAgentSpawner(world, n=6, facing="away",avoid_overlap=True, agent=agent, mode="oneshot")
    
    world.spawners.append(spawner) 

    circliness = Circliness(history=steps)
    circliness.attach_world(world)
    circliness.reset()
    world.metrics.append(circliness)

    for _ in range(steps):
        world.step()

    return float(circliness.average)
