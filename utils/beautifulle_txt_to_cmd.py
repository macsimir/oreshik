from rich.console import Console


def important_b_text_to_cmd(text):
    """Функция для вывода в коммандную строку важные данные 

    Args:
        text (_type_): текст который надо вывести 
    """
    console = Console()

    console.print(f"{text}".upper(), style="bold rgb(255,255,0)")


def plain_b_text_to_cmd(text):
    """Функция для вывода в коммандную строку данные 
    Args:
        text (_type_): текст который надо вывести 
    """
    console = Console()
    console.print(f"{text}",style="rgb(0, 255, 255)")