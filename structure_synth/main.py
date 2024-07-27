import batch_midi as bm
import numpy as np
import superdirtpy as sd

rng = np.random.default_rng()
client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "superpiano", "octave": 4}
bpm = 130
dt = round(60 / bpm / 4, 4)
scale = sd.Scale(sd.PitchClass.C, sd.Scales.messiaen3)


def r1(tctx: sd.TemporalContext, degrees: list[int], a: int, dt: float, amp: float, i: int = 0) -> None:
    if i >= 30:
        return

    params = p | {
        "n": scale.bind([x + a for x in degrees]),
        "delta": dt,
        "amp": amp,
    }
    sd.Pattern(client=client, params=params).play(tctx)

    r1(tctx, degrees, a + rng.choice([-2, 2]), dt * 0.9, min(amp * 1.05, 1), i + 1)


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)

    for i in range(8):
        r1(tctx, list(range(0, (i + 1) * 2, 2)), i * 2, dt, 0.4)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
