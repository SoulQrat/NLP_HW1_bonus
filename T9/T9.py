import sys
import os
sys.path.append(os.path.dirname(__file__))

import reflex as rx
from state import State


def TypingField():
    return rx.text_area(
        value=State.text,
        placeholder='Start typing...',
        on_change=State.update_field,
        width="600px",
    )

def WordSuggestions():
    return rx.foreach(
            State.word_suggestions,
            lambda word_suggestions: rx.button(
                word_suggestions,
                on_click=lambda: State.apply_word_suggestion(word_suggestions),
                width="600px",
                bg="red"
            )
        )

def TextSuggestions():
    return rx.foreach(
            State.text_suggestions,
            lambda text_suggestions: rx.button(
                text_suggestions,
                on_click=lambda: State.apply_text_suggestion(text_suggestions),
                width="600px",
            )
        )

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            TypingField(),
            WordSuggestions(),
            TextSuggestions(),
        ),
        align="center",
    )

app = rx.App()
app.add_page(index, title="T9")
