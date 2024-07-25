import batch_midi as bm
import superdirtpy as sd

client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "mydevice", "midichan": 0, "octave": 3, "amp": 0.8}
bpm = 150
dt = round(60 / bpm / 4, 4)


def m(k: int, n: int, o: int, r: int) -> str:
    a, b = n // k, n % k
    return (_m(b) + sd.euclid(o, k - b, r)) * a + _m(b)


def _m(size: int) -> str:
    if size < 1:
        return ""
    return "x" + "." * (size - 1)


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)

    for _ in range(4):
        bd = [0] * 128
        sn = [{"x": 2}.get(x) for x in sd.euclid(47, 128)]
        ho = [10, None, None, None] * 32

        params = p | {
            "n": [list(x) for x in zip(bd, sn, ho)],
            "delta": dt,
        }
        sd.Pattern(client=client, params=params).play(tctx)

    for i in range(4):
        for j in [1, 2]:
            for k in [23, 19, 17, 22]:
                bd = [{"x": 0}.get(x) for x in sd.euclid(k, 32)]
                sn = [{"x": 2}.get(x) for x in m(5, 32, j, i)]
                ho = [10, None, None, None] * 8

                params = p | {
                    "n": [list(x) for x in zip(bd, sn, ho)],
                    "delta": dt,
                }
                sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
