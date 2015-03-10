python hwcmp.py data/wilhw2.txt data/yathw2.txt force.txt hwcmp.txt
python hwnear_init.py hwcmp.txt hwcmp_near.txt
python analyze_near.py hwcmp_near.txt hwcmp_near_analyze.txt data/wil_mw.txt
python hwcmp_adj.py hwcmp.txt hwcmp_near_analyze.txt hwcmp_adj.txt
