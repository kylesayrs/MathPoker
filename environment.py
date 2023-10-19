from typing import List, Tuple, Optional, Dict, Any, Union

import numpy
import functools
from termcolor import colored
from gym import Env, spaces

from src.config import EnvironmentConfig
from src.piece import Piece
from src.utils import iterate_shape_2d, action_confs_to_prob, get_fillable_spaces, rand_argmax
from pieces import load_pieces


class MathPokerEnv(Env):
    def __init__(
        self,
        environment_config: EnvironmentConfig,
        tokenizer
    ):
        super().__init__()
        self.config = environment_config

        self.observation_space = spaces.Dict({
            "inputs": spaces.MultiDiscrete([self.config.num_cards] * self.config.sequence_length),
            "outputs": spaces.MultiDiscrete([self.config.num_cards + 1] * self.config.sequence_length),
        })

        self.action_space = spaces.Discrete(self.config.num_cards)

        self.inputs = None
        self.outputs = None


    def reset(self) -> None:
        self.inputs = numpy.random.randint(0, self.config.num_cards, size=self.config.sequence_length)
        self.outputs = None # [tokenizer(MASK)] * self.config.sequence_length
        
        return self.get_observation()


    def step(self, output: int) -> Tuple[numpy.ndarray, float, bool, Dict[str, Any]]:
        self.outputs.append(output)
        if not partial_sequence_is_valid(self.outputs):
            reward = -10

        if len(self.outputs) == self.config.sequence_length:
            reward = evaluate_sequence(self.outputs)

        # return results
        observation = self.get_observation()
        reward = self.get_reward()
        is_finished = self.is_finished()
        info = {"is_success": self.is_success()}

        return observation, reward, is_finished, info
    

    def partial_sequence_is_valid(self, sequence: List[int]) -> bool:
        """
        SYNTAX RULES
            No adjacent operators
            No adjacent numbers

        As a result, the sequence must be NONONON
        """
        for token, next_token in zip(sequence[:-1], sequence[1:]):
            if (
                (is_operator(token) and is_operator(next_token)) or
                (is_number(token) and is_number(next_token))
            ):
                return False
            
        return True
        

    def evaluate_sequence(sequence: List[int]) -> float:
        
        pass

    def is_operator():
        pass

    def is_number():
        pass


    def is_success(self):
        return self.board.all()
    

    def is_failure(self):
        return self.invalid_actions_mask.all()


    def get_reward(self) -> float:
        if self.is_success():
            return self.config.complete_reward
        
        elif self.is_failure():
            return self.config.fail_reward
        
        else:
            return (
                self.config.fill_reward * numpy.count_nonzero(self.board) +
                self.config.step_reward
            )
    

    def is_finished(self) -> bool:
        return self.is_success() or self.is_failure()


    def render(self, mode: str = "human") -> None:
        if mode == "human":
            self.render_human()
        else:
            raise ValueError(f"Unknown render mode {mode}")


    def render_human(
        self,
        action_history: Optional[List[int]] = None,
        show_observation: bool = True
    ) -> None:
        pass
