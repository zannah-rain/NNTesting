import pygame
from App.AI.Model import Model
from App.AI.Memory import Memory
from App.Functions.rotate_array import rotate_array
import random
import numpy as np


class Agent:

    def __init__(self, x, y, sess, heat_map, colour=(0, 255, 0), output_activation=None, rotation_sampling=False):
        self.x = x
        self.y = y
        self.colour = colour

        self._brain = Model(9, 9, 500, output_activation=output_activation)
        self._brain.initialize_tensorflow(sess)

        self._memory = Memory(2000)
        self._sess = sess
        self._max_epsilon = 0.9
        self._min_epsilon = 0.2
        self._epsilon = self._max_epsilon
        self._epsilon_decay_time = 10000
        self._heat_map = heat_map
        self._steps = 0  # Just a timer
        self._score = self.calculate_score()
        self._next_state = self.build_state()
        self._future_discount = 0.9

        # Whether we'll add rotations to the training set
        self._rotation_sampling = rotation_sampling

        self._random_delay = np.random.randint(50)

    def step(self):
        self._steps += 1

        self._score = self.calculate_score()

        state = self._next_state

        # Select & perform a movement action
        action = self.choose_action(state)

        # 0 = top-left. 1 = top. 2 = top-right etc
        new_x = self.x + [-1, 0, 1, 1, 1, 0, -1, -1, 0][action]
        new_y = self.y + [-1, -1, -1, 0, 1, 1, 1, 0, 0][action]
        self.move_to(new_x, new_y)

        self._next_state = self.build_state()

        if self._rotation_sampling:
            for i in range(8):
                for j in range(8):
                    self._memory.add_sample((rotate_array(state, i).flatten(),
                                            Agent.rotate_action(action, i),
                                            self._score,
                                            rotate_array(self._next_state, j).flatten()))
        else:
            self._memory.add_sample((state.flatten(), action, self._score, self._next_state.flatten()))

        if (self._steps + self._random_delay) % 50 == 0:
            self.train()

        # Decay our epsilon
        if self._epsilon > self._min_epsilon:
            self._epsilon -= (self._max_epsilon - self._min_epsilon) / self._epsilon_decay_time

    def move_to(self, x, y):
        if x < self._heat_map.cell_width + 1:
            x = (self._heat_map.n_cells - 1) * self._heat_map.cell_width - 1
        if y < self._heat_map.cell_height + 1:
            y = (self._heat_map.n_cells - 1) * self._heat_map.cell_height - 1
        if x > (self._heat_map.n_cells - 1) * self._heat_map.cell_width - 1:
            x = self._heat_map.cell_width + 1
        if y > (self._heat_map.n_cells - 1) * self._heat_map.cell_height - 1:
            y = self._heat_map.cell_height + 1

        self.x = x
        self.y = y

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, (self.x, self.y, 1, 1))

    def build_state(self):
        return self._heat_map.get_temperature_area(self.x, self.y, 1, 1)

    def choose_action(self, state):
        predictions = self._brain.predict_one(state, self._sess)[0]
        if random.random() < self._epsilon:
            predictions = np.exp(predictions)
            return np.random.choice(9, p=predictions / predictions.sum()) # Softmax
        else:
            return np.argmax(predictions) # Actual max

    # TODO: Split actions into their own object somehow so rotations can be defined better
    @staticmethod
    def rotate_action(action, amount):
        if action < 8:
            action = (action + amount) % 8
        return action

    def calculate_score(self):
        return self._heat_map.get_temperature(self.x, self.y)

    def train(self):
        batch = self._memory.sample(self._brain.batch_size)
        states = np.array([val[0] for val in batch])
        next_states = np.array([(np.zeros(self._brain.state_size)
                                 if val[3] is None else val[3]) for val in batch])
        # predict Q(s,a) given the batch of states
        q_s_a = self._brain.predict_batch(states, self._sess)
        # predict Q(s',a') - so that we can do gamma * max(Q(s'a')) below
        q_s_a_d = self._brain.predict_batch(next_states, self._sess)
        # setup training arrays
        x = np.zeros((len(batch), self._brain.state_size))
        y = np.zeros((len(batch), self._brain.num_actions))
        for i, b in enumerate(batch):
            state, action, reward, next_state = b[0], b[1], b[2], b[3]
            # get the current q values for all actions in state
            current_q = q_s_a[i]
            # update the q value for action
            if next_state is None:
                # in this case, the game completed after action, so there is no max Q(s',a')
                # prediction possible
                current_q[action] = reward
            else:
                current_q[action] = reward + self._future_discount * np.amax(q_s_a_d[i])
            x[i] = state
            y[i] = current_q
        self._brain.train_batch(self._sess, x, y)
