import randocat


def test_randocat():
    cat_response = randocat.view_random_cat(request=None)

    assert str(cat_response).startswith("200 OK")
    assert "img src" in str(cat_response)
