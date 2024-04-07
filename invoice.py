from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_invoice(items):
    buffer = BytesIO()  # Create a BytesIO buffer to store the PDF content
    c = canvas.Canvas(buffer, pagesize=letter)

    # Define content
    title = "Invoice"
    header = ["Name", "Quantity", "Price", "Total"]
    content = [[item[0], str(item[1]), "${:.2f}".format(
        item[2]), "${:.2f}".format(item[1] * item[2])] for item in items]

    # Define column widths
    col_widths = [200, 100, 100, 100]

    # Write content to PDF
    c.drawString(100, 750, title)

    # Write header
    y = 730
    for i, column in enumerate(header):
        c.drawString(100 + sum(col_widths[:i]), y, column)

    # Write content
    y -= 20
    subtotal = 0
    for row in content:
        for i, cell in enumerate(row):
            c.drawString(100 + sum(col_widths[:i]), y, cell)
            if i == 3:  # Total column
                subtotal += float(cell.replace("$", ""))
        y -= 20

    # Calculate subtotal
    subtotal_text = f"Subtotal: ${subtotal:.2f}"
    c.drawString(300, y - 20, subtotal_text)

    # Calculate tax (7%)
    tax_rate = 0.07
    tax = subtotal * tax_rate
    tax_text = f"Tax (7%): ${tax:.2f}"
    c.drawString(300, y - 40, tax_text)

    # Calculate total including tax
    total_with_tax = subtotal + tax
    total_text = f"Total (incl. tax): ${total_with_tax:.2f}"
    c.drawString(300, y - 60, total_text)

    c.save()

    # Get the PDF content from the buffer and return it as a bytes object
    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content


def print_invoice(items):
    print("Invoice:")
    print("{:<20} {:<10} {:<10} {:<10}".format(
        "Name", "Quantity", "Price", "Total"))
    subtotal = 0
    for item in items:
        item_name, quantity, price = item
        total_price = quantity * price
        subtotal += total_price
        # Adjust spacing based on the length of the item name
        name_spacing = max(0, 20 - len(item_name))
        print("{:<20} {:<10} ${:<8.2f} ${:<9.2f}".format(
            item_name, quantity, price, total_price))

    # Calculate subtotal
    subtotal_formatted = "${:.2f}".format(subtotal)
    print(f"Subtotal: {subtotal_formatted}")

    # Calculate tax (7%)
    tax_rate = 0.07
    tax = subtotal * tax_rate
    tax_formatted = "${:.2f}".format(tax)
    print(f"Tax (7%): {tax_formatted}")

    # Calculate total including tax
    total_with_tax = subtotal + tax
    total_with_tax_formatted = "${:.2f}".format(total_with_tax)
    print(f"Total (incl. tax): {total_with_tax_formatted}")


def get_items():
    items = []
    while True:
        name = input(
            "Enter item name ('done' to finish, 'list' to print invoice to the console): ")
        if name.lower() == 'done':
            break
        elif name.lower() == 'list':
            # Print the current invoice to the console
            if not items:
                print("No items added to the invoice yet.")
            else:
                print_invoice(items)
        else:
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: $"))
            # Append a tuple with three elements
            items.append((name, quantity, price))
    return items


def main():
    items = get_items()

    # Generate the invoice
    invoice_content = generate_invoice(items)

    # Save the invoice to a file
    with open("invoice.pdf", "wb") as f:
        f.write(invoice_content)


if __name__ == "__main__":
    main()
