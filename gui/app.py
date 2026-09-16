import pygame


WIDTH, HEIGHT = 1100, 700


class ForestGUI:
    def __init__(self, game):
        pygame.init()
        pygame.display.set_caption("Forest Resource Simulator")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = game
        self.running = True
        self.message = "Welcome to the forest."
        self.screen_name = "start" if game.player is None else "dashboard"
        self.name_input = ""

        self.font = pygame.font.Font(None, 30)
        self.small = pygame.font.Font(None, 24)
        self.title = pygame.font.Font(None, 44)

        self.forest_buttons = [
            pygame.Rect(55, 185, 300, 85),
            pygame.Rect(400, 185, 300, 85),
            pygame.Rect(745, 185, 300, 85),
        ]

        self.action_buttons = {
            "cut": pygame.Rect(55, 305, 220, 60),
            "sell": pygame.Rect(295, 305, 220, 60),
            "day": pygame.Rect(535, 305, 220, 60),
            "quit": pygame.Rect(775, 305, 270, 60),
        }

        self.start_button = pygame.Rect(425, 430, 250, 60)

    def text(self, value, x, y, font=None):
        surface = (font or self.font).render(str(value), True, (235, 235, 235))
        self.screen.blit(surface, (x, y))

    def draw_start(self):
        self.screen.fill((18, 24, 22))
        self.text("FOREST RESOURCE SIMULATOR", 310, 150, self.title)
        self.text("DSA-II PBL", 490, 205, self.font)
        self.text("Enter explorer name", 425, 300, self.small)
        field = pygame.Rect(375, 330, 350, 55)
        pygame.draw.rect(self.screen, (37, 54, 45), field, border_radius=10)
        pygame.draw.rect(self.screen, (111, 151, 115), field, 2, border_radius=10)
        self.text(self.name_input or "Player", 395, 346)
        pygame.draw.rect(self.screen, (63, 105, 70), self.start_button, border_radius=10)
        self.text("Begin Adventure", 465, 450, self.small)
        self.text("Type a name, then press Enter or click the button.", 360, 540, self.small)

    def draw_dashboard(self):
        self.screen.fill((18, 24, 22))

        self.text("FOREST RESOURCE SIMULATOR", 40, 30, self.title)
        self.text(
            f"{self.game.player.name}  |  Day {self.game.player.day}  |  "
            f"${self.game.player.money}",
            40, 82
        )
        self.text(
            f"Stamina {self.game.player.stamina}/{self.game.player.max_stamina}  |  "
            f"Power {self.game.player.power}  |  Level {self.game.player.level}",
            40, 116
        )

        self.text("FORESTS", 40, 155)

        for i, forest in enumerate(self.game.forests):
            rect = self.forest_buttons[i]
            pygame.draw.rect(self.screen, (37, 54, 45), rect, border_radius=12)
            self.text(f"{i + 1}. {forest.name}", rect.x + 15, rect.y + 15)
            self.text(
                f"{forest.wood_type}  |  ${forest.price}/unit",
                rect.x + 15, rect.y + 48, self.small
            )

        for key, rect in self.action_buttons.items():
            pygame.draw.rect(self.screen, (44, 62, 54), rect, border_radius=10)
            labels = {
                "cut": "Cut Selected",
                "sell": "Sell Wood",
                "day": "End Day",
                "quit": "Quit Game",
            }
            self.text(labels[key], rect.x + 25, rect.y + 18, self.small)

        # Inventory panel
        panel = pygame.Rect(55, 400, 470, 235)
        pygame.draw.rect(self.screen, (27, 34, 31), panel, border_radius=12)
        self.text("INVENTORY", 75, 420)

        if not self.game.player.inventory:
            self.text("Empty", 75, 460, self.small)
        else:
            y = 460
            for wood, quantity in self.game.player.inventory.items():
                self.text(f"{wood:<16} x{quantity}", 75, y, self.small)
                y += 32

        # Activity / DSA panel
        panel2 = pygame.Rect(555, 400, 490, 235)
        pygame.draw.rect(self.screen, (27, 34, 31), panel2, border_radius=12)
        self.text("ACTIVITY LOG (FIFO QUEUE)", 575, 420)
        y = 460
        for entry in self.game.recent_activities()[-4:]:
            self.text(entry, 575, y, self.small)
            y += 30
        self.text("Forest route: " + " → ".join(self.game.reachable_forests()), 575, 580, self.small)

    def draw(self):
        if self.screen_name == "start":
            self.draw_start()
        else:
            self.draw_dashboard()

    def start_game(self):
        self.game.new_game(self.name_input.strip() or "Player")
        self.message = "Your adventure begins."
        self.screen_name = "dashboard"

    def run(self):
        selected = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.screen_name == "start" and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    elif event.unicode.isprintable() and len(self.name_input) < 20:
                        self.name_input += event.unicode

                if (self.screen_name == "start" and event.type == pygame.MOUSEBUTTONDOWN
                        and self.start_button.collidepoint(event.pos)):
                    self.start_game()

                if self.screen_name == "dashboard" and event.type == pygame.MOUSEBUTTONDOWN:
                    position = event.pos

                    for i, rect in enumerate(self.forest_buttons):
                        if rect.collidepoint(position):
                            selected = i
                            self.message = f"Selected {self.game.forests[i].name}."

                    if self.action_buttons["cut"].collidepoint(position):
                        _, self.message = self.game.cut_wood(selected)

                    elif self.action_buttons["sell"].collidepoint(position):
                        forest = self.game.forests[selected]
                        quantity = self.game.player.inventory.get(
                            forest.wood_type, 0
                        )
                        if quantity:
                            _, self.message = self.game.sell_wood(
                                selected, quantity
                            )
                        else:
                            self.message = "No selected wood available to sell."

                    elif self.action_buttons["day"].collidepoint(position):
                        self.message = self.game.end_day()

                    elif self.action_buttons["quit"].collidepoint(position):
                        self.running = False

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


def run(game):
    ForestGUI(game).run()
