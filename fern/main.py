import batch_midi as bm
import numpy as np
import superdirtpy as sd

rng = np.random.default_rng()
client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "superpiano", "amp": 0.8, "octave": 0}

f1 = lambda _, y: (0.0, 0.16 * y)
f2 = lambda x, y: (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6)
f3 = lambda x, y: (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6)
f4 = lambda x, y: (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44)
fs = [f1, f2, f3, f4]

num = 10000
dt = 30


def main():
    points = []
    x, y = 0, 0
    for _ in range(num):
        points.append((x, y))
        f = rng.choice(fs, p=[0.01, 0.85, 0.07, 0.07])
        x, y = f(x, y)

    xs = [p[0] for p in points]
    min_x = min(xs)
    max_x = max(xs)

    ys = [p[1] for p in points]
    min_y = min(ys)
    max_y = max(ys)

    points = [(int(sd.zmap(p[0], min_x, max_x, 0, 127)), sd.zmap(p[1], min_y, max_y, 0, 1) * dt) for p in points]

    points = sorted(points, key=lambda p: p[1])
    n = [p[0] for p in points]
    ts = [p[1] for p in points]
    delta = np.diff(ts).tolist()

    tctx = sd.TemporalContext(dryrun=dryrun)
    params = p | {
        "n": n,
        "delta": delta,
        "sustain": 1,
    }
    sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
