import pygame
import sys
from animatronic import Diddy
from environment import Environment
from guard import Guard


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.env = Environment()
        self.diddy = Diddy(self.env)
        self.guard = Guard()

        self.clock = pygame.time.Clock()
        self.camera_active = False
        self.camera_rooms = ["h1", "h11", "101", "102", "105", "202", "205"]
        self.current_camera = "205"

        self.screen_size = (1920, 1080)

        # Таймер игры
        self.start_time = pygame.time.get_ticks()
        self.game_hours = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM"]
        self.current_hour = "12 AM"

        # Загрузка фонов
        office_img = pygame.image.load("assets/office.png")
        self.office_background = pygame.transform.scale(office_img, (1920, 1080))

        door_closed_img = pygame.image.load("assets/door_closed.png")
        self.door_closed_img = pygame.transform.scale(door_closed_img, (1920, 1080))

        # Камеры
        camera_image_paths = {
             "101": "assets/cameras/101.png",
            "102": "assets/cameras/102.png",
            "105": "assets/cameras/105.png",
            "202": "assets/cameras/202.png",
            "205": "assets/cameras/205.png",
            "h1": "assets/cameras/h1.png",
            "h11": "assets/cameras/h11.png"
        }

        self.camera_images = {
            room: pygame.transform.scale(pygame.image.load(path), (1600, 900))
            for room, path in camera_image_paths.items()
        }

        # Аниматроники
        animatronic_image_paths = {
             "101": "assets/Shrek/floor1/Shrek101.png",
            "102": "assets/Shrek/floor1/Shrek102.png",
            "103": "assets/Shrek/floor1/Shrek103.png",
            "104": "assets/Shrek/floor1/Shrek104.png",
            "105": "assets/Shrek/floor1/Shrek105.png",
            "h1": "assets/Shrek/floor1/Shrekh1.png",
            "h2": "assets/Shrek/floor1/Shrekh2.png",
            "h3": "assets/Shrek/floor1/Shrekh3.png",
            "h4": "assets/Shrek/floor1/Shrekh4.png",
            "h5": "assets/Shrek/floor1/Shrekh5.png",
            "AST": "assets/Shrek/floor2/ShrekAST.png",
            "h11": "assets/Shrek/floor2/Shrekh11.png",
            "h12": "assets/Shrek/floor2/Shrekh12.png",
            "h13": "assets/Shrek/floor2/Shrekh13.png",
            "h14": "assets/Shrek/floor2/Shrekh14.png",
            "201": "assets/Shrek/floor2/Shrekh201.png",
            "202": "assets/Shrek/floor2/Shrekh202.png",
            "203": "assets/Shrek/floor2/Shrekh203.png",
            "204": "assets/Shrek/floor2/Shrekh204.png",
            "205": "assets/Shrek/floor2/Shrekh205.png",
            "PCS": "assets/Shrek/floor2/ShrekPCS.png"
        }

        self.animatronic_images = {
            room: pygame.transform.scale(pygame.image.load(path), (1600, 900))
            for room, path in animatronic_image_paths.items()
        }

        self.image_position = (200, 100)
        self.font = pygame.font.SysFont("Arial", 50)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.camera_active = not self.camera_active
                    elif event.key == pygame.K_LEFT:
                        index = self.camera_rooms.index(self.current_camera)
                        self.current_camera = self.camera_rooms[(index - 1) % len(self.camera_rooms)]
                    elif event.key == pygame.K_RIGHT:
                        index = self.camera_rooms.index(self.current_camera)
                        self.current_camera = self.camera_rooms[(index + 1) % len(self.camera_rooms)]
                    elif event.key == pygame.K_d:
                        self.guard.door_closed = not self.guard.door_closed

                    self.guard.handle_input(event)

            self.diddy.move(self.guard.door_closed)
            self.guard.update()
            self.screen.fill((0, 0, 0))

            # Обновление игрового времени
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            hour_index = min(int(elapsed_time // 90), 6)
            self.current_hour = self.game_hours[hour_index]

            # Камера активна
            if self.camera_active:
                self.screen.blit(self.camera_images[self.current_camera], self.image_position)
                visible_rooms = self.env.get_camera_view(self.current_camera)

                if self.diddy.current_room in visible_rooms:
                    anim_img = self.animatronic_images.get(self.diddy.current_room)
                    if anim_img:
                        self.screen.blit(anim_img, self.image_position)

                cam_text = self.font.render(f"Camera: {self.current_camera}", True, (255, 255, 255))
                cam_rect = cam_text.get_rect(topright=(self.screen_size[0] - 200, 100))
                self.screen.blit(cam_text, cam_rect)
            else:
                bg = self.door_closed_img if self.guard.door_closed else self.office_background
                self.screen.blit(bg, (0, 0))

            time_text = self.font.render(self.current_hour, True, (255, 255, 255))
            self.screen.blit(time_text, (50, 30))

            total_seconds = int(elapsed_time)
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            real_time_text = self.font.render(f"Прош Time: {minutes}", True, (255, 255, 255))
            self.screen.blit(real_time_text, (50, 100))

            self.guard.draw(self.screen, self.env.rooms)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


def draw_menu(screen):
    font = pygame.font.SysFont("Arial", 80)
    small_font = pygame.font.SysFont("Arial", 50)

    screen.fill((255, 255, 255))  # Белый фон
    blue = (0, 0, 225)

    title = font.render("One Night at Salymbekov", True, blue)
    play_button = small_font.render("Играть", True, blue)
    quit_button = small_font.render("Выйти", True, blue)

    title_rect = title.get_rect(center=(960, 200))
    play_rect = play_button.get_rect(center=(960, 450))
    quit_rect = quit_button.get_rect(center=(960, 550))

    screen.blit(title, title_rect)
    screen.blit(play_button, play_rect)
    screen.blit(quit_button, quit_rect)

    return play_rect, quit_rect


def main_menu(screen):
    while True:
        play_rect, quit_rect = draw_menu(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Shrek Night")

    main_menu(screen)
    game = Game(screen)
    game.run()
