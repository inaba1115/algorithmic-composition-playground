import batch_midi as bm
import superdirtpy as sd

client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "superpiano", "amp": 0.7, "octave": 4}
bpm = 90
dt = round(60 / bpm, 4)

novel = """\
One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. \
He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. \
The bedding was hardly able to cover it and seemed ready to slide off any moment. \
His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. \
"""


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)
    scale = sd.Scale(sd.PitchClass.Fs, sd.Scales.messiaen3)

    for word in novel.split():
        xs = [
            ord(x.lower()) - ord("a") for x in word if ord("A") <= ord(x) <= ord("Z") or ord("a") <= ord(x) <= ord("z")
        ]
        params = p | {
            "n": [scale.bind(list(set(xs)))],
            "delta": dt,
        }
        sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
