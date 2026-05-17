import tkinter as tk, math, random
W, H = 600, 360
PW, PH, PX, PR = 10, 70, 14, 7
root = tk.Tk()
root.title("Pong")
cv = tk.Canvas(root, width=W, height=H, bg="white", highlightthickness=0)
cv.pack()
score_var = tk.StringVar(value="0 : 0")
tk.Label(root, textvariable=score_var, font=("Courier", 24, "bold")).pack(before=cv)
keys = set()
root.bind("<KeyPress>",   lambda e: keys.add(e.keysym))
root.bind("<KeyRelease>", lambda e: keys.discard(e.keysym))
py = ey = (H - PH) / 2
ey_vel = 0   
bx = by = vx = vy = 0
ps = es = 0
def spawn(d):
    global bx, by, vx, vy
    bx, by = W/2, H/2
    a = (random.random() - 0.5)
    vx = d * (3.8 + random.random() * 1.2)
    vy = math.sin(a) * 3
def hit(px, pady):
    return bx-PR < px+PW and bx+PR > px and by-PR < pady+PH and by+PR > pady
def bounce(pady, d):
    global vx, vy, bx
    rel = (by - (pady + PH/2)) / (PH/2)
    spd = min(math.hypot(vx, vy) * 1.05, 12)
    vx = d * abs(spd * math.cos(rel * 0.9))
    vy = spd * math.sin(rel * 0.9)
    bx = PX+PW+PR if d > 0 else W-PX-PW-PR
def loop():
    global py, ey, ey_vel, bx, by, vx, vy, ps, es
    if "w" in keys: py = max(0, py - 6)
    if "s" in keys: py = min(H-PH, py + 6)
    target = by - PH/2 + (random.random()-0.5) * 18
    target = max(0, min(H-PH, target))
    ey_vel += (target - ey) * 0.06  
    ey_vel *= 0.82                    
    ey_vel = max(-7, min(7, ey_vel))  
    ey = max(0, min(H-PH, ey + ey_vel))
    bx += vx; by += vy
    if by - PR < 0:  by = PR;    vy =  abs(vy)
    if by + PR > H:  by = H-PR;  vy = -abs(vy)
    if vx < 0 and hit(PX, py):        bounce(py, +1)
    if vx > 0 and hit(W-PX-PW, ey):   bounce(ey, -1)
    if bx < 0: es += 1; score_var.set(f"{ps} : {es}"); spawn(+1)
    if bx > W: ps += 1; score_var.set(f"{ps} : {es}"); spawn(-1)
    cv.delete("all")
    for y in range(0, H, 18):
        cv.create_rectangle(W//2-1, y, W//2+1, y+10, fill="#ddd", outline="")
    cv.create_rectangle(PX, py, PX+PW, py+PH, fill="black")
    cv.create_rectangle(W-PX-PW, ey, W-PX, ey+PH, fill="black")
    cv.create_oval(bx-PR, by-PR, bx+PR, by+PR, fill="black")
    root.after(16, loop)
spawn(1)
loop()
root.mainloop()