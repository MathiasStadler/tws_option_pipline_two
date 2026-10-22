# Test 

- ssh -N -L 7496:127.0.0.1:7496 trapapa@192.168.178.75
- watch "ps aux | grep ssh | grep -Eo '^[^ ]+' | sort | uniq"

- cd /home/hermes/tws_option_pipline_two-1 && source venv/bin/activate && python3 ../tws_option_pipline_two/src/multi_symbol_batch.py CROX AAPL TREX PEP DELL --chains 3 --spread --spread-width 5 --max-margin 1000 --min-credit 0.80 --dmin -0.50 --dmax -0.01 --bid-min 0.01 -m 0 1 SMART USD
