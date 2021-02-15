import pytest
import json
import requests

PROD_API_URL = 'https://openpredict.semanticscience.org'

def test_get_predict():
    """Test predict API GET operation"""
    # url = PROD_API_URL + '/predict?drug_id=DRUGBANK:DB00394&model_id=openpredict-baseline-omim-drugbank&n_results=42'
    get_predictions = requests.get(PROD_API_URL + '/predict',
                        params={
                            'drug_id': 'DRUGBANK:DB00394',
                            'n_results': '42',
                            'model_id': 'openpredict-baseline-omim-drugbank'
                        }).json()
    assert 'hits' in get_predictions
    assert len(get_predictions['hits']) == 42
    assert get_predictions['count'] == 42
    assert get_predictions['hits'][0]['id'] == 'OMIM:246300'

def test_post_trapi():
    """Test Translator ReasonerAPI query POST operation to get predictions"""
    trapi_query = {
        "message": {
            # "n_results": 10,
            "query_graph": {
                "edges": {
                    "e01": {
                        "subject": "n0",
                        "object": "n1",
                        "predicate": "biolink:treated_by"
                    }
                },
                "nodes": {
                    "n0": {
                        "curie": "DRUGBANK:DB00394",
                        "category": "biolink:Drug"
                    },
                    "n1": {
                        "category": "biolink:Disease"
                    }
                }
            }
            # "query_options": {
            # "min_score": 0.5
            # }
        }
    }
    headers = {'Content-type': 'application/json'}
    trapi_results = requests.post(PROD_API_URL + '/query',
                        data=json.dumps(trapi_query), headers=headers).json()

    edges = trapi_results['knowledge_graph']['edges'].items()
    assert len(edges) == 300
    # assert edges[0]['object'] == 'OMIM:246300'