import batch_midi as bm
import superdirtpy as sd

client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "mydevice", "midichan": 0, "octave": 3, "amp": 0.8}
bpm = 150
dt = round(60 / bpm / 4, 4)


def m(k: int, n: int, r: int = 0) -> str:
    a = n // k
    b = n % k
    mb = _m(b)
    return (mb + sd.euclid(int((k - b) * 0.5), k - b, r)) * a + mb


def _m(size: int) -> str:
    if size < 1:
        return ""
    return "x" + "." * (size - 1)


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)

    for _ in range(4):
        for i in [5, 7, 11, 13]:
            for j in range(4):
                p1 = sd.euclid(7, 32, j)
                p2 = m(i, 32, -j)
                p3 = sd.euclid(2, 8, j) * 4

                bd = [{"x": 0}.get(x) for x in p1]
                sn = [{"x": 2}.get(x) for x in p2]
                hc = [{"x": 6}.get(x) for x in p3]

                params = p | {
                    "n": [list(x) for x in zip(bd, sn, hc)],
                    "delta": dt,
                }
                sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
