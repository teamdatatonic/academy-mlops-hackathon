from kfp.components import load_component_from_file
from pathlib import Path

PIPELINE_COMPONENTS_DIR = Path(__file__).parents[2] / "pipeline_components"

# _tensorflow components

train_tensorflow_model = load_component_from_file(
    str(
        PIPELINE_COMPONENTS_DIR
        / "_tensorflow"
        / "_tensorflow"
        / "train"
        / "component.yaml"
    )
)

predict_tensorflow_model = load_component_from_file(
    str(
        PIPELINE_COMPONENTS_DIR
        / "_tensorflow"
        / "_tensorflow"
        / "predict"
        / "component.yaml"
    )
)

# aiplatform components

custom_train_job = load_component_from_file(
    str(
        PIPELINE_COMPONENTS_DIR
        / "aiplatform"
        / "aiplatform"
        / "custom_train_job"
        / "component.yaml"
    )
)

model_batch_predict = load_component_from_file(
    str(
        PIPELINE_COMPONENTS_DIR
        / "aiplatform"
        / "aiplatform"
        / "model_batch_predict"
        / "component.yaml"
    )
)

update_best_model = load_component_from_file(
    str(
        PIPELINE_COMPONENTS_DIR
        / "aiplatform"
        / "aiplatform"
        / "update_best_model"
        / "component.yaml"
    )
)

import_model_evaluation = load_component_from_file(
    str(
        PIPELINE_COMPONENTS_DIR
        / "aiplatform"
        / "aiplatform"
        / "import_model_evaluation"
        / "component.yaml"
    )
)

# bigquery components

extract_bq_to_dataset = load_component_from_file(
    str(
        PIPELINE_COMPONENTS_DIR
        / "bigquery"
        / "bigquery"
        / "extract_dataset"
        / "component.yaml"
    )
)

bq_query_to_table = load_component_from_file(
    str(
        PIPELINE_COMPONENTS_DIR
        / "bigquery"
        / "bigquery"
        / "query_to_table"
        / "component.yaml"
    )
)

load_dataset_to_bq = load_component_from_file(
    str(
        PIPELINE_COMPONENTS_DIR
        / "bigquery"
        / "bigquery"
        / "upload_prediction"
        / "component.yaml"
    )
)
