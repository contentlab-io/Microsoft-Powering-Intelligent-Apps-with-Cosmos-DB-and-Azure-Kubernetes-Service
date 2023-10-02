import os
import azure.cosmos.cosmos_client as cosmos_client

class CosmosDBHelper:
  def __init__(self):
    self.cosmos_database_id = os.environ["COSMOS_DATABASE_ID"]
    self.cosmos_image_analysis_container_id = os.environ["COSMOS_IMAGE_ANALYSIS_CONTAINER_ID"]
    self.cosmos_aggregate_results_container_id = os.environ["COSMOS_AGGREGATE_RESULTS_CONTAINER_ID"]
    cosmos_account_host = os.environ["COSMOS_ACCOUNT_HOST"]
    cosmos_account_key = os.environ["COSMOS_ACCOUNT_KEY"]
    self.client = cosmos_client.CosmosClient(cosmos_account_host, {'masterKey': cosmos_account_key})
    self.db = self.client.get_database_client(self.cosmos_database_id)
    self.image_analysis_container = self.db.get_container_client(self.cosmos_image_analysis_container_id)
    self.aggregate_results_container = self.db.get_container_client(self.cosmos_aggregate_results_container_id)

  def create_analysis(self, document):
    return self.image_analysis_container.upsert_item(document)

  def create_aggregate_result(self, inserted_id, aggregate_result):
    entity = {
      "id": inserted_id,
      "sum": float(aggregate_result["sum"]),
      "average": float(aggregate_result["average"]),
      "median": float(aggregate_result["median"]),
      "min": float(aggregate_result["min"]),
      "max": float(aggregate_result["max"])
    }
    return self.aggregate_results_container.upsert_item(entity)
