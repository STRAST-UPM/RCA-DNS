# external imports
import pandas as pd
# internal imports
from src.providers.ripeatlas_provider import RIPEAtlasProvider
from src.utilities.utils import (
    get_filepaths_from_folder,
    json_file_to_list
)
from src.utilities.constants import (
    CAMPAIGN_RESULTS_FOLDER_PATH,
    CAMPAIGN_RESULTS_RESUME,
    RCA_DNS_IPS
)

# Analysis functions
def create_results_resume():
    results_filepaths = get_filepaths_from_folder(CAMPAIGN_RESULTS_FOLDER_PATH)
    results_df = pd.DataFrame(
        columns=[
            "measurement_id", "probe_id", "timestamp", 
            "rca-dns-domain", "uri", "source_address", "destination_address", 
            "rtt", "response_code", "headers_size", "body_size"
        ]
    )

    for result_file in results_filepaths:
        results_list = json_file_to_list(result_file)
        for result in results_list:
            result_dict = extract_data_from_result(result)
            

def extract_data_from_result(result: dict):
    return {
        "measurement_id":result["msm_id"],
        "probe_id":result["prb_id"],
        "timestamp":result["timestamp"],
        "rca-dns-domain":RCA_DNS_IPS[result["result"][0]["src_addr"]],
        "uri":result["uri"],
        "source_address":result["result"][0]["src_addr"],
        "destination_address":result["result"][0]["dst_addr"],
        "rtt":result["result"][0]["rt"],
        "response_code":result["result"][0]["res"],
        "headers_size":result["result"][0]["hsize"],
        "body_size":result["result"][0]["bsize"],
    }


if __name__ == "__main__":
    ripe_atlas_provider = RIPEAtlasProvider()
    ripe_atlas_provider.get_campaign_results()

    create_results_resume()
