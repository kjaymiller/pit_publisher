import pytest
import models

def test_get_html_url_defaults_to_none():
    assert models.get_html_url('') == None

def test_get_html_url_finds_href():
    subject = models.get_html_url('<a href="foo.com">Test</a>')
    expected_result = ('foo.com', 'Test')
    assert subject == expected_result

def test_get_html_url_finds_src_no_alt():
    subject = models.get_html_url('<img src="foo.com">Test</img>')
    expected_result = ('foo.com', '')
    assert subject == expected_result



def test_remove_iframe():
    test_content = '''This content should appear
<div><iframe src='foo.html'>This should not appear</iframe></div>
This should also appear'''
    expected_result = '''This content should appear
<a href='foo.com'> Click to Play Video</a>
This should also appear'''
    no_iframe = models.remove_iframes(test_content)
    assert no_iframe == expected_result
