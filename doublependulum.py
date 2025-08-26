import torch
import pygame
import math
import colorsys
import numpy as np

def compute_derivatives(X):
    θ1, θ2, ω1, ω2 = X[:, 0], X[:, 1], X[:, 2], X[:, 3]

    delta = θ2 - θ1
    den1 = (m1 + m2) * l1 - m2 * l1 * torch.cos(delta)**2

    # Angular accelerations (ddθ1, ddθ2)
    a1 = (m2 * l1 * ω1**2 * torch.sin(delta) * torch.cos(delta)
          + m2 * g * torch.sin(θ2) * torch.cos(delta)
          + m2 * l2 * ω2**2 * torch.sin(delta)
          - (m1 + m2) * g * torch.sin(θ1)) / den1

    den2 = (l2 / l1) * den1

    a2 = (-m2 * l2 * ω2**2 * torch.sin(delta) * torch.cos(delta)
          + (m1 + m2) * (g * torch.sin(θ1) * torch.cos(delta)
          - l1 * ω1**2 * torch.sin(delta)
          - g * torch.sin(θ2))) / den2
    return torch.stack([ω1, ω2, a1, a2, torch.zeros_like(X[:, 0])], dim=1)

def compute_max(X):
    m = torch.max(torch.stack([torch.abs(X[:, 0]), torch.abs(X[:, 1]), X[:, 4]], dim=1), dim=1).values
    return torch.stack([X[:,0],X[:,1],X[:,2],X[:,3],m], dim=1)

def polar_color(x, y): # might've asked chat gpt to create this
    
    pi = torch.pi
    r = torch.hypot(x, y)  # radius

    # To avoid division by zero or weirdness, create a mask for r == 0
    zero_mask = (r == 0)

    # Angle in radians, shift by +pi/2 and wrap [0, 2pi)
    angle = torch.atan2(y, x)
    hue = ((angle + pi/2) % (2 * pi)) / (2 * pi)  # normalized hue [0,1]

    saturation = torch.ones_like(hue)
    value = torch.clamp(1 - r / (pi * 1.414), min=0.0, max=1.0)

    # HSV to RGB conversion (vectorized)
    rgb = hsv_to_rgb_tensor(hue, saturation, value)  # returns (..., 3), floats in [0,1]

    # Replace center pixels (r=0) with white
    rgb[zero_mask, :] = 1.0

    # Scale to 0-255 uint8
    rgb_uint8 = (rgb * 255).to(torch.uint8)
    return rgb_uint8

def hsv_to_rgb_tensor(h, s, v): # as well as this

    i = torch.floor(h * 6).to(torch.int64)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    i = i % 6

    conditions = [i == 0, i == 1, i == 2, i == 3, i == 4, i == 5]

    r = torch.zeros_like(h)
    g = torch.zeros_like(h)
    b = torch.zeros_like(h)

    r = torch.where(conditions[0], v, r)
    g = torch.where(conditions[0], t, g)
    b = torch.where(conditions[0], p, b)

    r = torch.where(conditions[1], q, r)
    g = torch.where(conditions[1], v, g)
    b = torch.where(conditions[1], p, b)

    r = torch.where(conditions[2], p, r)
    g = torch.where(conditions[2], v, g)
    b = torch.where(conditions[2], t, b)

    r = torch.where(conditions[3], p, r)
    g = torch.where(conditions[3], q, g)
    b = torch.where(conditions[3], v, b)

    r = torch.where(conditions[4], t, r)
    g = torch.where(conditions[4], p, g)
    b = torch.where(conditions[4], v, b)

    r = torch.where(conditions[5], v, r)
    g = torch.where(conditions[5], p, g)
    b = torch.where(conditions[5], q, b)

    return torch.stack([r, g, b], dim=-1)

def craziness_color(C):
    normalized = torch.pow((C/C.max()), 0.3)* 255  # Shape: (H, W)
    rgb = normalized.unsqueeze(-1).repeat(1, 1, 3)
    return rgb.to(torch.uint8)

dt = 1e-3
g = 9.81      # gravity
l1 = l2 = 1.0  # rod lengths
m1 = m2 = 1.0  # masses
steps = 2000
threshold = 100.0
M = 0


pi = math.pi
N = 1000

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((N, N))
pygame.display.set_caption("Double Pendulum")
clock = pygame.time.Clock()
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def draw_pendulum(t0,t1):
    pygame.draw.line(screen, WHITE, (N/2, N/2), (N/2+N/4.5*math.sin(t0),N/2+N/4.5*math.cos(t0)), 5)
    pygame.draw.line(screen, WHITE, (N/2+N/4.5*math.sin(t0),N/2+N/4.5*math.cos(t0)), 
                     (N/2+N/4.5*(math.sin(t0)+math.sin(t1)),N/2+N/4.5*(math.cos(t0)+math.cos(t1))), 5)


theta1_0 = torch.linspace(-pi, pi, N)
theta2_0 = torch.linspace(-pi, pi, N)

THETA1, THETA2 = torch.meshgrid(theta1_0, theta2_0, indexing='ij')

# Flatten and stack into state vector: (N*N, 4)
initial_states = torch.stack([THETA1.ravel(), THETA2.ravel(), torch.zeros_like(THETA1).ravel(), torch.zeros_like(THETA2).ravel(), torch.zeros_like(THETA2).ravel()], dim=-1)


state = initial_states.clone()

initial_states = initial_states.to(device)
state = state.to(device)

running = True
run = False
t=0
mousex, mousey = 0, 0
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            run = not run
        if event.type == pygame.MOUSEMOTION:
            mousex, mousey = pygame.mouse.get_pos()
            mousex = int(mousex)
            mousey = int(mousey)
    if run:
        x_dot = compute_derivatives(state)  # shape (N*N, 4)
        state = state + dt * x_dot
        state = compute_max(state)
    
    angles = state[:, :2]
    craziness = state[:,4]
    wrapped = (angles+pi) % (2*pi) - pi
    colors = polar_color(wrapped[:, 0], wrapped[:, 1])
    colors = craziness_color(craziness)
    colors = colors.reshape(N, N, 3)
    img_np = colors.cpu().numpy()
    img_np = np.transpose(img_np, (1, 0, 2))
    surface = pygame.surfarray.make_surface(img_np)
    screen.blit(surface, (0, 0))
    draw_pendulum(wrapped[mousey*N+mousex, 0], wrapped[mousey*N+mousex, 1])

    pygame.display.flip()
    clock.tick(200)  # limit to 30 FPS
    


pygame.quit()
