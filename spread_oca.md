# Bull Put Spread mit OCA Stop-Loss / Take-Profit

> **Script:** `/home/hermes/tws_option_pipline_two/src/multi_symbol_batch.py`  
> **Neue Funktionen:** `place_spread_order()`, `place_spread_oca_orders()`

---

## Übersicht

Das Script unterstützt jetzt **Bull Put Spreads (Credit Spreads)** mit automatischen **OCA-Orders (One-Cancels-All)** für Stop-Loss und Take-Profit auf dem **gesamten Spread** (Combo/BAG Contract).

### Was passiert:

1. **Entry:** Bull Put Spread eröffnen (Short Higher Strike PUT + Long Lower Strike PUT) → OCA Group für beide Legs
2. **TP/SL anhängen:** Zwei Orders auf dem **Spread-Combo**:
   - **Take Profit:** BUY Spread @ Limit (Debit = Credit × 30% → 70% Gewinn)
   - **Stop Loss:** BUY Spread @ Stop-Limit (Debit = Credit × 200% → 100% Verlust)
   - **OCA Type 1:** Ein Fill killt den anderen Order

---

## Kommandozeilen-Parameter

```bash
python3 multi_symbol_batch.py [SYMBOLS...] [OPTIONEN]
```

| Parameter | Short | Default | Beschreibung |
|-----------|-------|---------|--------------|
| `--spread` / `--bull-put-spread` | | `False` | **Bull Put Spread Mode aktivieren** |
| `--spread-width` / `--sw` | | `5` | Strike-Abstand (Points) |
| `--max-margin` / `--mm` | | `1000` | Max Margin pro Spread (USD) |
| `--min-credit` / `--mc` | | `0.80` | Minimaler Credit Target (USD) |
| `--order-type` / `--ot` | | `LMT` | `LMT`, `REL`, `MKT` |
| `--bracket` / `-b` | | `False` | Für Single-Options: Bracket Order (TP 70% / SL 200%) |
| `-m` / `--manual` | | `False` | **Interaktiver Modus** (fragt nach OCA für Spreads) |
| `-v` / `--verbose` | | `False` | Debug Logging |

---

## Nutzungsszenarien

### 1. Auto-Mode (unbeaufsichtigt) – **Empfohlen für Montag**

```bash
# Beispiel: AAPL + TSLA, Spread Width 5, Max Margin $1000, Min Credit $0.80
python3 multi_symbol_batch.py AAPL TSLA --spread --spread-width 5 --max-margin 1000 --min-credit 0.80
```

**Ablauf:**
1. Scannt Option Chains, filtert nach Delta (-0.50 bis -0.10), Bid ≥ $0.80, DTE ≤ 45
2. Findet beste Bull Put Spreads pro Symbol (sortiert nach Return on Margin %)
3. Platziert **Entry Spread** (OCA für beide Legs)
4. **Automatisch:**hängt OCA TP/SL an (TP 70%, SL 100%)
5. Schreibt CSV + HTML Report

---

### 2. Manual Mode (interaktiv) – **Zum Testen/Kontrollieren**

```bash
python3 multi_symbol_batch.py AAPL TSLA --spread -m
```

**Ablauf:**
1. Gleicher Scan wie Auto
2. Zeigt nummerierte Liste aller gefundenen Spreads
3. User wählt: `1`, `1,3`, `1 3` oder `q`
4. Nach Spread-Platzierung: **Fragt explizit**  
   `>>> OCA Stop-Loss / Take-Profit für Spread anhängen? (y/n)`
5. Bei `y` → TP/SL OCA wird angelegt

---

### 3. Single Symbol, spezifische Expirations

```bash
# Month indices: 0 = front month, 1 = next, etc.
python3 multi_symbol_batch.py SPY --spread 0 1 --spread-width 5 --max-margin 500
```

---

## TP/SL Logik (Defaults)

| Metrik | Wert | Bedeutung |
|--------|------|-----------|
| **Take Profit** | 30% des Credit | Spread zurückkaufen @ 30% des erhaltenen Credit = **70% Gewinn** |
| **Stop Loss** | 200% des Credit | Spread zurückkaufen @ 200% des Credit = **100% Verlust** (Max Risk) |

**Beispiel:** Credit = $1.50
- TP Limit: $0.45 (Buy Spread @ $0.45 Debit)
- SL Stop: $3.00, Limit: $3.05 (Buy Spread @ $3.00 Debit)

### Anpassung (im Code)

In `place_spread_oca_orders()` aufrufbar mit:
```python
place_spread_oca_orders(ib, short_opt, long_opt, 
                        quantity=1, 
                        net_credit=placed['net_credit'],
                        take_profit_pct=0.30,   # 0.30 = 30% = 70% Profit
                        stop_loss_pct=2.00,     # 2.00 = 200% = 100% Loss
                        verbose=False)
```

---

## Wichtige technische Details

### Combo/BAG Contract für TP/SL
```python
spread_combo = Bag([
    Leg(short_option, 1, 'BUY'),   # Short Leg zurückkaufen
    Leg(long_option, 1, 'SELL')    # Long Leg verkaufen
], symbol=short_option.symbol, exchange=short_option.exchange)
```
- **Action BUY** = Spread schließen (Debit zahlen)
- Funktioniert nur, wenn **beide Legs offene Positionen** sind

### OCA Groups
| Phase | OCA Group Name | Typ | Zweck |
|-------|----------------|-----|-------|
| Entry | `SPREAD_SYMBOL_EXP_<uuid>` | 1 | Short + Long Leg zusammen |
| TP/SL | `SPREAD_OCA_SYMBOL_EXP_<uuid>` | 1 | TP Order + SL Order zusammen |

### Order Types für TP/SL
- **Take Profit:** `LMT` (Limit Order) – garantiert Preis, aber Fill-Risiko
- **Stop Loss:** `STP LMT` (Stop-Limit) – Stop @ SL-Preis, Limit +$0.05 für Fill-Sicherheit

---

## Output / Reports

### CSV (`output/multi_symbol_top5_YYYYMMDD_HHMMSS.csv`)
**Spread-Modus Spalten:**
```
symbol, expiration, short_strike, long_strike, spread_width,
short_bid, short_ask, long_bid, long_ask,
credit, max_loss, margin_req, rom, pop,
short_delta, long_delta, short_volume, long_volume, short_iv, long_iv
```

### HTML Report
Gleichzeitig erzeugt: `multi_symbol_top5_YYYYMMDD_HHMMSS.html`

### Console Summary (Auto-Mode)
```
📈 AAPL @ 225.50 USD (3 expirations) — BULL PUT SPREADS
Short | Long | W  | Exp       | Credit | Margin | ROM% | POP% | Short Δ
------|------|----|-----------|--------|--------|------|------|--------
 220  | 215  |  5 | 241220    | $1.25  | $375   | 33.3%| 68.2%| -0.318
```

---

## Checkliste für Montag

- [ ] TWS/Gateway läuft auf **Port 7496** (Socket API)
- [ ] Paper Trading Account verbunden (Market Data Type 4 = Delayed-Frozen)
- [ ] Genügend **Available Funds** für Margin (Short PUT Margin ≈ 20% Strike × 100)
- [ ] Script ausführbar: `chmod +x multi_symbol_batch.py`
- [ ] Test-Run mit **einem Symbol** im Manual Mode: `python3 multi_symbol_batch.py AAPL --spread -m`
- [ ] Prüfen: Orders erscheinen in TWS → **Activity → Orders** (OCA Group sichtbar)

---

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| `qualifyContracts failed` | Symbol/Exchange prüfen (SYMBOL_DEFAULTS im Script), Internet? |
| `No valid prices` | Paper Delayed Data: nur liquide Strikes nahe ATM haben Bids. `--bid-min` senken? |
| `Credit <= 0` | Spread Width zu groß / IV zu niedrig. Andere Expiration oder Width probieren. |
| OCA Orders nicht sichtbar | TWS → **Global Configuration → Orders → Show OCA Groups** aktivieren |
| `Connection refused` | TWS läuft? Port 7496? API Settings: "Enable ActiveX and Socket Clients" ✓ |

---

## Nächste Schritte (Ideas)

- [ ] Trailing Stop für Spread (statt fixem SL)
- [ ] Time-based Exit (z. B. schließen 7 Tage vor Expiry)
- [ ] Delta-basiertes Rolling (wenn Short Delta > -0.30 → rollen)
- [ ] Portfolio-Level Risk Limits (max gesamt Margin, max Positionen)

---

**Stand:** Implementiert in `multi_symbol_batch.py` (Lines ~898-1100)  
**Testen:** `python3 multi_symbol_batch.py AAPL --spread -m`

python3 multi_spread_oca.py PLTR --spread  --max-margin 1000 --min-credit 0.80