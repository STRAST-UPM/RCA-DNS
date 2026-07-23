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
    results_df = pd.read_csv(CAMPAIGN_RESULTS_RESUME_FILEPATH)
    objective_domains = results_df["rca-dns-domain"].unique().tolist()
    report_data = {}
    for objective_domain in objective_domains:
        print(f"Creating report for domain: {objective_domain}")

        report_data[objective_domain] = analysis_module.generate_dict_report_for_domain(
            results_df.loc[
                results_df["rca-dns-domain"] == objective_domain
            ].copy()
        )

        print(f"Finished report for domain: {objective_domain}")
        
    dict_to_json_file(
        report_data,
        CAMPAIGN_ANALYSIS_REPORT_FILEPATH
    )
