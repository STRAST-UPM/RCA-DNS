# external imports
import pandas as pd
import numpy as np
# internal imports
from src.modules.graphics_module import GraphicsModule
from src.utilities.utils import (
    json_file_to_set,
    json_file_to_list,
    dict_to_json_file,
    get_filepaths_from_folder,
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
    CAMPAIGN_ANALYSIS_REPORT_FILEPATH,
    CAMPAIGN_GRAPHICS_FOLDER_PATH,
    RCA_DNS_IPS,
    BASE_DOMAIN,
    GOOD_RESPONSE_TIME_LIMIT_MS,
    MID_RESPONSE_TIME_LIMIT_MS
)


class AnalysisModule:
    def __init__(self):
        self._domains_to_country_codes = {
            f"africa.{BASE_DOMAIN}": json_file_to_set(AFRICA_COUNTRY_CODES_LIST_FILEPATH),
            f"asia.{BASE_DOMAIN}": json_file_to_set(ASIA_COUNTRY_CODES_LIST_FILEPATH),
            f"australia.{BASE_DOMAIN}": json_file_to_set(OCEANIA_COUNTRY_CODES_LIST_FILEPATH),
            f"europe.{BASE_DOMAIN}": json_file_to_set(EUROPE_COUNTRY_CODES_LIST_FILEPATH),
            f"northamerica.{BASE_DOMAIN}": {"MX", "CA"},
            f"us.{BASE_DOMAIN}": {"US"},
            f"southamerica.{BASE_DOMAIN}": json_file_to_set(AMERICA_COUNTRY_CODES_LIST_FILEPATH) - {"MX", "CA", "US"},
        }
        self._world_countries_codes_list = json_file_to_set(WORLD_COUNTRY_CODES_LIST_FILEPATH)

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

    def generate_results_report(
        self,
        results_resume_filepath: str = CAMPAIGN_RESULTS_RESUME_FILEPATH,
    ):
        results_df = pd.read_csv(results_resume_filepath)
        objective_domains = results_df["rca-dns-domain"].unique().tolist()
        report_data = {}
        for objective_domain in objective_domains:
            print(f"Creating report for domain: {objective_domain}")
    
            report_data[objective_domain] = self._get_report_dict(
                results_df.loc[
                    results_df["rca-dns-domain"] == objective_domain
                ].copy()
            )

            if objective_domain in self._domains_to_country_codes.keys():            
                # Report or metrics from countries inside the region
                region_countries_set = self._domains_to_country_codes[objective_domain]
                region_report = self._get_report_dict(
                    results_df.loc[
                        results_df["rca-dns-domain"] == objective_domain,
                        # results_df["origin_country_code"].isin(region_countries_set)
                    ].copy()
                )
                region_report["countries_codes"] = list(region_countries_set)
                report_data[objective_domain]["inside_region_countries_report"] = region_report

                # Report or metrics from countries outside the region
                non_region_countries_set = self._world_countries_codes_list - region_countries_set
                region_report = self._get_report_dict(
                    results_df.loc[
                        results_df["rca-dns-domain"] == objective_domain,
                        # results_df["origin_country_code"].isin(non_region_countries_set)
                    ].copy()
                )
                region_report["countries_codes"] = list(non_region_countries_set)
                report_data[objective_domain]["outside_region_countries_report"] = region_report

            print(f"Finished report for domain: {objective_domain}")

        dict_to_json_file(
            dict_to_save=report_data,
            file_path=CAMPAIGN_ANALYSIS_REPORT_FILEPATH,
        )

    def _get_report_dict(
        self,
        results_df: pd.DataFrame
    ):
        total_measurements_count = int(results_df["rtt"].count())
        rtt_values_ordered = results_df.loc[
            results_df["rtt"] != -1, 
            "rtt"
        ].sort_values()
        valid_measurements_count = len(rtt_values_ordered)

        # General statistics for domain
        measurement_errors_count = int(results_df.loc[
            results_df["rtt"] == -1,
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

    def generate_cdfs_for_regions_in_domains(
        self,
        results_resume_filepath: str = CAMPAIGN_RESULTS_RESUME_FILEPATH,
    ):
        results_df = pd.read_csv(results_resume_filepath)
        objective_domains = results_df["rca-dns-domain"].unique().tolist()

        graphics = GraphicsModule()
        for objective_domain in objective_domains:
            print(f"Creating CDFs for domain: {objective_domain}")

            if objective_domain in self._domains_to_country_codes.keys():
                region_countries_set = self._domains_to_country_codes[objective_domain]
                non_region_countries_set = self._world_countries_codes_list - region_countries_set
                regions = [
                    (region_countries_set,
                    "CDF of RTT observed in the region-constrained countries deployment",
                    f"{objective_domain}_cdf_rtts_inside_region_contrained"),
                    (non_region_countries_set,
                    "CDF of RTT observed outside region-constrained countries deployment",
                    f"{objective_domain}_cdf_rtts_outside_region_contrained")
                ]
            else:
                regions = [
                    (self._world_countries_codes_list,
                    "CDF of RTT observed in the global region",
                    f"{objective_domain}_cdf_rtts"),
                ]

            for countries_set, title, filename in regions:
                domain_countries_results_df = results_df.loc[
                    results_df["rca-dns-domain"] == objective_domain,
                    # results_df["origin_country_code"].isin(countries_set)
                ].copy()

                rtt_values_ordered = domain_countries_results_df.loc[
                    domain_countries_results_df["rtt"] != -1, 
                    "rtt"
                ].sort_values()
                rtt_mean = np.mean(rtt_values_ordered)
                rtt_median = np.median(rtt_values_ordered)

                graphics.generate_rtt_cdf(
                    rtt_mean=rtt_mean,
                    rtt_median=rtt_median,
                    rtt_ordered_values=rtt_values_ordered,
                    outliers_limit=rtt_mean*5,
                    title=f"{title}",
                    filepath_to_save=f"{CAMPAIGN_GRAPHICS_FOLDER_PATH}/{filename}.png",
                )

            print(f"Finished CDFs for domain: {objective_domain}")
