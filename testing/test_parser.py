import parser


def test_empty_body():
    print("hi")

    assert parser.HTMLparser("<body></body>").body == ""


def test_body_with_text():
    assert (
        parser.HTMLparser("<body>abcd!wadjpz\n\t12093</body>").body
        == "abcdwadjpz\n\t12093"
    )


def test_empty_text():
    assert parser.HTMLparser("").body == ""


def test_tag():
    assert parser.HTMLparser("<body><p>test</p></body>").body == "test"


def test_multiline_tag():
    assert (
        parser.HTMLparser(
            """<body>
                <
                p>test<
                /
                p>
            </body>"""
        ).body
        == "test"
    )


def test_apostrophe_in_text():
    assert (
        parser.HTMLparser("<body>The fella's friend's is lookin' good!</body>").body
        == "The fella's friend's is lookin' good"
    )
