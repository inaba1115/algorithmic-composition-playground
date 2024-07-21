import batch_midi as bm
import superdirtpy as sd

client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "superpiano", "amp": 0.3, "octave": 4}
bpm = 105
dt = round(60 / bpm / 2, 4)


def fifth_mode(scale: list[int]) -> list[int]:
    return sorted([(x - 7) % 12 for x in scale])


def main():
    phrygian = fifth_mode(sd.Scales.minor)
    phrygian_dominant = fifth_mode(sd.Scales.harmonic_minor)
    mixolydian_b6 = fifth_mode(sd.Scales.melodic_minor)

    fs_phrygian = sd.Scale(sd.PitchClass.Fs, phrygian)
    fs_phrygian_dominant = sd.Scale(sd.PitchClass.Fs, phrygian_dominant)
    fs_mixolydian_b6 = sd.Scale(sd.PitchClass.Fs, mixolydian_b6)

    fs_min = fs_phrygian.bind([0, 2, 4])
    fs_add_b9 = fs_phrygian.bind([0, 2, 4, 8])
    g_maj = fs_phrygian.bind([1, 3, 5])
    g_maj7 = fs_phrygian.bind([1, 3, 5, 7])
    a_6 = fs_phrygian.bind([2, 4, 6, 7])
    fs_maj = fs_phrygian_dominant.bind([0, 2, 4])
    e_add9 = fs_mixolydian_b6.bind([-1, 1, 3, 7])

    tctx = sd.TemporalContext(dryrun=dryrun)

    n = [fs_maj, fs_maj, g_maj7, a_6, a_6]
    n += [a_6, g_maj7, g_maj7, g_maj, g_maj]
    n += [fs_add_b9, fs_maj, g_maj7, a_6, a_6]
    n += [a_6, g_maj7, g_maj7, g_maj7, g_maj7]

    for _ in range(2):
        params = p | {
            "n": n,
            "delta": [x * dt for x in [3, 3, 4, 3, 3]],
        }
        sd.Pattern(client=client, params=params).play(tctx)

    n = [fs_maj, fs_maj, g_maj7, a_6, a_6]
    n += [a_6, g_maj7, g_maj7, fs_maj, fs_maj]
    n += [fs_min, fs_min, e_add9, e_add9, e_add9]
    n += [g_maj7, g_maj7, g_maj7, g_maj7, g_maj7]

    for _ in range(4):
        params = p | {
            "n": n,
            "delta": [x * dt for x in [3, 3, 4, 3, 3]],
        }
        sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
