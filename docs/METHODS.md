# Metric decisions

- eFG = (FGM + 0.5 × 3PM) / FGA. For a season or filter selection, **sum numerators and denominators first**. Do not average percentages.
- Estimated team possessions = FGA − ORB + TOV + 0.475 × FTA. Average IU and opponent estimates to get a shared game denominator. The 0.475 coefficient is a college-basketball approximation; label it and test 0.44 as a sensitivity check. Play-by-play possession counting would be an extension.
- Offensive rating = 100 × points / estimated possessions; defensive rating uses opponent points. Net rating is their difference.
- Pace per 40 minutes = estimated possessions × 40 / (40 + 5 × overtime periods).
- Player PPG uses games played; points per 40 uses minutes. Default ranking eligibility is 100 total minutes; expose the threshold and sample size.
- A zero denominator produces a missing value, not 0%.

Before Week 3, write one claim, e.g. “IU's home net rating exceeded its away net rating in this season.” Report the difference and game counts. Do not claim a home-court causal effect: opponent mix and schedule differ. The starter bootstraps games to estimate uncertainty around the season ratio of total margin to total possessions; it is not a home/away significance test. Implement the two-group comparison only after predefining it, and review small samples and dependence.

Bootstrap 2,000 resamples locally, then 20,000 on a compute node if runtime justifies it. Resample complete games, not player rows. Examine stability over five seeds. Consecutive games may be dependent; add a short-block sensitivity analysis if the team has time. Intervals describe sampling assumptions, not a guarantee about future seasons.

No predictive model is required. A clean statistical comparison and interpretable dashboard meet this project's learning goals.
