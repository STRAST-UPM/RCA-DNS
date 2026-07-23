# external imports
import pandas as pd
# internal imports
from src.providers.ripeatlas_provider import RIPEAtlasProvider
from src.utilities.utils import (
    get_filepaths_from_folder,
    json_file_to_list,
    dict_to_json_file
)
from src.utilities.constants import (
    CAMPAIGN_RESULTS_FOLDER_PATH,
    CAMPAIGN_RESULTS_RESUME_FILEPATH,
    CAMPAIGN_ANALYSIS_REPORT_FILEPATH,
    RCA_DNS_IPS,
    GOOD_RESPONSE_TIME_LIMIT_MS,
    MID_RESPONSE_TIME_LIMIT_MS
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
        print(f"Extracting data from file: {result_file}")
        results_list = json_file_to_list(result_file)
        for result in results_list:
            result_dict = extract_data_from_result(result)
            results_df.loc[len(results_df)] = result_dict

    results_df.to_csv(CAMPAIGN_RESULTS_RESUME_FILEPATH, index=False)
            

def extract_data_from_result(result: dict):
    if "err" in result["result"][0].keys():
        source_address = ""
        rtt = -1
        response_code = 408
        headers_size = -1
        body_size = -1
    else:
        source_address = result["result"][0]["src_addr"]
        rtt = result["result"][0]["rt"]
        response_code = result["result"][0]["res"]
        headers_size = result["result"][0]["hsize"]
        body_size = result["result"][0]["bsize"]

    return {
        "measurement_id":result["msm_id"],
        "probe_id":result["prb_id"],
        "timestamp":result["timestamp"],
        "rca-dns-domain":RCA_DNS_IPS[result["result"][0]["dst_addr"]],
        "uri":result["uri"],
        "source_address":source_address,
        "destination_address":result["result"][0]["dst_addr"],
        "rtt":rtt,
        "response_code": response_code,
        "headers_size": headers_size,
        "body_size": body_size,
    }


if __name__ == "__main__":
    # print("Obtaining measurements results")
    # ripe_atlas_provider = RIPEAtlasProvider()
    # ripe_atlas_provider.get_campaign_results()

    # print("Creating resume from results data")
    # create_results_resume()

    print("Generating analysis report")
    results_df = pd.read_csv(CAMPAIGN_RESULTS_RESUME_FILEPATH)
    objective_domains = results_df["rca-dns-domain"].unique().tolist()
    report_data = {}
    for objective_domain in objective_domains:
        report_data[objective_domain] = {}

    dict_to_json_file(
        report_data,
        CAMPAIGN_ANALYSIS_REPORT_FILEPATH
    )
