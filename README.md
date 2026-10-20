# TWS Option Pipeline

Pipeline für Option Greeks (Delta, Gamma, Theta, Vega, IV) + Market Data (Bid/Ask/Volume) via IBKR TWS Socket API (Port 7496).

## Struktur

```
tws_option_pipline_two-1/
├── README.md
├── venv/                    # Python virtual environment
└── src/
    ├── multi_symbol_batch.py   # Multi-Symbol Scanner (Main)
    ├── tws_pipeline.py         # Single-Symbol Pipeline
    └── close_position.py       # Position Closer
```

## Voraussetzungen

1. **TWS läuft auf Remote-Server** (192.168.178.75) mit API aktiviert:
   - File → Global Configuration → API → Settings
   - ☑ Enable ActiveX and Socket Clients
   - Port: 7496
   - ☑ Read-Only API (für Paper Trading)

2. **SSH Tunnel** von lokal zu Remote:
   ```bash
   sshpass -p trapapa ssh -L 7496:localhost:7496 -N -f -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null trapapa@192.168.178.75
   ```

## Installation

```bash
cd /home/hermes/tws_option_pipline_two-1
python3 -m venv venv
source venv/bin/activate
pip install ib_insync
```

## Ausführung

```bash
# 1. SSH Tunnel aufbauen (einmalig pro Session)
sshpass -p trapapa ssh -L 7496:localhost:7496 -N -f -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null trapapa@192.168.178.75

# 2. venv aktivieren
source venv/bin/activate

# 3. Multi-Symbol Batch (Main Script)
python3 src/multi_symbol_batch.py [OPTIONEN] SYMBOL [MONTH_INDICES] [EXCHANGE] [CURRENCY]
```

### Multi-Symbol Batch Parameter

| Flag | Kurz | Beschreibung | Standard |
|------|------|--------------|----------|
| `--manual` | `-m` | Manueller Modus: Option selbst wählen | aus |
| `--order-type` | `--ot` | Order Type: `LMT` (Limit) oder `REL` (Pegged-to-Midpoint) | `LMT` |
| `--chains` | `--num-chains` | Anzahl Expirations zu scannen | alle |
| `--delta-min` | `--dmin` | Min Delta (z.B. -0.30) | -0.50 |
| `--delta-max` | `--dmax` | Max Delta (z.B. -0.10) | -0.10 |
| `--bid-min` | `--bmin` | Min Bid Preis (z.B. 0.80) | 0.80 |

### Beispiele

```bash
# Standard (LMT, Delta -0.50 bis -0.10, Bid ≥ 0.80, DTE ≤ 28, erste 2 Expirations)
python3 src/multi_symbol_batch.py ZIM 0 1 SMART USD

# REL Order Type (Pegged-to-Midpoint, Offset=0)
python3 src/multi_symbol_batch.py ZIM --order-type REL 0 1 SMART USD
python3 src/multi_symbol_batch.py ZIM --ot REL 0 1 SMART USD

# Manual Mode + REL + 5 Chains + Delta Range
python3 src/multi_symbol_batch.py ZIM -m --ot REL --chains 5 --delta-min -0.30 --delta-max -0.10 0 1 SMART USD

# Alle Parameter explizit
python3 src/multi_symbol_batch.py ZIM \
  --manual \
  --order-type REL \
  --num-chains 3 \
  --delta-min -0.30 \
  --delta-max -0.10 \
  0 1 SMART USD

# IBM Beispiel
python3 src/multi_symbol_batch.py IBM -m --ot REL --chains 3 --dmin -0.30 --dmax -0.10 0 1 SMART USD

# CROX mit allen Filtern (Delta -0.25 bis -0.15, Bid ≥ 0.80, DTE ≤ 28)
python3 src/multi_symbol_batch.py CROX --chains 3 -m --ot REL --dmin -0.25 --dmax -0.15 --bid-min 0.80 0 1 SMART USD

# ZIM mit Bid ≥ 0.80 (Default), DTE ≤ 28
python3 src/multi_symbol_batch.py ZIM --chains 3 -m --ot REL 0 1 SMART USD

# Custom Bid Minimum
python3 src/multi_symbol_batch.py ZIM --chains 3 -m --bid-min 0.20 0 1 SMART USD
```

### Single-Symbol Pipeline

```bash
python3 src/tws_pipeline.py CROX 2 SMART USD
python3 src/tws_pipeline.py AAPL 2 SMART USD
```

### Position Closer

```bash
python3 src/close_position.py          # Interaktiv
python3 src/close_position.py -h       # Hilfe
```

**Aktionen im Menü:**
- `1,3` oder `1 3` - Mehrere Positionen schließen
- `c1` - Order #1 abbrechen
- `r` - Refresh
- `q` - Quit

## Output

- **CSV**: `output/multi_symbol_top5_<TIMESTAMP>.csv` (Top 5 pro Symbol)
- **HTML**: `output/multi_symbol_top5_<TIMESTAMP>.html` (parallel zur CSV)

**Spalten:** conid, symbol, right, expiration, strike, multiplier, bid, ask, last, close, volume, delta, gamma, theta, vega, impliedVol, bidSize, askSize, high, low, openPrice, openInterest, put_profit%, DTE

**Filter:** Nur PUTs mit Delta -0.50 bis -0.10, Bid ≥ 0.80, DTE ≤ 28 (alle anpassbar)

## Bekannte Limitationen

- **OpenInterest** = `nan` (Delayed Data bei Paper Trading)
- Client IDs können erschöpft sein → TWS neu starten
- Für europäische Aktien (ALV, ASML) braucht man Market Data Subscription
- REL Orders benötigen `auxPrice=0` für Midpoint (automatisch gesetzt)

## IBKR Order Types für Optionen

| Type | Beschreibung |
|------|--------------|
| `LMT` | Limit Order (Preis festlegen) |
| `REL` | Pegged-to-Midpoint (Offset=0 = Midpoint) |
| `MKT` | Market Order |

* `MID` wird von IBKR für Optionen **nicht** unterstützt.

bevor take profit