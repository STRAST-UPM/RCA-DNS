# external imports
import pandas as pd
import numpy as np
# internal imports
from src.providers.ripeatlas_provider import RIPEAtlasProvider
from src.modules.analysis_module import AnalysisModule
from src.modules.graphics_module import GraphicsModule
from src.utilities.utils import (
    dict_to_json_file,
    json_file_to_dict,
    json_file_to_list
)
from src.utilities.constants import (
    CAMPAIGN_RESULTS_RESUME_FILEPATH,
    CAMPAIGN_ANALYSIS_REPORT_FILEPATH,
    CAMPAIGN_GRAPHICS_FOLDER_PATH,
    WORLD_COUNTRIES_INFO_DICT_FILEPATH,
    BASE_DOMAIN,
    CAMPAIGN_PROBES_INFO_FILEPATH
)


if __name__ == "__main__":
    get_results = False
    build_data_for_analysis = False
    generate_analysis_report = True
    generate_gc_locations_map = True
    generate_probes_map = True

    ripe_atlas_provider = RIPEAtlasProvider()
    analysis_module = AnalysisModule()
    graphics_module = GraphicsModule()

    if get_results:
        print("Obtaining measurements results")
        ripe_atlas_provider.get_campaign_results()

    if build_data_for_analysis:
        print("Creating resume from results data")
        analysis_module.create_results_resume()
        analysis_module.add_probes_country_code_to_results_resume()

    if generate_analysis_report:
        print("Generating analysis report")
        analysis_module.generate_results_report(
            results_resume_filepath=CAMPAIGN_RESULTS_RESUME_FILEPATH
        )
        analysis_module.generate_cdfs_for_regions_in_domains(
            results_resume_filepath=CAMPAIGN_RESULTS_RESUME_FILEPATH
        )

    if generate_gc_locations_map:
        print("Generating Google Cloud locations map")
        countries_info = json_file_to_dict(WORLD_COUNTRIES_INFO_DICT_FILEPATH)
        iso2_to_iso3 = {
            iso2: info["cca3"] for iso2, info in countries_info.items()
        }
        # region name -> set of ISO alpha-2 codes, reusing the analysis definitions
        region_countries = {
            domain.removesuffix(f".{BASE_DOMAIN}"): countries
            for domain, countries in analysis_module._domains_to_country_codes.items()
        }
        graphics_module.generate_gc_locations_map(
            filepath_to_save=f"{CAMPAIGN_GRAPHICS_FOLDER_PATH}/rcadns_gc_locations_map.png",
            region_countries=region_countries,
            iso2_to_iso3=iso2_to_iso3,
        )

    if generate_probes_map:
        print("Generating RIPE Atlas probes map")
        region_countries = {
            domain.removesuffix(f".{BASE_DOMAIN}"): countries
            for domain, countries in analysis_module._domains_to_country_codes.items()
        }
        graphics_module.generate_probes_map(
            probes_info=json_file_to_list(CAMPAIGN_PROBES_INFO_FILEPATH),
            region_countries=region_countries,
            filepath_to_save=f"{CAMPAIGN_GRAPHICS_FOLDER_PATH}/rcadns_ripe_probes_map.png",
        )
