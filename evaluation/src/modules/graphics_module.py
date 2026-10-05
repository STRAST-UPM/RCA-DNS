# external imports
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import pandas as pd
# internal imports
from src.utilities.constants import (
    GOOD_RESPONSE_TIME_LIMIT_MS,
    MID_RESPONSE_TIME_LIMIT_MS,
    RCA_DNS_REGION_COLORS,
    GC_LOCATIONS,
    GC_LOCATIONS_BY_REGION
)
from src.utilities.utils import (
    create_directory_structure
)


class GraphicsModule():
    def __init__(self):
        pass

    def generate_rtt_cdf(
        self,
        rtt_mean: float,
        rtt_ordered_values: pd.Series,
        outliers_limit: int,
        title: str,
        filepath_to_save: str,
    ):
        if rtt_ordered_values.empty:
            raise ValueError("rtt_ordered_values cannot be empty")

        plt.figure(figsize=(10, 6))

        cumulative_probabilities = np.arange(1,
            len(rtt_ordered_values) + 1) / len(rtt_ordered_values)
        plt.plot(rtt_ordered_values, cumulative_probabilities, 'b-', linewidth=2)
        plt.fill_between(
            rtt_ordered_values,
            cumulative_probabilities,
            1,
            where=(rtt_ordered_values <= GOOD_RESPONSE_TIME_LIMIT_MS),
            interpolate=True,
            color='green',
            alpha=0.18,
            label=f'Upper area ≤ {GOOD_RESPONSE_TIME_LIMIT_MS:.0f} ms'
        )
        plt.fill_between(
            rtt_ordered_values,
            cumulative_probabilities,
            1,
            where=((rtt_ordered_values > GOOD_RESPONSE_TIME_LIMIT_MS) & (rtt_ordered_values <= MID_RESPONSE_TIME_LIMIT_MS)),
            interpolate=True,
            color='yellow',
            alpha=0.18,
            label=f'Upper area ≤ {MID_RESPONSE_TIME_LIMIT_MS:.0f} ms'
        )
        plt.fill_between(
            rtt_ordered_values,
            cumulative_probabilities,
            1,
            where=(rtt_ordered_values > MID_RESPONSE_TIME_LIMIT_MS),
            interpolate=True,
            color='red',
            alpha=0.18,
            label=f'Upper area > {MID_RESPONSE_TIME_LIMIT_MS:.0f} ms'
        )
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xlabel(f"RTT in ms")
        plt.ylabel('Cumulative Probability')
        # plt.title(title)

        plt.xlim(
            xmin=float(rtt_ordered_values.iloc[0]),
            xmax=float(outliers_limit)
        )
        plt.ylim(0, 1)

        # Plot vertical lines for median and mean
        plt.axvline(x=rtt_mean, color='black', linestyle='--', alpha=0.5, label=f'Mean: {rtt_mean:.0f}')

        plt.legend()
        plt.tight_layout()
        create_directory_structure(filepath_to_save)
        plt.savefig(filepath_to_save)
        plt.close()

    @staticmethod
    def geo_layout_borders_in_purple(fig: go.Figure, fitbounds: bool = False):
        fig.update_geos(
            visible=False,
            resolution=50,
            showcountries=True,
            countrycolor="RebeccaPurple",
            projection_type="natural earth",
            fitbounds="locations" if fitbounds else False
        )

    def generate_gc_locations_map(
        self,
        filepath_to_save: str,
        region_countries: dict[str, set[str]] | None = None,
        iso2_to_iso3: dict[str, str] | None = None,
        width: int = 1600,
        height: int = 800,
        scale: int = 2,
    ):
        """
        World map with the Google Cloud locations of the RCA-DNS prototype,
        coloured by the regional deployment to which they belong.

        If region_countries (region -> ISO alpha-2 codes) and iso2_to_iso3 are
        given, the countries whose probes are considered inside each region are
        shaded with a light version of the region colour.
        """
        fig = go.Figure()

        # Optional background layer: countries assigned to each region
        if region_countries and iso2_to_iso3:
            for region, countries in region_countries.items():
                color = RCA_DNS_REGION_COLORS[region]
                iso3_codes = [
                    iso2_to_iso3[code] for code in sorted(countries)
                    if code in iso2_to_iso3
                ]
                fig.add_trace(go.Choropleth(
                    locations=iso3_codes,
                    locationmode="ISO-3",
                    z=[1] * len(iso3_codes),
                    colorscale=[[0, color], [1, color]],
                    showscale=False,
                    marker_opacity=0.18,
                    marker_line_color="RebeccaPurple",
                    marker_line_width=0.5,
                    hoverinfo="skip",
                    showlegend=False,
                ))

        # Google Cloud locations, one trace per region (one legend entry each)
        for region, location_ids in GC_LOCATIONS_BY_REGION.items():
            fig.add_trace(go.Scattergeo(
                lon=[GC_LOCATIONS[loc]["lon"] for loc in location_ids],
                lat=[GC_LOCATIONS[loc]["lat"] for loc in location_ids],
                text=[GC_LOCATIONS[loc]["city"] for loc in location_ids],
                mode="markers",
                name=f"{region} ({len(location_ids)})",
                marker=dict(
                    size=11,
                    color=RCA_DNS_REGION_COLORS[region],
                    line=dict(width=1.2, color="white"),
                    symbol="circle",
                ),
            ))

        self.geo_layout_borders_in_purple(fig)
        # Hide Antarctica, as in the Hunter maps
        fig.update_geos(lataxis_range=[-58, 85])
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="white",
            legend=dict(
                orientation="h",
                yanchor="top", y=0.0,
                xanchor="center", x=0.5,
                font=dict(size=18),
                itemsizing="constant",
            ),
        )

        create_directory_structure(filepath_to_save)
        fig.write_image(filepath_to_save, width=width, height=height, scale=scale)

    def generate_probes_map(
        self,
        probes_info: list[dict],
        region_countries: dict[str, set[str]],
        filepath_to_save: str,
        outside_color: str = "#9E9E9E",
        width: int = 1600,
        height: int = 800,
        scale: int = 2,
    ):
        """
        World map with the RIPE Atlas probes used in the campaign, coloured by
        the region to which the country of each probe is assigned. Probes in
        countries not assigned to any region are drawn in grey.

        probes_info: probe objects returned by the RIPE Atlas API
                     (as stored in probes_info.json).
        region_countries: region name -> set of ISO alpha-2 country codes.
        """
        country_to_region = {
            country: region
            for region, countries in region_countries.items()
            for country in countries
        }

        # Group probe coordinates by region
        groups: dict[str, dict[str, list]] = {}
        skipped = 0
        for probe in probes_info:
            coordinates = (probe.get("geometry") or {}).get("coordinates")
            if not coordinates or len(coordinates) < 2:
                skipped += 1
                continue
            lon, lat = coordinates[0], coordinates[1]
            region = country_to_region.get(probe.get("country_code"), "outside")
            group = groups.setdefault(region, {"lon": [], "lat": [], "text": []})
            group["lon"].append(lon)
            group["lat"].append(lat)
            group["text"].append(f"{probe.get('id')} ({probe.get('country_code')})")

        if skipped:
            print(f"{skipped} probes without coordinates were not drawn")

        fig = go.Figure()

        # Probes outside every region first, so they stay in the background
        draw_order = ["outside"] + [r for r in RCA_DNS_REGION_COLORS if r != "outside"]
        for region in draw_order:
            if region not in groups:
                continue
            group = groups[region]
            label = "no region" if region == "outside" else region
            color = outside_color if region == "outside" else RCA_DNS_REGION_COLORS[region]
            fig.add_trace(go.Scattergeo(
                lon=group["lon"],
                lat=group["lat"],
                text=group["text"],
                mode="markers",
                name=f"{label} ({len(group['lon'])})",
                # "no region" is drawn first (background) but listed last
                legendrank=2000 if region == "outside" else 1000,
                marker=dict(
                    size=6,
                    color=color,
                    opacity=0.85,
                    line=dict(width=0.4, color="white"),
                ),
            ))

        self.geo_layout_borders_in_purple(fig)
        # Hide Antarctica, as in the other maps
        fig.update_geos(lataxis_range=[-58, 85])
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="white",
            legend=dict(
                orientation="h",
                yanchor="top", y=0.0,
                xanchor="center", x=0.5,
                font=dict(size=18),
                itemsizing="constant",
            ),
        )

        create_directory_structure(filepath_to_save)
        fig.write_image(filepath_to_save, width=width, height=height, scale=scale)
