import importlib
import os

from timeout_decorator import timeout, TimeoutError


def import_year(year):
    year_path = os.path.join(os.getcwd(), str(year))
    for day in range(1, 26):
        day_filename = f"day{day:02d}.py"
        day_path = os.path.join(year_path, day_filename)
        if os.path.exists(day_path):
            module_name = f"{year}.{day_filename[:-3]}"
            import_module_with_timeout(module_name)


@timeout(10)
def import_module_with_timeout(module_name):
    module = importlib.import_module(module_name)
    print(f"Imported {module_name}")
    return module


if __name__ == '__main__':
    for current_year in reversed(range(2020, 2023)):
        try:
            import_year(current_year)
        except TimeoutError:
            print(f"Timed out importing {current_year}")
        except ImportError as e:
            print(f"Failed to import {current_year}: {e}")