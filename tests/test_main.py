from protein_annotator.main import say_hi


def test_say_hi() -> None:
    assert "hi!" == say_hi()
