import reflex as rx
from T9.state import State


def TypingField():
    return rx.text_area(
        value=State.text,
        placeholder="Start typing...",
        on_change=State.update_text,
        width="600px",
    )

def Suggestions():
    return rx.foreach(
            State.suggestions,
            lambda suggestion: rx.button(
                suggestion,
                on_click=lambda: State.apply_suggestion(suggestion),
                width="600px",
            )
        )

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            TypingField(),
            Suggestions(),
        ),
    )

app = rx.App()
app.add_page(index, title="T9")
