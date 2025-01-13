from datetime import datetime, timedelta

import pygame


class Freeze:

    def __init__(self):

        self.freeze_time = None
        self.reload_magic_time = None

    def use(self, key_state):
        mod_to_freeze = None
        if (self.reload_magic_time is None) or (datetime.now() - self.reload_magic_time >= timedelta(seconds=6)):
            if key_state[pygame.K_q]:
                self.freeze_time = datetime.now()
                self.reload_magic_time = datetime.now()
                mod_to_freeze = "red"
            if key_state[pygame.K_e]:
                self.freeze_time = datetime.now()
                self.reload_magic_time = datetime.now()
                mod_to_freeze = "blue"
        return mod_to_freeze

    def is_active(self):
        if self.freeze_time is not None:
            return not ((datetime.now() - self.freeze_time) >= timedelta(seconds=3))
        return False
