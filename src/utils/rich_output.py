"""Salida estilizada con Rich."""

from rich.console import Console
from rich.table import Table
from rich.theme import Theme


custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
})


console = Console(theme=custom_theme)


def print_resumen(total: int, actualizados: int, sin_match: int, ruta: str) -> None:
    """Imprime el resumen con tabla de Rich."""
    table = Table(title="[bold green]RESUMEN[/bold green]", show_header=False)

    table.add_column("", style="bold")
    table.add_column("", style="")

    table.add_row("Total de registros", str(total))
    table.add_row("Actualizados", f"[green]{actualizados}[/green]")
    if sin_match > 0:
        table.add_row("Sin coincidencia", f"[yellow]{sin_match}[/yellow]")

    console.print(table)
    console.print(f"\n[bold green]Proceso completado exitosamente![/bold green]\n")
    console.print(f"  [blue]{ruta}[/blue]")