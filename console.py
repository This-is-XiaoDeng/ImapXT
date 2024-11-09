import rich
import rich.table

console = rich.get_console()


def print_result(emails: list[tuple[str, str]]) -> None:
    table = rich.table.Table()
    table.add_column("Address")
    table.add_column("Subject")
    for e in emails:
        table.add_row(*e)
    console.print(table)


