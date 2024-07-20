import batch_midi as bm
import numpy as np
import superdirtpy as sd

rng = np.random.default_rng()
client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "superpiano", "amp": 0.8, "octave": 0}


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)
    scale = sd.Scale(sd.PitchClass.D, sd.Scales.bartok)
    cluster = [x for x in range(128) if x % 12 in scale.degrees()]

    for _ in range(100):
        low, high = sorted(rng.choice(128, size=2, replace=False))
        num = 2 ** rng.integers(8)
        _, step = np.linspace(0, 1, num=num, endpoint=False, retstep=True)

        params = p | {
            "n": [[x for x in cluster if low <= x <= high]],
            "delta": [step] * num,
        }
        sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
