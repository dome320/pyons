import numpy as np
from world_setup import simulate

from swarmsim.util.processing.multicoreprocessing import process_map

step = 0.01

V_MAX: float = 0.27
V_MIN: float = 0.05 # no reversing and avoiding zero or it will exploit static behavior as good circliness
V_VALUES = np.arange(V_MIN, V_MAX + step, step)

W_MAX: float = 0.60
W_MIN: float = -0.60
W_VALUES = np.arange(W_MIN, W_MAX + step, step)

POP_COUNT: int = 100
MAX_GEN_COUNT: int = 10000
DUP_RATE: float = 0.1
MUT_RATE: float = 0.05

# def fitness_individual(individual: list[float], target: float) -> float:
def fitness_individual(config: tuple[np.array, float]) -> float:
    individual, target = config
    fitness = simulate(individual)
    return target - fitness

def fitness_mp(pop_matrix: np.array, target: float) -> np.array:
    args = []
    for indiv in pop_matrix:
        args.append((indiv, target))

    # args = [(indiv, target) for indiv in pop_matrix]

    return np.array(process_map(fitness_individual, args))

def update_fitness(pop_matrix: np.array, target: float) -> np.array:
    fitness_values = []

    for l in pop_matrix:
        fitness = simulate(l)
        fitness_values.append(target - fitness)

    return np.array(fitness_values)



def main():
    rng = np.random.default_rng(99)
    target = 1.0 # perfect circliness metric
    pop_matrix = np.empty((POP_COUNT, 4))
    pop_matrix[:, [0, 2]] = rng.choice(V_VALUES, size=(POP_COUNT, 2))
    pop_matrix[:, [1, 3]] = rng.choice(W_VALUES, size=(POP_COUNT, 2))

    epoch: int = 0

    best_fit: float = np.inf
    best_genome = np.array([])
    try:
        while best_fit > 0 and epoch < MAX_GEN_COUNT:
            print(f"[ep. {epoch}] '{best_genome}'; fitness = {best_fit}")

            # fitness = update_fitness(pop_matrix, target)
            fitness = fitness_mp(pop_matrix, target)

            indices = np.argsort(fitness)
            pop_matrix = pop_matrix[indices]
            fitness = fitness[indices]
            if fitness[0] < best_fit:
                best_genome = pop_matrix[0]
                best_fit = fitness[0]

            new_pop_matrix = np.zeros_like(pop_matrix)

            dup_count = int(DUP_RATE * POP_COUNT)
            new_pop_matrix[:dup_count] = pop_matrix[:dup_count]

            for i in range(dup_count, POP_COUNT):
                p1, p2 = rng.choice(pop_matrix[:dup_count + 10], size=2, replace=False)
                split = rng.integers(1, 4)
                new_pop_matrix[i, :split] = p1[:split]
                new_pop_matrix[i, split:] = p2[split:]


            mut_mask = rng.random(size=new_pop_matrix.shape) < MUT_RATE
            top_n = 3
            mut_mask[:top_n:, :] = False


            random_genes = np.empty_like(new_pop_matrix)
            random_genes[:, [0, 2]] = rng.choice(V_VALUES, size=(POP_COUNT, 2))
            random_genes[:, [1, 3]] = rng.choice(W_VALUES, size=(POP_COUNT, 2))
            pop_matrix = np.where(mut_mask, random_genes, new_pop_matrix)
            epoch += 1

    except KeyboardInterrupt:
        print("Stopped Early by the user")

    print(f"Solved in {epoch} epochs! Final: {best_genome}; fitness = {best_fit}")

if __name__ == "__main__":
    main()
