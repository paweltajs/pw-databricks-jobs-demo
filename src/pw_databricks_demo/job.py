"""C. Ta sama logika opakowana w instalowalny modul Python."""

import json


def calculate_sales():
    """Generuje fikcyjne zamowienia i oblicza proste podsumowanie."""
    sales = [
        {"day": day, "orders": 8 + 2 * day, "unit_price": 20 + day}
        for day in range(1, 8)
    ]

    return {
        "days": len(sales),
        "orders": sum(item["orders"] for item in sales),
        "revenue_pln": sum(item["orders"] * item["unit_price"] for item in sales),
        "best_day": max(sales, key=lambda item: item["orders"] * item["unit_price"])["day"],
    }


def main():
    print(json.dumps(calculate_sales(), indent=2))
    print("Zadanie wykonane w Pythonie w Databricks!")


if __name__ == "__main__":
    main()
