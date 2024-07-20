from datetime import timedelta

import batch_midi as bm
import numpy as np
import superdirtpy as sd

rng = np.random.default_rng()
client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "super808", "amp": 0.8, "octave": 0}
dt = 10
size = 100


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)

    for _ in range(6):
        now = tctx.now()
        sample = rng.exponential(scale=dt, size=size)
        delta = np.diff(sorted(sample[sample < dt])).tolist()

        params = p | {
            "n": rng.integers(128, size=len(delta)).tolist(),
            "delta": delta,
            "sustain": 1,
            "room": 0.5,
        }
        sd.Pattern(client=client, params=params).play(tctx)

        tctx.set_now(now + timedelta(seconds=dt))


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
