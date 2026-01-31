#!/usr/bin/env python3
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "shopping_list.json")


#functie pentru incarcarea articolelor din fisier
def load_items():
    """Citește lista de articole din fișierul JSON. Dacă nu există, întoarce listă goală."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Dacă fișierul e corupt, începem de la 0
            return []# JSON invalid -> lista goala

#functie pentru salvarea articolelor in fisier
def save_items(items):
    """Salvează lista de articole în fișierul JSON."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def add_item(name, quantity, price, category):
    """Adaugă un articol nou în lista de cumpărături, cu validări simple."""
    # Validări
    name = name.strip()
    category = category.strip()


    if quantity <= 0:
        print("Eroare: cantitatea trebuie să fie > 0.")
        return
    if price < 0:
        print("Eroare: prețul nu poate fi negativ.")
        return
    if not name.strip():
        print("Eroare: numele nu poate fi gol.")
        return

    items = load_items()

    item = {
        "name": name,
        "quantity": quantity,
        "price": price,
        "category": category
    }
    items.append(item)
    save_items(items)

    total_item = quantity * price
    print(
        f'Articol adăugat: {name} (cantitate: {quantity}, preț unitar: {price} RON, '
        f'total: {total_item} RON, categorie: {category})'
    )
    print(f"Lista salvată în {DATA_FILE}")

def remove_item(name):
    """Sterge un articol dupa nume."""
    name = name.strip()
    category = category.strip()

    items = load_items()
    if not items:
        print("Lista de cumparaturi este goala.")
        return
    
    initial_len = len(items)
    items= [it for it in items if it["name"].strip()lower() != name.strip().lower()]

    if len(items) == initial_len:
        print(f'Nu am găsit niciun articol cu numele "{name}".')
        return

    save_items(items)
    print(f'Articolul "{name}" a fost șters cu succes.')

def search_by_category(category):
    """Afișează articolele dintr-o categorie."""
    name = name.strip()
    category = category.strip()


    items = load_items()
    if not items:
        print("Lista de cumpărături este goală.")
        return

    cat = category.strip().lower()
    found = [it for it in items if it["category"].strip().lower() == cat]

    if not found:
        print(f'Nu există articole în categoria "{category}".')
        return

    print(f'Articole în categoria "{category}":')
    for item in found:
        total = item["quantity"] * item["price"]
        print(
            f'- {item["name"]}: {item["quantity"]} x {item["price"]} RON '
            f'(total: {total} RON)'
        )


def export_csv(filename):
    """Exportă lista în fișier CSV."""
    items = load_items()
    if not items:
        print("Lista de cumpărături este goală.")
        return

    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "quantity", "price", "category", "total"])
        for it in items:
            total = it["quantity"] * it["price"]
            writer.writerow([it["name"], it["quantity"], it["price"], it["category"], total])

    print(f"Export realizat: {filename}")

def list_items(sort_by=None):
    """Listează articolele, opțional sortate după name/price/category."""
    items = load_items()
    if not items:
        print("Lista de cumpărături este goală.")
        return

    if sort_by == "price":
        items.sort(key=lambda x: x["price"])
    elif sort_by == "name":
        items.sort(key=lambda x: x["name"].lower())
    elif sort_by == "category":
        items.sort(key=lambda x: x["category"].lower())

    print("Lista de cumpărături:")
    for item in items:
        total = item["quantity"] * item["price"]
        print(
            f'- {item["name"]}: {item["quantity"]} x {item["price"]} RON '
            f'(total: {total} RON), categorie: {item["category"]}'
        )


def total_cost():
    """Calculează costul total și subtotalurile pe categorii."""
    items = load_items()
    if not items:
        print("Lista de cumpărături este goală.")
        return

    total = 0.0
    by_category = {}

    for item in items:
        item_total = item["quantity"] * item["price"]
        total += item_total
        cat = item["category"]
        by_category[cat] = by_category.get(cat, 0.0) + item_total

    print(f"Cost total: {total} RON")
    print("Subtotaluri pe categorii:")
    for cat, value in by_category.items():
        print(f"  - {cat}: {value} RON")


def print_help():
    """Afișează comenzile disponibile."""
    print("Comenzi disponibile:")
    print('  add "nume" cantitate pret "categorie"')
    print('  remove "nume"')
    print('  list [--sort name|price|category]')
    print('  search --category "categorie"')
    print('  total')
    print('  export nume_fisier.csv')
    print('  help')


def main():

    if len(sys.argv) < 2:
        print("Eroare: nu ai dat nicio comandă.")
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        # ./shopping_list add "mere" 5 2.5 "fructe"
        if len(sys.argv) != 6:
            print('Utilizare: ./shopping_list add "nume" cantitate pret "categorie"')
            sys.exit(1)
        name = sys.argv[2]
        quantity = int(sys.argv[3])
        price = float(sys.argv[4])
        category = sys.argv[5]
        add_item(name, quantity, price, category)

    elif command == "list":
        # ./shopping_list list --sort price
        sort_by = None
        if len(sys.argv) == 4 and sys.argv[2] == "--sort":
            sort_by = sys.argv[3]
        list_items(sort_by)

    elif command == "total":
        total_cost()

    elif command == "help":
        print_help()

    else:
        print(f"Comandă necunoscută: {command}")
        print_help()


if __name__ == "__main__":
    main()
