import reflex as rx
from typing import List
from T9.suggestion import tokenize


class State(rx.State):
    text: str = ''
    suggestions: List[str] = []


    def _update_suggestions(self) -> List[str]:
        if self.text == '':
            self.suggestions = []
            return
        tokens = tokenize(self.text)
        self.suggestions = ['dummy text', 'text', 'dummy']

    def update_text(self, new_text: str):
        self.text = new_text
        self._update_suggestions()

    def apply_suggestion(self, suggestion: str):
        self.text += suggestion
        self._update_suggestions()
