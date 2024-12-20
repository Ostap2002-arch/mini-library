from typing import List


def print_table(data: List[dict]) -> None:
    """Функция печати списка книг.

    Эта функция печатает список книг в виде таблицы.

    Args:
        data (List[dict]): Список книг.

    Returns:
        None
    """

    headers = ['id', 'title', 'author', 'year', 'status']
    col_widths = {header: len(header) for header in headers}

    for row in data:
        for header in headers:
            col_widths[header] = max(col_widths[header], len(str(row[header])))

    header_row = " | ".join(header.ljust(col_widths[header]) for header in headers)
    print("-" * len(header_row))
    print(header_row)
    print("-" * len(header_row))
    for row in data:
        row_str = " | ".join(str(row[header]).ljust(col_widths[header]) for header in headers)
        print(row_str)
    print("-" * len(header_row))


