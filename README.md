# algotrader

Pulls target stock data from Yahoo finance, plots bollingerbands and a following stop loss.

<img src="/screenshot.jpg">

Many of the formulas could have been implimented via a module like numpy, but I chose to write them out manually as this is mostly to help me practice.

# Implimented features

- Following stop loss based on parabolic SAR
- Bollinger bands

# Planned features

- Kalman filtering of various signals.
- Given more than one stock, a recommendation on which to purchase.
- Auto diversification.
- Automatic buys and sells.
- Comparison of held positions to market as a whole, to help decide whether to panic sell.
- Live stats.
