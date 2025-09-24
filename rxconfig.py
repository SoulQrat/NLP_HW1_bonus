import reflex as rx

config = rx.Config(
    app_name="T9",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)