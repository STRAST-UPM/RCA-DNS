# external imports
import matplotlib.pyplot as plt
import numpy as np
# internal imports
from src.utilities.constants import (
    GOOD_RESPONSE_TIME_LIMIT_MS,
    MID_RESPONSE_TIME_LIMIT_MS
)


class GraphicsModule():
    def __init__(self):
        pass

    def rtts_cds(
        rtt_mean: float,
        rtt_median: float,
        rtt_ordered_values: list[int],
        outliers_limit: int,
        filepath_to_save: str,
    ):
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
            where=( (rtt_ordered_values > GOOD_RESPONSE_TIME_LIMIT_MS) & (rtt_ordered_values <= MID_RESPONSE_TIME_LIMIT_MS) ),
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
        plt.title(f"CDF of RTT observed in the region-constrained deployment")

        plt.xlim(xmax=outliers_limit)
        plt.ylim(0, 1)

        # Plot vertical lines for median and mean
        plt.axvline(x=rtt_mean, color='black', linestyle='--', alpha=0.5, label=f'Mean: {rtt_mean:.0f}')

        plt.legend()
        plt.tight_layout()
        plt.savefig(filepath_to_save)
        plt.close()
