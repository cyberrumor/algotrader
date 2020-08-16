# algotrader

Pulls target stock data from Yahoo finance, plots bollingerbands and a following stop loss.

<img src="/screenshot.jpg">

Many of the formulas could have been implimented via a module like numpy, but I chose to write them out manually as this is mostly to help me practice.

# Implimented features

- Following stop loss based on parabolic SAR
- Bollinger bands

# Planned features

- Dynamic choice of strategy based on Hurst exponent (and possibly other fractal data measurements).
- Automated choice in stocks based on:
- - Risk/reward ratio comparison (using Sharpe filter).
- - Portfolio optimization (using Kalman filtering).
- - Confidence in patern recognition (using Augmented Dickey Fuller tests).
