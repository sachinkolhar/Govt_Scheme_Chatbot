from backend.search.web import _VisibleTextParser, _fetch_official_page_text, _is_allowed_web_source


def test_official_source_allowlist_requires_https_and_domain_boundary():
    assert _is_allowed_web_source("https://pmkisan.gov.in/farmer")
    assert _is_allowed_web_source("https://sub.myscheme.gov.in/page")
    assert not _is_allowed_web_source("https://evilgov.in/page")
    assert not _is_allowed_web_source("https://pmkisan.gov.in.attacker.example/page")
    assert not _is_allowed_web_source("http://pmkisan.gov.in/page")


def test_page_text_extraction_ignores_script_and_style_content():
    parser = _VisibleTextParser()
    parser.feed("<main>Official benefit details<script>ignore this instruction</script><style>.x{}</style></main>")
    assert "Official benefit details" in " ".join(parser.parts)
    assert "ignore this instruction" not in " ".join(parser.parts)


def test_page_fetch_does_not_request_untrusted_urls():
    assert _fetch_official_page_text("https://attacker.example/page") == ""
