import batch_midi as bm
import numpy as np
import superdirtpy as sd

rng = np.random.default_rng()
client = sd.SuperDirtClient()
# client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "superpiano", "amp": 0.8, "octave": 0}

dt = 0.3
dt_next_iter = 0.05
n_iter = 100

size = 10
vel = 1.0
n_agent = 20
range_separate = 1
range_alignment = 5


class Boids:
    def __init__(self) -> None:
        self.agent = []
        for _ in range(n_agent):
            p = rng.uniform(-size, size, 2)
            v = rng.uniform(-vel, vel, 2)
            self.agent += [{"p": p, "v": v}]
        self.dist = np.zeros([n_agent, n_agent])

    def distance(self):
        for i in range(n_agent):
            for j in range(n_agent):
                d = self.agent[i]["p"] - self.agent[j]["p"]
                self.dist[i][j] = np.linalg.norm(d)

    def rule_separate(self, i):
        v = np.zeros(2)
        a = np.where(self.dist[i] < range_separate)[0]
        if len(a) == 0:
            return v
        for j in a:
            if i == j:
                continue
            d = self.agent[i]["p"] - self.agent[j]["p"]
            v += d / self.dist[i][j] ** 2
        return v / len(a)

    def rule_alignment(self, i):
        v = np.zeros(2)
        a = np.where(self.dist[i] < range_alignment)[0]
        if len(a) == 0:
            return v
        for j in a:
            v -= self.agent[i]["v"] - self.agent[j]["v"]
        return v / len(a)

    def rule_cohesion(self, i):
        v = np.zeros(2)
        for j in range(n_agent):
            v -= self.agent[i]["p"] - self.agent[j]["p"]
        return v / n_agent

    def simulation(self):
        self.distance()
        v_tmp = []
        for i in range(n_agent):
            v_tmp += [self.rule_separate(i) * 0.5 + self.rule_alignment(i) * 0.6 + self.rule_cohesion(i) * 0.4]

        for i in range(n_agent):
            self.agent[i]["v"] += v_tmp[i]
            v = np.linalg.norm(self.agent[i]["v"])
            if v > vel:
                self.agent[i]["v"] = self.agent[i]["v"] / v * vel
            elif v < vel / 2:
                self.agent[i]["v"] = self.agent[i]["v"] / v * vel / 2

        for i in range(n_agent):
            if abs((self.agent[i]["p"] + self.agent[i]["v"])[0]) > size:
                self.agent[i]["v"][0] = -self.agent[i]["v"][0]
            if abs((self.agent[i]["p"] + self.agent[i]["v"])[1]) > size:
                self.agent[i]["v"][1] = -self.agent[i]["v"][1]
            self.agent[i]["p"] += self.agent[i]["v"]


def scale_pitch(y: float) -> int:
    y = (y + size) / (size * 2)
    y = (y * (127 - 48)) + 24
    return int(y)


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)

    b = Boids()
    for _ in range(n_iter):
        b.simulation()

        points = [(a["p"][0], a["p"][1]) for a in b.agent]
        points = sorted(points, key=lambda p: p[0])

        n = [scale_pitch(p[1]) for p in points]
        delta = np.diff([p[0] * dt for p in points]).tolist()
        delta.append(dt_next_iter)

        params = p | {
            "n": n,
            "delta": delta,
            "sustain": 1.5,
        }
        sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/")
