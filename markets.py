import numpy as np
import vectorbt as vbt
from numpy.typing import NDArray

# gene and genome definition 
Gene = np.int16
Genome = NDArray[Gene]

#initialize data to S&P 500 
price = vbt.YFData.download('^GSPC').get('Close')

# fast_window and slow_window can only contain numbers from 1 through 1000
GENE_VALUES = np.arange(1, 250, dtype=Gene)

# initialization of population size and genetic operator specifications 
POP_COUNT: int = 100
GEN_COUNT: int = 20
START_CASH = 100
DUP_RATE: float = 0.1 
DUP_COUNT = int(DUP_RATE * POP_COUNT)
MUT_RATE: float = 0.05

# helper methods 
def compute_fitness(population: Genome) -> np.array:
    fitness = np.array([])
    for fast_window, slow_window in population:

        # Make sure imposible strategy doesn't crash vector
        if fast_window <= 0 or slow_window <= 0:
            fitness = np.append(fitness, -np.inf)
            continue
        if fast_window >= slow_window:
            fitness = np.append(fitness, -np.inf)
            continue

        fast_ma = vbt.MA.run(price, fast_window)
        slow_ma = vbt.MA.run(price, slow_window) 
        entries = fast_ma.ma_crossed_above(slow_ma)
        exits = fast_ma.ma_crossed_below(slow_ma) 
        pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=START_CASH)
        fitness_value = pf.total_return() - abs(pf.max_drawdown())
        fitness = np.append(fitness, fitness_value)
    return fitness


def main():
    rng = np.random.default_rng(99) 
    population = rng.choice(GENE_VALUES, size = (POP_COUNT, 2)).astype(Gene)
    epoch: int = 0
    best_fit: float = -np.inf 
    best_genome: Genome = np.array([])
    # training loop 
    while epoch < GEN_COUNT:
        if epoch % 1 == 0:
            print(f"Best Genome: {best_genome} | Best Fitness: {best_fit}")

        # fitness calc
        fitness = compute_fitness(population)

        # sort by fittness 
        indices = np.argsort(fitness)[::-1]
        population = population[indices]
        fitness = fitness[indices]
        if fitness[0] > best_fit:
            best_fit = fitness[0]
            best_genome = population[0] 

        new_population = np.zeros_like(population)

        # duplication 
        new_population[:DUP_COUNT] = population[:DUP_COUNT]

        #crossover
        for i in range(POP_COUNT - DUP_COUNT):
            p1, p2 = rng.choice(population[:DUP_COUNT + 10], size=2, replace=False)
            new_population[i,0] = p1[0]
            new_population[i,1] = p2[1]

        # muatation
        mut_mask = rng.random(size=new_population.shape) < MUT_RATE
        top_n = 3
        mut_mask[:top_n:, :] = False

        random_genes = rng.choice(GENE_VALUES, size=new_population.shape)

        population = np.where(mut_mask, random_genes, new_population)

        epoch += 1
    
    print(f"Completed {epoch} epochs! | Final: {best_genome} | Fitness: {best_fit}")

if __name__ == "__main__":
    main()












    
