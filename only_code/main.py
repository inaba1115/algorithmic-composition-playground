import numpy as np
import superdirtpy as sd

rng = np.random.default_rng()
client = sd.SuperDirtClient()
p = {"s": "test"}


def main():
    tctx = sd.TemporalContext()

    while True:
        params = p | {
            "n": rng.choice(12, size=8).tolist(),
            "delta": 0.08,
        }
        sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
