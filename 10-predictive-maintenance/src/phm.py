"""设备预测性维护：振动时序 -> 特征工程 -> 健康评分 -> 剩余寿命(RUL)预测。工业AI典型落地。"""
import math, random
from collections import deque

def rms(xs): return math.sqrt(sum(x*x for x in xs)/len(xs)) if xs else 0.0
def peak(xs): return max((abs(x) for x in xs), default=0.0)
def kurtosis(xs):
    if not xs: return 0.0
    m = sum(xs)/len(xs); v = sum((x-m)**2 for x in xs)/len(xs) or 1e-9
    return sum((x-m)**4 for x in xs)/len(xs)/(v*v)

def features(window): return {"rms": round(rms(window),3), "peak": round(peak(window),3),
                              "kurtosis": round(kurtosis(window),3)}

def health_score(f, base_rms=1.0):
    r = f["rms"]/base_rms
    score = 100 * math.exp(-0.4*max(0, r-1))
    return round(max(0, min(100, score)), 1)

def rul(score, decline=0.5):
    """粗略剩余寿命（周期数），健康分越低剩余越短。"""
    return max(0, int((score - 20) / decline))

class VibrationSim:
    def __init__(self): self.t = 0
    def sample(self):
        self.t += 1
        wear = min(3.0, self.t/40)   # 逐渐磨损
        return random.gauss(0, 0.3) * (1 + wear*0.5) + wear*0.2

def monitor(steps=100, win=20):
    sim, buf, out = VibrationSim(), deque(maxlen=win), []
    for _ in range(steps):
        buf.append(sim.sample())
        if len(buf) == win:
            f = features(list(buf)); s = health_score(f); out.append((f, s, rul(s)))
    return out

if __name__ == "__main__":
    res = monitor()
    print("样本数:", len(res))
    print("初期:", res[0])
    print("末期:", res[-1])
    print("健康度趋势:", [s for _, s, _ in res[::20]])
