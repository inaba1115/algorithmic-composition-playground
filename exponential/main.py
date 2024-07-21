import batch_midi as bm
import numpy as np
import superdirtpy as sd

rng = np.random.default_rng()
client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "super808", "amp": 0.8, "octave": 0}
lamb = 5
size = 100
dt = 0.3


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)

    for _ in range(30):
        t_interval = rng.exponential(scale=1 / lamb, size=size) * dt

        params = p | {
            "n": rng.integers(128, size=len(t_interval)).tolist(),
            "delta": t_interval.tolist(),
            "sustain": 1,
            "room": 0.5,
        }
        sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
