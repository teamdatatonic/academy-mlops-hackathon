# Copyright 2022 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kfp.v2.dsl import component
from pathlib import Path


@component(
    base_image="python:3.7",
    packages_to_install=["google-cloud-bigquery==2.30.0"],
    output_component_file=str(Path(__file__).with_suffix(".yaml")),
)
def load_dataset_to_bq(
    bq_client_project_id: str,
    destination_project_id: str,
    dataset_id: str,
    table_name: str,
    gcs_source_uri: str,
    dataset_location: str = "EU",
) -> None:
    """
    Load datasets in JSONL format (e.g. results of batch prediction) to bigquery

    Args:
        bq_client_project_id (str): project id that will be used by the bq client
        destination_project_id (str): project id where BQ table will be created
        dataset_id (str): dataset id where BQ table will be created
        table_name (str): table name (without project id and dataset id)
        gcs_source_uri (str): gs:// URI of input files
        dataset_location (str): bq dataset location. Defaults to "EU".

    Returns:
        None
    """
    from google.cloud import bigquery
    import logging
    from pathlib import Path

    logging.getLogger().setLevel(logging.INFO)

    client = bigquery.Client(project=bq_client_project_id)

    table_id = f"{destination_project_id}.{dataset_id}.{table_name}"

    # find predictions folder
    parent = Path(gcs_source_uri.replace("gs://", "/gcs/"))
    children = list(parent.glob("prediction-*"))
    if len(children) != 1:
        raise RuntimeError(
            f"Can't find single prediction folder in {gcs_source_uri}. "
            f"Found {children}"
        )
    gcs_source_uri = str(children[0] / "prediction.results-*").replace("/gcs/", "gs://")

    logging.info(f"loading data from GCS location: {gcs_source_uri}")
    logging.info(f"destination table in BQ: {table_id}")

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    # Make an API request.
    load_job = client.load_table_from_uri(
        gcs_source_uri,
        table_id,
        location=dataset_location,
        job_config=job_config,
    )

    # Waits for the job to complete.
    job_result = load_job.result()

    if job_result.done():
        logging.info("BQ job finished")
    else:
        logging.error(job_result.exception())
        raise RuntimeError(job_result.exception())
