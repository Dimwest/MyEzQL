from output.json import to_json
from output.mermaid import Mermaid
from tests.utils import OUTPUT_TEST_INPUT, JSON_OUTPUT_EXPECTED, MERMAID_EXPECTED


def test_output_json():
    """
    Ensure that transformation of results into JSON returns
    expected result, without creating a file.
    """
    assert to_json(OUTPUT_TEST_INPUT, None) == JSON_OUTPUT_EXPECTED


def test_output_mermaid():
    """
    Ensure that tables_chart function returns expected HTML code,
    without creating a file.
    """
    m = Mermaid(OUTPUT_TEST_INPUT)
    assert m.tables_chart(None).string == MERMAID_EXPECTED.string
