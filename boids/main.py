import batch_midi as bm
import numpy as np
import superdirtpy as sd

rng = np.random.default_rng()
# client = sd.SuperDirtClient()
client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "superpiano", "amp": 0.8, "octave": 0}

SIZE = 10
VEL = 1.0
AGENT = 20
RANGE_Separate = 1
RANGE_Alignment = 5


class Boids:
    def __init__(self) -> None:
        self.agent = []
        for _ in range(AGENT):
            pos = rng.uniform(-SIZE, SIZE, 2)
            vel = rng.uniform(-VEL, VEL, 2)
            self.agent += [{"p": pos, "v": vel}]
        self.dist = np.zeros([AGENT, AGENT])

    def distance(self):
        for i in range(AGENT):
            for j in range(AGENT):
                d = self.agent[i]["p"] - self.agent[j]["p"]
                self.dist[i][j] = np.linalg.norm(d)

    def rule_separate(self, n):
        a = np.array(np.where(self.dist[n] < RANGE_Separate), dtype=int)[0]
        v = np.zeros(2)
        cnt = 0
        for i in a:
            if i != n:
                d = self.agent[n]["p"] - self.agent[i]["p"]
                v += d / (self.dist[n][i] * self.dist[n][i])
                cnt += 1
        if cnt == 0:
            return 0
        return v / cnt

    def rule_alignment(self, n):
        a = np.array(np.where(self.dist[n] < RANGE_Alignment), dtype=int)[0]
        v = np.zeros(2)
        cnt = 0
        for i in a:
            v -= self.agent[n]["v"] - self.agent[i]["v"]
            cnt += 1
        return v / cnt

    def rule_cohesion(self, n):
        p = np.zeros(2)
        for i in range(AGENT):
            p -= self.agent[n]["p"] - self.agent[i]["p"]
        return p / AGENT

    def simulation(self):
        self.distance()
        vel_tmp = []
        for i in range(AGENT):
            vel_tmp += [self.rule_separate(i) * 0.5 + self.rule_alignment(i) * 0.6 + self.rule_cohesion(i) * 0.4]

        for i in range(AGENT):
            self.agent[i]["v"] += vel_tmp[i]
            v = np.linalg.norm(self.agent[i]["v"])
            if v > VEL:
                self.agent[i]["v"] = self.agent[i]["v"] / v * VEL
            elif v < VEL / 2:
                self.agent[i]["v"] = self.agent[i]["v"] / v * VEL / 2

        for i in range(AGENT):
            if abs((self.agent[i]["p"] + self.agent[i]["v"])[0]) > SIZE:
                self.agent[i]["v"][0] = -self.agent[i]["v"][0]
            if abs((self.agent[i]["p"] + self.agent[i]["v"])[1]) > SIZE:
                self.agent[i]["v"][1] = -self.agent[i]["v"][1]
            self.agent[i]["p"] += self.agent[i]["v"]


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)

    b = Boids()
    for _ in range(100):
        b.simulation()

        tmp = []
        for i in range(AGENT):
            tmp.append((b.agent[i]["p"][0], b.agent[i]["p"][1]))
        tmp = sorted(tmp, key=lambda p: p[0])

        n = [int((x[1] + 10) / 20 * 127) for x in tmp]
        delta: list[float] = np.diff([x[0] for x in tmp]).tolist()
        delta.append(1)

        print(len(n))
        print(len(delta))

        params = p | {
            "n": n,
            "delta": delta,
            "sustain": 1,
        }
        sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
