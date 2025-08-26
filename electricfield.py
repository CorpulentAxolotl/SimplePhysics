import torch
import pygame
import math

# PyTorch electric field calculation

def compute_electric_forces(r_particles, r_sources, q_sources, k_e=8.987551787e-9):
    diff = r_particles.unsqueeze(1) - r_sources.unsqueeze(0) # (N_particles, N_sources, 2)
    dist_sq = torch.sum(diff ** 2, dim=2) + 1e-20 # avoid div by zero
    dist = torch.sqrt(dist_sq)
    dist_cubed = dist_sq * dist

    force_magnitudes = k_e * q_sources / dist_cubed # (N_particles, N_sources)
    forces = force_magnitudes.unsqueeze(2) * diff # vector forces (N_particles, N_sources, 2)
    net_forces = torch.sum(forces, dim=1) # sum over sources (N_particles, 2)
    return net_forces

# Pygame setup

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electric Field Visualization")
clock = pygame.time.Clock()

# setup charges and grid

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Define source charges and positions
q_sources = torch.tensor([1e-6, -1e-6, 1e-6, -1e-6], device=device)
r_sources = torch.tensor([[400.0, 300.0], # center of screen
                          [600.0, 300.0], # to the right
                          [300.0, 100.0],
                          [200.0, 400.0]],
                         device=device)

# Create a grid of particles
grid_x = torch.linspace(50, WIDTH-50, 60)
grid_y = torch.linspace(50, HEIGHT-50, 45)
xx, yy = torch.meshgrid(grid_x, grid_y)
positions = torch.stack([xx.flatten(), yy.flatten()], dim=1).to(device) # shape (N, 2)

# Scale factor to reduce arrow lengths visually
ARROW_SCALE = 1e19

def draw_arrow(surface, color, start, vector, max_length=20):
    # Draw an arrow from start point in direction of vector scaled to max_length
    vx, vy = vector
    length = math.sqrt(vx*vx + vy*vy)
    if length == 0:
        return

    # Normalize and scale arrow length
    scale = min(length * ARROW_SCALE, max_length) / length
    end_pos = (float(start[0] + vx * scale), float(start[1] + vy * scale))

    pygame.draw.line(surface, color, start, end_pos, 2)

    # Draw arrowhead
    angle = math.atan2(vy, vx)
    arrow_size = 5
    left = (float(end_pos[0] - arrow_size * math.cos(angle - math.pi / 6)),
            float(end_pos[1] - arrow_size * math.sin(angle - math.pi / 6)))
    right = (float(end_pos[0] - arrow_size * math.cos(angle + math.pi / 6)),
            float(end_pos[1] - arrow_size * math.sin(angle + math.pi / 6)))
    pygame.draw.polygon(surface, color, [end_pos, left, right])



running = True
mousedown = [False]*4
while running:
    screen.fill(BLACK)

    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(num_buttons=5)[0]:
                mousedown[0] = True
            if pygame.mouse.get_pressed(num_buttons=5)[2]:
                mousedown[1] = True
            if pygame.mouse.get_pressed(num_buttons=5)[3]:
                mousedown[2] = True
            if pygame.mouse.get_pressed(num_buttons=5)[4]:
                mousedown[3] = True
        if event.type == pygame.MOUSEBUTTONUP:
            mousedown[0] = pygame.mouse.get_pressed(num_buttons=5)[0]
            mousedown[1] = pygame.mouse.get_pressed(num_buttons=5)[2]
            mousedown[2] = pygame.mouse.get_pressed(num_buttons=5)[3]
            mousedown[3] = pygame.mouse.get_pressed(num_buttons=5)[4]
            
    if mousedown[0]:
        x, y = pygame.mouse.get_pos()
        r_sources = r_sources.clone().detach().requires_grad_(False)
        r_sources[0, 0] = x
        r_sources[0, 1] = y
    if mousedown[1]:
        x, y = pygame.mouse.get_pos()
        r_sources = r_sources.clone().detach().requires_grad_(False)
        r_sources[1, 0] = x
        r_sources[1, 1] = y
    if mousedown[2]:
        x, y = pygame.mouse.get_pos()
        r_sources = r_sources.clone().detach().requires_grad_(False)
        r_sources[2, 0] = x
        r_sources[2, 1] = y
    if mousedown[3]:
        x, y = pygame.mouse.get_pos()
        r_sources = r_sources.clone().detach().requires_grad_(False)
        r_sources[3, 0] = x
        r_sources[3, 1] = y
    # Calculate forces on all grid points
    forces = compute_electric_forces(positions, r_sources, q_sources)

    # Draw arrows on screen
    for pos, force in zip(positions.cpu().numpy(), forces.cpu().numpy()):
        start = (float(pos[0]), float(pos[1]))
        draw_arrow(screen, (0,150,0), start, force)

    # Draw source charges as filled circles
    for pos, q in zip(r_sources.cpu().numpy(), q_sources.cpu().numpy()):
        color = (255, 0, 0) if q > 0 else (0, 0, 255)
        pygame.draw.circle(screen, color, pos.astype(int), 10)

    pygame.display.flip()
    clock.tick(30)  # limit to 30 FPS


pygame.quit()
