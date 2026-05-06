"""Salida estilizada con Rich."""

from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
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


def print_menu() -> None:
    """Imprime el menú de configuración."""
    console.print("\n")
    table = Table(title="[bold cyan]MENU DE CONFIGURACION[/bold cyan]", show_header=False, box=None)

    table.add_column("", style="bold")
    table.add_column("", style="")

    table.add_row("1.", "Ejecutar con archivos por defecto (datos/)")
    table.add_row("2.", "Especificar ruta de notas.csv")
    table.add_row("3.", "Especificar ruta de hoja_uedi.csv")
    table.add_row("4.", "Especificar ambas rutas")
    table.add_row("5.", "Salir")

    console.print(table)
    console.print()


def pedir_ruta_rich(tipo: str) -> Path:
    """Pide una ruta de archivo CSV usando Rich."""
    console.print(f"[bold]Ingrese la ruta al archivo {tipo}.csv:[/bold]")

    while True:
        ruta_str = Prompt.ask(">>> ", default="")

        if not ruta_str:
            console.print("[yellow]Ruta vacia. Intente de nuevo.[/yellow]")
            continue

        ruta = Path(ruta_str.strip('"').strip("'"))

        if not ruta.exists():
            console.print(f"[red]El archivo no existe: {ruta}[/red]")
            continue

        if ruta.suffix.lower() != ".csv":
            console.print("[yellow]El archivo debe terminar en .csv[/yellow]")
            continue

        console.print(f"[green]✓ Archivo encontrado[/green]")
        return ruta


def mostrar_menu_rich() -> tuple[Path | None, Path | None]:
    """Muestra el menú interactivo estilizado."""
    while True:
        print_menu()

        eleccion = Prompt.ask(
            "[bold]Seleccione una opcion[/bold]",
            choices=["1", "2", "3", "4", "5"],
            default="",
        )

        if eleccion == "1":
            return None, None
        elif eleccion == "2":
            ruta = pedir_ruta_rich("notas")
            return ruta, None
        elif eleccion == "3":
            ruta = pedir_ruta_rich("hoja")
            return None, ruta
        elif eleccion == "4":
            ruta_notas = pedir_ruta_rich("notas")
            ruta_hoja = pedir_ruta_rich("hoja")
            return ruta_notas, ruta_hoja
        elif eleccion == "5":
            console.print("[cyan]Saliendo...[/cyan]")
            import sys
            sys.exit(0)