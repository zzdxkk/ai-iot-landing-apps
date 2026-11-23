"""智慧水务边缘监测：传感器采样 -> 低功耗策略 -> 边缘异常检测 -> NB-IoT 上报。AI+IoT 融合。"""
import random, math
from collections import deque

class SensorSim:
    def __init__(self, base=25.0): self.base = base; self.t = 0
    def sample(self):
        self.t += 1
        drift = math.sin(self.t / 8) * 0.6
        spike = 8.0 if self.t % 17 == 0 else 0.0   # 周期性异常
        return round(self.base + drift + random.uniform(-0.3, 0.3) + spike, 2)

class LowPowerPolicy:
    """电池供电设备的休眠/唤醒策略：按周期与唤醒时长估算占空比。"""
    def __init__(self, period=600, wake_s=5): self.period, self.wake_s = period, wake_s
    def duty_cycle(self): return round(self.wake_s / self.period, 6)

class EWMA:
    """指数加权移动平均做边缘异常检测，无需云端即可发现突变。"""
    def __init__(self, alpha=0.3, k=2.5): self.alpha, self.k = alpha, k; self.mean = None; self.var = 1.0
    def update(self, x):
        if self.mean is None: self.mean = x; return False
        diff = x - self.mean
        sd = math.sqrt(self.var) or 1e-6
        is_anomaly = abs(diff) > self.k * sd
        self.mean += self.alpha * diff
        self.var = (1 - self.alpha) * (self.var + self.alpha * diff * diff)
        return is_anomaly

def report(device, value, alert):
    return {"device": device, "flow": value, "alert": alert,
            "payload_size": len(f"{value:.2f},{int(alert)}")}

if __name__ == "__main__":
    s, det, lp = SensorSim(), EWMA(), LowPowerPolicy()
    sent = 0
    for i in range(25):
        v = s.sample(); ab = det.update(v)
        if ab or i % 5 == 0:
            pkt = report("water-001", v, ab); sent += 1
            print(pkt)
    print("占空比:", lp.duty_cycle(), "上报次数:", sent)
