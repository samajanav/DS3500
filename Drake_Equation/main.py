"""
Homework 4
Simulation and Modeling
Janav Sama
"""

from drv import DRV

num_samples = 1000

def main():
    R_star_range = DRV(type='uniform', min_max=(1.5, 3), bins=5)
    fp_range = DRV(type='uniform', min_max=(0, 1.0), bins=5)
    ne_range = DRV(type='uniform', min_max=(1, 5), bins=5)
    fl_range = DRV(type='normal', mean_std=(0.3, 0.1), min_max=(0, 1), bins=5, num_samples=num_samples)
    fi_range = DRV(dist={1 / 8: 1})
    fc_range = DRV(type='normal', mean_std=(0.5, 0.1), min_max=(0, 1), bins=5, num_samples=num_samples)
    L_range = DRV(type='normal', mean_std=(10000, 5000), min_max=(0, 1000000), bins=5, num_samples=num_samples)

    # Multiplying the distributions
    N_dist = R_star_range.multiply(fp_range).multiply(ne_range).multiply(fl_range).multiply(fi_range).multiply(
        fc_range).multiply(L_range)
    N_dist.plot(title='Distribution of N', show_cumulative=True, log_scale=True)

    print("Expected Value of N:", N_dist.expected_value())
    print("Standard Deviation of N:", N_dist.standard_deviation())


if __name__ == '__main__':
    main()
