import pygame

class Guard:
    def __init__(self):
        self.door_closed = False
        self.camera_open = False
        self.current_camera_index = 0
        self.energy = 100
        self.start_time = pygame.time.get_ticks()
        self.game_hours = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM"]
        self.current_hour = "12 AM"

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.door_closed = not self.door_closed
            if event.key == pygame.K_c:
                self.camera_open = not self.camera_open
            if event.key == pygame.K_LEFT:
                self.current_camera_index = max(0, self.current_camera_index - 1)
            if event.key == pygame.K_RIGHT:
                self.current_camera_index = min(6, self.current_camera_index + 1)

    def update(self):
        if self.door_closed or self.camera_open:
            self.energy -= 0.05

    def draw(self, window, rooms):
        color_door = (255, 0, 0) if self.door_closed else (0, 255, 0)
        pygame.draw.rect(window, color_door, (50, 250, 50, 100))

        font = pygame.font.Font(None, 24)
        energy_text = font.render(f"Energy: {int(self.energy)}%", True, (255, 255, 255))
        window.blit(energy_text, (600, 10))

        if self.camera_open:
            cam_text = font.render(f"Camera: {rooms[self.current_camera_index]}", True, (255, 255, 0))
            window.blit(cam_text, (300, 50))