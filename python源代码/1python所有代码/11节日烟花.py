import math, random , time
import threading
import tkinter as tk
import re


Fireworks = []
maxFireworks = 8
height, width =600, 600


class firework(object):
    def __init__(self, color, speed, width, height):
        self.radius = random.randint(2, 4)
        self.color = color
        self.speed = speed
        self.status = 0
        self.nParticle = random.randint(20, 30)
        self.center = [random.randint(0, width - 1), random.randint(0, height - 1)]
        self.oneParticle = []
        self.rotTheta = random.uniform(0, 2 * math.pi)

        self.ellipsePara = [random.randint(30, 40), random.randint(20, 30)]
        theta = 2 * math.pi / self.nParticle
        for i in range(self.nParticle):
            t = random.uniform(-1.0 / 16, 1.0 / 16)
            x, y = self.ellipsePara[0] * math.cos(theta * i + t), self.ellipsePara[1] * math.sin(
                theta * i + t)
            xx, yy = x * math.cos(self.rotTheta) - y * math.sin(self.rotTheta), y * math.cos(
                self.rotTheta) + x * math.sin(self.rotTheta)
            self.oneParticle.append([xx, yy])

        self.curParticle = self.oneParticle[0:]
        self.thread = threading.Thread(target=self.extend)

    def extend(self):
        for i in range(100):
            self.status += 1
            self.curParticle = [[one[0] * self.status / 100, one[1] * self.status / 100] for one in
                                self.oneParticle]
            time.sleep(self.speed / 50)

    def explode(self):
        self.thread.setDaemon(True)
        self.thread.start()

    def __repr__(self):
        return ('color:{color}\n'
                'speed:{speed}\n'
                'number of particle: {np}\n'
                'center:[{cx} , {cy}]\n'
                'ellipse:a={ea} , b={eb}\n'
                'particle:\n{p}\n'
                ).format(color=self.color, speed=self.speed, np=self.nParticle, cx=self.center[0], cy=self.center[1],
                         p=str(self.oneParticle), ea=self.ellipsePara[0], eb=self.ellipsePara[1])


def colorChange(fire):
    rgb = re.findall(r'(.{2})', fire.color[1:])
    cs = fire.status

    f = lambda x, c: hex(int(int(x, 16) * (100 -c) / 30))[2:]
    if cs > 70:
        ccr, ccg, ccb = f(rgb[0], cs), f(rgb[1], cs), f(rgb[2], cs)
    else:
        ccr, ccg, ccb = rgb[0], rgb[1], rgb[2]

    return '#{0:0>2}{1:0>2}{2:0>2}'.format(ccr, ccg, ccb)


def appendFirework(n=1):
    if n > maxFireworks or len(Fireworks) > maxFireworks:
        pass
    elif n == 1:
        cl = '#{0:0>6}'.format(
            hex(int(random.randint(0, 16777215)))[2:])
        a = firework(cl, random.uniform(1.5, 3.5), width, height)
        Fireworks.append(
            {'particle': a, 'points': []})
        a.explode()
    else:
        appendFirework()
        appendFirework(n - 1)


def show(c):
    for p in Fireworks:
        for pp in p['points']:
            c.delete(pp)

    for p in Fireworks:
        oneP = p['particle']
        if oneP.status == 100:
            Fireworks.remove(p)
            appendFirework()
            continue
        else:
            li = [[int(cp[0] * 2) + oneP.center[0], int(cp[1] * 2) + oneP.center[1]] for cp in
                  oneP.curParticle]
            color = colorChange(oneP)
            for pp in li:
                p['points'].append(
                    c.create_oval(pp[0] - oneP.radius, pp[1] - oneP.radius, pp[0] + oneP.radius, pp[1] + oneP.radius,
                                  fill=color))

    root.after(50, show, c)


if __name__ == '__main__':
    appendFirework(maxFireworks)

    root = tk.Tk()
    cv = tk.Canvas(root, height=height, width=width)
    cv.create_rectangle(0, 0, width, height, fill="black")

    cv.pack()

    root.after(50, show, cv)
    root.mainloop()