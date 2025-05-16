import random
import time
import numpy as np

class Diddy:
    def __init__(self, environment, night_duration=180):
        self.env = environment
        self.current_room = "205"
        self.start_time = time.time()
        self.last_move_time = self.start_time

        self.learning_rate = 0.1
        self.discount_factor = 0.95

        self.epsilon_start = 1.0
        self.epsilon_end = 0.01
        self.epsilon = self.epsilon_start
        self.night_duration = night_duration

        self.rooms = list(self.env.rooms.keys())
        self.room_to_index = {room: idx for idx, room in enumerate(self.rooms)}
        self.index_to_room = {idx: room for idx, room in enumerate(self.rooms)}

        self.q_table = np.zeros((len(self.rooms), len(self.rooms)))

    def update_epsilon(self):
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.night_duration, 1.0)
        self.epsilon = self.epsilon_start - progress * (self.epsilon_start - self.epsilon_end)

    def move(self, door_closed, reward=0):
        now = time.time()
        move_delay = 5  # Ход каждые

        if now - self.last_move_time > move_delay:
            self.update_epsilon()

            current_index = self.room_to_index[self.current_room]
            next_rooms = self.env.get_next_rooms(self.current_room)

            if random.random() < self.epsilon:
                # Случайное движение
                chosen_room = random.choice(next_rooms)
            else:
                # Лучшее движение по Q-таблице
                next_indices = [self.room_to_index[room] for room in next_rooms]
                q_values = self.q_table[current_index, next_indices]
                best_index = next_indices[np.argmax(q_values)]
                chosen_room = self.index_to_room[best_index]

            reward = self.calculate_reward(chosen_room, door_closed)

            next_index = self.room_to_index[chosen_room]
            old_value = self.q_table[current_index, next_index]
            future_max = np.max(self.q_table[next_index])

            new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (
                reward + self.discount_factor * future_max
            )
            self.q_table[current_index, next_index] = new_value

            if chosen_room == "Office" and door_closed:
                self.current_room = "101"
            else:
                self.current_room = chosen_room

            self.last_move_time = now

    def calculate_reward(self, chosen_room, door_closed):
        if chosen_room == "Office":
            return -10 if door_closed else 10
        else:
            return -1
