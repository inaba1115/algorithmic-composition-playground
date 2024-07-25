import batch_midi as bm
import superdirtpy as sd

client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "mydevice", "midichan": 0, "octave": 3, "amp": 0.8}
bpm = 150
dt = round(60 / bpm / 4, 4)


def m(k: int, n: int) -> str:
    a, b = n // k, n % k
    return (_m(b) + _m(k - b)) * a + _m(b)


def _m(size: int) -> str:
    if size < 1:
        return ""
    return "x" + "." * (size - 1)


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)

    for _ in range(4):
        for i in [5, 7, 11, 13]:
            for j in range(4):
                bd = [{"x": 0}.get(x) for x in sd.euclid(7, 32, j)]
                sn = [{"x": 2}.get(x) for x in m(i, 32)]
                hc = [{"x": 6}.get(x) for x in sd.euclid(2, 8, j) * 4]

                params = p | {
                    "n": [list(x) for x in zip(bd, sn, hc)],
                    "delta": dt,
                }
                sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
