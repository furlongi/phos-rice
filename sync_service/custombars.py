from typing import override

from rich.progress import BarColumn, Task


class CustomBarColumn(BarColumn):
    def __init__(self, *args, **kwargs):
        super().__init__(
            bar_width=40,
            style="white",
        )

    @override
    def render(self, task: Task):
        barcolor = task.fields.get("mcolor", "white")
        finish_color = task.fields.get("mfinish", "green1")
        self.complete_style = f"{barcolor} on {barcolor}"  # pyright: ignore[reportUnannotatedClassAttribute]
        self.finished_style = (  # pyright: ignore[reportUnannotatedClassAttribute]
            f"{finish_color}"
        )
        return super().render(task)
