# external imports
import pandas as pd
import numpy as np
# internal imports
from src.utilities.utils import (
    json_file_to_list,
    get_filepaths_from_folder
)
from src.utilities.constants import (
    WORLD_COUNTRY_CODES_LIST_FILEPATH,
    AFRICA_COUNTRY_CODES_LIST_FILEPATH,
    AMERICA_COUNTRY_CODES_LIST_FILEPATH,
    ASIA_COUNTRY_CODES_LIST_FILEPATH,
    EUROPE_COUNTRY_CODES_LIST_FILEPATH,
    OCEANIA_COUNTRY_CODES_LIST_FILEPATH,
    CAMPAIGN_RESULTS_FOLDER_PATH,
    CAMPAIGN_RESULTS_RESUME_FILEPATH,
    RCA_DNS_IPS,
    BASE_DOMAIN,
    GOOD_RESPONSE_TIME_LIMIT_MS,
    MID_RESPONSE_TIME_LIMIT_MS
)


class AnalysisModule:
    def __init__(self):
        southamerica_countries = json_file_to_list(AMERICA_COUNTRY_CODES_LIST_FILEPATH)
        southamerica_countries.remove("CA")
        southamerica_countries.remove("MX")
        southamerica_countries.remove("US")
        self._domains_to_country_codes = {
            f"global.{BASE_DOMAIN}":json_file_to_list(WORLD_COUNTRY_CODES_LIST_FILEPATH),
            f"africa.{BASE_DOMAIN}":json_file_to_list(AFRICA_COUNTRY_CODES_LIST_FILEPATH),
            f"asia.{BASE_DOMAIN}":json_file_to_list(ASIA_COUNTRY_CODES_LIST_FILEPATH),
            f"australia.{BASE_DOMAIN}":json_file_to_list(OCEANIA_COUNTRY_CODES_LIST_FILEPATH),
            f"europe.{BASE_DOMAIN}":json_file_to_list(EUROPE_COUNTRY_CODES_LIST_FILEPATH),
            f"northamerica.{BASE_DOMAIN}":["MX","CA"],
            f"us.{BASE_DOMAIN}":southamerica_countries,
            f"southamerica.{BASE_DOMAIN}":["US"],
        }

    # Analysis functions
    def create_results_resume(self):
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
                        result_dict = self.extract_data_from_result(result)
                        results_df.loc[len(results_df)] = result_dict
        
                results_df.to_csv(CAMPAIGN_RESULTS_RESUME_FILEPATH, index=False)

    def extract_data_from_result(self, result: dict):
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

    def generate_dict_report_for_domain(
        self,
        domain_results_df: pd.DataFrame
    ) -> dict[str:any]:
        total_measurements_count = int(domain_results_df["rtt"].count())
        rtt_values_ordered = domain_results_df.loc[
            domain_results_df["rtt"] != -1, 
            "rtt"
        ].sort_values()
        valid_measurements_count = len(rtt_values_ordered)

        # General statistics for domain
        measurement_errors_count = int(domain_results_df.loc[
            domain_results_df["rtt"] == -1,
            "rtt"
        ].count())
        rtt_max = np.max(rtt_values_ordered)
        rtt_min = np.min(rtt_values_ordered)
        rtt_mean = np.mean(rtt_values_ordered)
        rtt_median = np.median(rtt_values_ordered)
        rtt_percentile_90 = np.percentile(rtt_values_ordered, 90)

        # RTTs threshold for good service
        rtts_above_good_count = int(
            (rtt_values_ordered <= GOOD_RESPONSE_TIME_LIMIT_MS).sum()
        )
        rtts_above_good_percentage = 100*(rtts_above_good_count / valid_measurements_count)
        rtts_above_mid_count = int(
            (rtt_values_ordered <= MID_RESPONSE_TIME_LIMIT_MS).sum()
        )
        rtts_above_mid_percentage = 100*(rtts_above_mid_count / valid_measurements_count)
        
        return {
            "total_measurements": total_measurements_count,
            "valid_measurements_count": valid_measurements_count,
            "measurement_errors_count": measurement_errors_count,
            "rtt_max": rtt_max,
            "rtt_min": rtt_min,
            "rtt_mean": rtt_mean,
            "rtt_median": rtt_median,
            "rtt_percentile_90": rtt_percentile_90,
            "rtts_above_good_count": rtts_above_good_count,
            "rtts_above_good_percentage": rtts_above_good_percentage,
            "rtts_above_mid_count": rtts_above_mid_count,
            "rtts_above_mid_percentage": rtts_above_mid_percentage,
        }
