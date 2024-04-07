from unittest.mock import patch
from invoice import generate_invoice, get_items, print_invoice


def test_generate_invoice():
    items = [("Item 1", 2, 10.0), ("Item 2", 1, 20.0)]
    invoice_content = generate_invoice(items)
    assert isinstance(invoice_content, bytes)
    # You may add more assertions to validate the content or structure of the generated PDF if needed.

def test_print_invoice(capsys):
    items = [("Item 1", 2, 10.0), ("Item 2", 1, 20.0)]
    print_invoice(items)
    captured = capsys.readouterr()
    assert "Invoice:" in captured.out
    assert "Item 1" in captured.out
    assert "Item 2" in captured.out

def test_get_items_input(capsys):
    # Simulate user input using patch
    with patch("builtins.input", side_effect=["Item 1", "2", "10.0", "Item 2", "1", "20.0", "done"]):
        items = get_items()
        assert items == [("Item 1", 2, 10.0), ("Item 2", 1, 20.0)]




