from world_setup import simulate

def main():
    #TODO: Add in some file loading system

    # Result after 280 epochs: Final: [ 0.23 -0.05  0.1  -0.17]; fitness = 0.5449154775816047
    best = [0.23, -0.05,  0.1, -0.17]

    simulate(best, show=True)


if __name__ == "__main__":
    main()
