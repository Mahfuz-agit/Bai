from app.core.pipeline import CognitivePipeline
from app.providers.mock import MockProvider
from app.schemas.contracts import InputCase


def test_pipeline_contract():
    result = CognitivePipeline(MockProvider()).run(
        InputCase(case_id="t1", content="One observation. Another observation.")
    )
    assert result.case_id == "t1"
    assert result.decomposition
    assert result.synthesis
