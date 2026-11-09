import main


def run_with_inputs(monkeypatch, capsys, inputs):
    answers = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))
    main.main()
    return capsys.readouterr().out


def test_exit_straight_away(monkeypatch, capsys):
    output = run_with_inputs(monkeypatch, capsys, ["0"])
    assert "Goodbye." in output


def test_list_books_in_title_order(monkeypatch, capsys):
    output = run_with_inputs(monkeypatch, capsys, ["4", "0"])
    assert output.index("Algorithms") < output.index("Clean Code")


def test_borrow_and_return(monkeypatch, capsys):
    output = run_with_inputs(
        monkeypatch, capsys,
        ["5", "9780132350884", "M001", "6", "9780132350884", "0"],
    )
    assert "Book borrowed." in output
    assert "Book returned." in output


def test_invalid_menu_choice(monkeypatch, capsys):
    output = run_with_inputs(monkeypatch, capsys, ["x", "0"])
    assert "Please choose a number from the menu." in output


def test_errors_are_shown_not_crashed(monkeypatch, capsys):
    output = run_with_inputs(monkeypatch, capsys, ["6", "0000000000000", "0"])
    assert "Error: No book with ISBN 0000000000000." in output


def test_each_run_starts_with_fresh_sample_books(monkeypatch, capsys):
    run_with_inputs(monkeypatch, capsys, ["5", "9780132350884", "M001", "0"])
    output = run_with_inputs(monkeypatch, capsys, ["2", "9780132350884", "0"])
    assert "Available" in output