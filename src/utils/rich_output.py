"""Salida estilizada con Rich."""

from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt


console = Console()


def print_encabezado(titulo: str) -> None:
    """Imprime el encabezado principal."""
    console.print(f"\n[bold cyan]{'=' * 50}[/bold cyan]")
    console.print(f"[bold cyan]{titulo:^50}[/bold cyan]")
    console.print(f"[bold cyan]{'=' * 50}[/bold cyan]")


def print_paso(numero: int, mensaje: str) -> None:
    """Imprime un paso del proceso."""
    console.print(f"\n[yellow bold]({numero})[/yellow bold] [bold]{mensaje}[/bold]")


def print_info(mensaje: str) -> None:
    """Imprime un mensaje de info."""
    console.print(f"[cyan]{mensaje}[/cyan]")


def print_exito(mensaje: str) -> None:
    """Imprime un mensaje de exito."""
    console.print(f"[green]OK {mensaje}[/green]")


def print_advertencia(mensaje: str) -> None:
    """Imprime una advertencia."""
    console.print(f"[yellow]! {mensaje}[/yellow]")


def print_error(mensaje: str) -> None:
    """Imprime un error."""
    console.print(f"[red]X {mensaje}[/red]")


def print_substep(mensaje: str) -> None:
    """Imprime un subpaso."""
    console.print(f"     - {mensaje}")


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


def pedir_ruta(tipo: str) -> Path:
    """Pide una ruta de archivo CSV."""
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


def mostrar_menu() -> tuple[Path | None, Path | None]:
    """Muestra el menú interactivo."""
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
            ruta = pedir_ruta("notas")
            return ruta, None
        elif eleccion == "3":
            ruta = pedir_ruta("hoja")
            return None, ruta
        elif eleccion == "4":
            ruta_notas = pedir_ruta("notas")
            ruta_hoja = pedir_ruta("hoja")
            return ruta_notas, ruta_hoja
        elif eleccion == "5":
            console.print("[cyan]Saliendo...[/cyan]")
            import sys
            sys.exit(0)


def print_resumen(total: int, actualizados: int, sin_match: int, ruta: str) -> None:
    """Imprime el resumen final."""
    console.print()

    table = Table(title="[bold green]RESUMEN[/bold green]", show_header=False)

    table.add_column("")
    table.add_column("")

    table.add_row("Total de registros", str(total))
    table.add_row("Actualizados", f"[green]{actualizados}[/green]")
    if sin_match > 0:
        table.add_row("Sin coincidencia", f"[yellow]{sin_match}[/yellow]")

    console.print(table)
    console.print(f"[bold green]Proceso completado exitosamente![/bold green]\n")
    console.print(f"  [bold green]{ruta}[/bold green]")