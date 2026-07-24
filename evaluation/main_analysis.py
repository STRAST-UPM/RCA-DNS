# external imports
import pandas as pd
import numpy as np
# internal imports
from src.providers.ripeatlas_provider import RIPEAtlasProvider
from src.modules.analysis_module import AnalysisModule
from src.modules.graphics_module import GraphicsModule
from src.utilities.utils import (
    dict_to_json_file
)
from src.utilities.constants import (
    CAMPAIGN_RESULTS_RESUME_FILEPATH,
    CAMPAIGN_ANALYSIS_REPORT_FILEPATH,
)


if __name__ == "__main__":
    ripe_atlas_provider = RIPEAtlasProvider()
    analysis_module = AnalysisModule()
    graphics_module = GraphicsModule()

    # print("Obtaining measurements results")
    # ripe_atlas_provider.get_campaign_results()

    # print("Creating resume from results data")
    # analysis_module.create_results_resume()

    print("Generating analysis report")
    analysis_module.generate_results_report(
        results_resume_filepath=CAMPAIGN_RESULTS_RESUME_FILEPATH
    )
    analysis_module.generate_cdfs_for_regions_in_domains(
        results_resume_filepath=CAMPAIGN_RESULTS_RESUME_FILEPATH
    )
