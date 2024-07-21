import math

import batch_midi as bm
import superdirtpy as sd

client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "superpiano", "amp": 0.8, "octave": 0}
bpm = 444
dt = round(60 / bpm / 4, 4)


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)

    for i in range(128 * 4):
        n1 = [(x + i) % 128 for x in [0, 12, 24, 36]]
        n2 = [127 - x for x in n1]
        params = p | {
            "n": [n1 + n2],
            "delta": dt,
        }
        sd.Pattern(client=client, params=params).play(tctx)

    for i in range(128 * 4):
        params = p | {
            "n": [list(range(i % 128))],
            "delta": (math.sqrt(127 - (i % 128)) / math.sqrt(127)) * dt / 4,
        }
        sd.Pattern(client=client, params=params).play(tctx)

    for i in range(128 * 4):
        params = p | {
            "n": [list(range(127 - (i % 128), 128))],
            "delta": (math.sqrt(127 - (i % 128)) / math.sqrt(127)) * dt / 4,
        }
        sd.Pattern(client=client, params=params).play(tctx)

    for i in range(128 * 8):
        params = p | {
            "n": [list(range(i % 128))],
            "delta": (math.sqrt(127 - (i % 128)) / math.sqrt(127)) * dt / 8,
        }
        sd.Pattern(client=client, params=params).play(tctx)

    for i in range(128 * 8):
        params = p | {
            "n": [list(range(127 - (i % 128), 128))],
            "delta": (math.sqrt(127 - (i % 128)) / math.sqrt(127)) * dt / 8,
        }
        sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
