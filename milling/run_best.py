from world_setup import simulate

def main():
    #TODO: Add in some file loading system
    best = [0.27, -0.36,  0.1, -0.15]

    simulate(best, show=True)


if __name__ == "__main__":
    main()
