[![Test production API](https://github.com/MaastrichtU-IDS/translator-openpredict/actions/workflows/run-tests-prod.yml/badge.svg)](https://github.com/MaastrichtU-IDS/translator-openpredict/actions/workflows/run-tests-prod.yml) [![Run tests](https://github.com/MaastrichtU-IDS/translator-openpredict/actions/workflows/run-tests.yml/badge.svg)](https://github.com/MaastrichtU-IDS/translator-openpredict/actions/workflows/run-tests.yml) [![CodeQL analysis](https://github.com/MaastrichtU-IDS/translator-openpredict/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/MaastrichtU-IDS/translator-openpredict/actions/workflows/codeql-analysis.yml)

[![Python versions](https://img.shields.io/pypi/pyversions/openpredict)](https://pypi.org/project/openpredict) [![Version](https://img.shields.io/pypi/v/openpredict)](https://pypi.org/project/openpredict) [![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=MaastrichtU-IDS_translator-openpredict&metric=coverage)](https://sonarcloud.io/dashboard?id=MaastrichtU-IDS_translator-openpredict) [![SonarCloud Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=MaastrichtU-IDS_translator-openpredict&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=MaastrichtU-IDS_translator-openpredict) [![CII Best  Practices](https://bestpractices.coreinfrastructure.org/projects/4382/badge)](https://bestpractices.coreinfrastructure.org/projects/4382)

**OpenPredict** is a Python library and API to train and serve predicted biomedical entities associations (e.g. disease treated by drug). 

Metadata about runs, models evaluations, features are stored using the [ML Schema ontology](http://ml-schema.github.io/documentation/ML%20Schema.html) in a RDF triplestore (such as Ontotext GraphDB, or Virtuoso).

Access the **Translator OpenPredict API** at **[https://openpredict.semanticscience.org 🔮🐍](https://openpredict.semanticscience.org)**

> You can use this API to retrieve predictions for drug/disease, or add new embeddings to improve the model.

# Deploy the OpenPredict API locally :woman_technologist:

> Requirements: Python 3.6+ and `pip` installed

You can install the `openpredict` python package with `pip` to run the OpenPredict API on your machine, to test new embeddings or improve the library.

We currently recommend to install from the source code `master` branch to get the latest version of OpenPredict. But we also regularly publish the `openpredict` package to PyPI: https://pypi.org/project/openpredict

### Install from the source code :inbox_tray:

Clone the repository:

```bash
git clone https://github.com/MaastrichtU-IDS/translator-openpredict.git
cd translator-openpredict
```

Install `openpredict` from the source code, the package will be automatically updated when the files changes locally :arrows_counterclockwise:

```bash
pip3 install -e .
```

#### Optional: isolate with a Virtual Environment

If you face conflicts with already installed packages, then you might want to use a [Virtual Environment](https://docs.python.org/3/tutorial/venv.html) to isolate the installation in the current folder before installing OpenPredict:

```bash
# Create the virtual environment folder in your workspace
python3 -m venv .venv
# Activate it using a script in the created folder
source .venv/bin/activate
```

> On Windows you might also need to install [Visual Studio C++ 14 Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (required for `numpy`)

### Start the OpenPredict API :rocket:

Start locally the OpenPredict API on http://localhost:8808

```bash
openpredict start-api
```

By default all data are stored in the `data/` folder in the directory were you used the `openpredict` command (RDF metadata, features and models of each run)

> Contributions are welcome! If you wish to help improve OpenPredict, see the [instructions to contribute :woman_technologist:](/CONTRIBUTING.md)

### Reset your local OpenPredict data :wastebasket:

You can easily reset the data of your local OpenPredict deployment by deleting the `data/` folder and restarting the OpenPredict API:

```bash
rm -rf data/
```

> If you are working on improving OpenPredict, you can explore [additional documentation to deploy the OpenPredict API](https://github.com/MaastrichtU-IDS/translator-openpredict/tree/master/docs) locally or with Docker.

### Test the OpenPredict API

See the [`TESTING.md`](/TESTING.md) file for more details on testing the API.

---

# Use the API​ :mailbox_with_mail:


The user provides a drug or a disease identifier as a CURIE (e.g. DRUGBANK:DB00394, or OMIM:246300), and choose a prediction model (only the `Predict OMIM-DrugBank` classifier is currently implemented). 

The API will return predicted targets for the given drug or disease:

* The **potential drugs treating a given disease** :pill:
* The **potential diseases a given drug could treat** :microbe:

> Feel free to try the API at **[openpredict.semanticscience.org](https://openpredict.semanticscience.org)**

### Notebooks examples :notebook_with_decorative_cover:

We provide [Jupyter Notebooks](https://jupyter.org/) with examples to use the OpenPredict API:

1. [Query the OpenPredict API](https://github.com/MaastrichtU-IDS/translator-openpredict/blob/master/docs/openpredict-examples.ipynb)
2. [Generate embeddings with pyRDF2Vec](https://github.com/MaastrichtU-IDS/translator-openpredict/blob/master/docs/openpredict-pyrdf2vec-embeddings.ipynb), and import them in the OpenPredict API

### Add embedding :station:

The default baseline model is `openpredict-baseline-omim-drugbank`. You can choose the base model when you post a new embeddings using the `/embeddings` call. Then the OpenPredict API will:

1. add embeddings to the provided model
2. train the model with the new embeddings
3. store the features and model using a unique ID for the run (e.g. `7621843c-1f5f-11eb-85ae-48a472db7414`)

Once the embedding has been added you can find the existing models previously generated (including `openpredict-baseline-omim-drugbank`), and use them as base model when you ask the model for prediction or add new embeddings.

### Predict operation :crystal_ball:

Use this operation if you just want to easily retrieve predictions for a given entity. The `/predict` operation takes 4 parameters (1 required):

* A `drug_id` to get predicted diseases it could treat (e.g. `DRUGBANK:DB00394`)
  * **OR** a `disease_id` to get predicted drugs it could be treated with (e.g. `OMIM:246300`)
* The prediction model to use (default to `Predict OMIM-DrugBank`)
* The minimum score of the returned predictions, from 0 to 1 (optional)
* The limit of results to return, starting from the higher score, e.g. 42 (optional)  

The API will return the list of predicted target for the given entity, the labels are resolved using the [Translator Name Resolver API](http://robokop.renci.org:2434/docs#/lookup/lookup_curies_lookup_post):

```json
{
  "count": 300,
  "hits": [
    {
      "score": 0.8361061489249737,
      "id": "OMIM:246300",
      "label": "leprosy, susceptibility to, 3",
      "type": "disease"
    }
  ]
}
```

> Try it at [https://openpredict.semanticscience.org/predict?drug_id=DRUGBANK:DB00394](https://openpredict.semanticscience.org/predict?drug_id=DRUGBANK:DB00394)

### Query operation :email:

The `/query` operation will return the same predictions as the `/predict` operation, using the [ReasonerAPI](https://github.com/NCATSTranslator/ReasonerAPI) format, used within the [Translator project](https://ncats.nih.gov/translator/about).

The user sends a [ReasonerAPI](https://github.com/NCATSTranslator/ReasonerAPI) query asking for the predicted targets given: a source, and the relation to predict. The query is a graph with nodes and edges defined in JSON, and uses classes from the [BioLink model](https://biolink.github.io/biolink-model).

See this [ReasonerAPI](https://github.com/NCATSTranslator/ReasonerAPI) query example:

```json
{
  "message": {
    "query_graph": {
      "edges": [
        {
          "id": "e00",
          "source_id": "n00",
          "target_id": "n01",
          "type": "treated_by"
        }
      ],
      "nodes": [
        {
          "curie": "DRUGBANK:DB00394",
          "id": "n00",
          "type": "drug"
        },
        {
          "id": "n01",
          "type": "disease"
        }
      ]
    }
  }
}
```

The results provides the following attributes for the `knowledge_graph` edges:

```python
     "e0": {
        "attributes": [
          {
            "name": "model_id",
            "source": "OpenPredict",
            "type": "EDAM:data_1048",
            "value": "openpredict-baseline-omim-drugbank"
          },
          {
            "name": "score",
            "source": "OpenPredict",
            "type": "EDAM:data_1772",
            "value": "0.8267106697312154"
          }
        ],
        "object": "DRUGBANK:DB00394",
        "predicate": "biolink:treated_by",
        "relation": "RO:0002434",
        "subject": "OMIM:246300"
      },
```

### Predicates operation :world_map:

The `/predicates` operation will return the entities and relations provided by this API in a JSON object (following the [ReasonerAPI](https://github.com/NCATSTranslator/ReasonerAPI) specifications).

> Try it at [https://openpredict.semanticscience.org/predicates](https://openpredict.semanticscience.org/predicates)

---

# More about the data model :minidisc:

* The gold standard for drug-disease indications has been retrieved from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3159979
* Metadata about runs, models evaluations, features are stored using the [ML Schema ontology](http://ml-schema.github.io/documentation/ML%20Schema.html) in a RDF triplestore (Ontotext GraphDB).
  * See the [ML Schema documentation](http://ml-schema.github.io/documentation/ML%20Schema.html) for more details on the data model.

Diagram of the data model used for OpenPredict, based on the ML Schema ontology (`mls`):

![OpenPredict datamodel](https://raw.githubusercontent.com/MaastrichtU-IDS/translator-openpredict/master/docs/OpenPREDICT_datamodel.jpg)

---

# Acknowledgments​

* This service has been built from the [fair-workflows/openpredict](https://github.com/fair-workflows/openpredict) project.
* Predictions made using the [PREDICT method](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3159979/).
* Service funded by the [NIH NCATS Translator project](https://ncats.nih.gov/translator/about). 

![Funded the the NIH NCATS Translator project](https://ncats.nih.gov/files/TranslatorGraphic2020_1100x420.jpg)

