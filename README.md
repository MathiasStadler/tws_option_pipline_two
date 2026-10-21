# Test


1962  ssh -N -L 7496:127.0.0.1:7496 trapapa@192.168.178.75
 1963  source venv/bin/activate
 1964  python3 tws_pipeline.py ALV 0 XETRA EUR
 1965  cd src/
 1966  python3 tws_pipeline.py ALV 0 XETRA EUR
 1967  python3 src/tws_pipeline.py SAP 0 SMART EUR
 1968  python3 tws_pipeline.py SAP 0 SMART EUR
 1969  cat /home/hermes/tws_option_pipeline/src/tws_option_contracts_SAP_20261020_103344.csv
 1970  clean
 1971  claer
 1972  clear
 1973  python3 src/multi_symbol_batch.py ZIM --chains 3 -m --ot REL 0 1 SMART USD
 1974  cd ..
 1975  python3 src/multi_symbol_batch.py ZIM --chains 3 -m --ot REL 0 1 SMART USD
 1976  python3 src/multi_symbol_batch.py CSX --chains 3 -m --ot REL 0 1 SMART USD
 1977  python3 src/multi_symbol_batch.py MDLZ --chains 3 -m --ot REL 0 1 SMART USD
 1978  python3 src/multi_symbol_batch.py ZIM --chains 3 --dmin -0.50 --dmax -0.01 --bid-min 0.01 --bracket -m 0 1 SMART USD
 1979  python3 src/multi_symbol_batch.py TREX --chains 3 --dmin -0.50 --dmax -0.01 --bid-min 0.01 --bracket -m 0 1 SMART USD
 1980  python3 src/multi_symbol_batch.py ZIM --chains 3 --dmin -0.50 --dmax -0.01 --bid-min 0.01 --bracket -m 0 1 SMART USD
 1981  python3 src/multi_symbol_batch.py ZIM --chains 3 --dmin -0.30 --dmax -0.10 --bid-min 0.01 --bracket -m 0 1 SMART USD
 1982  python3 src/multi_symbol_batch.py ZIM --chains 5 --dmin -0.30 --dmax -0.10 --bid-min 1.00 --bracket -m 0 1 SMART USD
 1983  python3 src/multi_symbol_batch.py crox --chains 5 --dmin -0.30 --dmax -0.10 --bid-min 1.00 --bracket -m 0 1 SMART USD
 1984  python3 src/multi_symbol_batch.py crox --chains 5 --dmin -0.10 --dmax -0.30 --bid-min 1.00 --bracket -m 0 1 SMART USD
 1985  cat /home/hermes/tws_option_pipline_two-1/output/multi_symbol_top5_20261020_190853.csv
 1986  python3 src/multi_symbol_batch.py crox --chains 5 --dmin -0.10 --dmax -0.50 --bid-min 1.00 --bracket -m 0 1 SMART USD
 1987  python3 src/multi_symbol_batch.py MDLZ --chains 3 -m --ot REL 0 1 SMART USD
 1988  python3 src/multi_symbol_batch.py ZIM --chains 3 --dmin -0.50 --dmax -0.01 --bid-min 0.01 --bracket -m 0 1 SMART USD
 1989  python3 src/multi_symbol_batch.py ZIM --chains 3 --dmin -0.50 --dmax -0.01 --bid-min 0.01  -m 0 1 SMART USD
 1990  python3 src/multi_symbol_batch.py MDLZ --chains 3 --dmin -0.50 --dmax -0.01 --bid-min 0.01  -m 0 1 --ot MKT SMART USD