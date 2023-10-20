from unittest.mock import patch

from bs4 import BeautifulSoup

from from_my_ex.posts import Media


def test_media_from_img_tag():
    html = '<div><img src="42.png" alt="fourty two" /></div>'
    tree = BeautifulSoup(html)
    img, *_ = tree.find_all("img")
    with patch("from_my_ex.posts.get") as mock:
        mock.return_value.content = b"42"
        mock.return_value.headers = {"content-type": "image/png"}
        media = Media.from_img_tag(img)

    assert media.content == b"42"
    assert media.mime == "image/png"
    assert media.alt == "fourty two"
