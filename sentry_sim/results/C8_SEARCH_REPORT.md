# C8: large nested random search on EDB (auto-generated; numbers come from results/c8_*.csv)

Protocol frozen before any result (`configs/c8_frozen.json`, `c8_cnn_frozen.json`). Configurations completed: {'cnn': 240, 'tabular': 1360}. Each outer fold picks its own best configuration by inner-validation AUROC only; test scores of all configurations are logged only to measure the winner's curse. EDB subjects were already used as test folds earlier in this project, so any winner here is a **hypothesis, not a result**; the raw LTSTDB ECG (the only fresh ST-labelled source) was not downloaded (about 114 KB/s measured, about 17 hours). Label: **Replayed**.

## Pass rule (written in advance)
Search adds value only if the lower end of the 95 % subject-bootstrap range of (nested pick, all families, sensitivity at 1 % FPR) minus R1 is above 0.
Outcome: **SEARCH ADDS VALUE (lower end above 0)**; point 0.152, range 0.065 to 0.318.

## Nested picks, mean over the 5 outer folds (validation-selected)
```
                   val_auroc  test_auroc  test_sens1
criterion family                                    
val_auroc all          0.927       0.767       0.272
          cnn          0.898       0.793       0.184
          tabular      0.927       0.767       0.272
val_sens1 all          0.899       0.762       0.187
          cnn          0.876       0.749       0.154
          tabular      0.890       0.783       0.188
```
## Bootstrap (sensitivity at 1 % false-positive rate, pooled over 5 folds)
```
                                           quantity  point    lo    hi
       nested pick: tabular (val AUROC): sens@1%FPR  0.272 0.203 0.464
           nested pick: cnn (val AUROC): sens@1%FPR  0.182 0.124 0.415
           nested pick: all (val AUROC): sens@1%FPR  0.272 0.203 0.464
                                     R1: sens@1%FPR  0.120 0.081 0.204
                                     R0: sens@1%FPR  0.124 0.062 0.284
                                     M1: sens@1%FPR  0.232 0.162 0.414
                                  M2_s0: sens@1%FPR  0.109 0.074 0.249
                                  M2_s1: sens@1%FPR  0.091 0.065 0.235
                                  M2_s2: sens@1%FPR  0.070 0.048 0.218
                                  A3_s0: sens@1%FPR  0.122 0.084 0.201
                                  A3_s1: sens@1%FPR  0.108 0.077 0.194
                                  A3_s2: sens@1%FPR  0.066 0.050 0.180
              nested pick: tabular (val AUROC) - R1  0.152 0.065 0.318
nested pick: tabular (val AUROC) - A3 (3-seed mean)  0.173 0.095 0.319
                  nested pick: cnn (val AUROC) - R1  0.063 0.011 0.239
    nested pick: cnn (val AUROC) - A3 (3-seed mean)  0.084 0.035 0.249
                  nested pick: all (val AUROC) - R1  0.152 0.065 0.318
    nested pick: all (val AUROC) - A3 (3-seed mean)  0.173 0.095 0.319
```
## AUROC by fold (unseen patients)
```
                          method  fold0  fold1  fold2  fold3  fold4  mean
nested pick: tabular (val AUROC)  0.518  0.716  0.875  0.931  0.792 0.767
    nested pick: cnn (val AUROC)  0.502  0.887  0.833  0.907  0.840 0.794
    nested pick: all (val AUROC)  0.518  0.716  0.875  0.931  0.792 0.767
                              R1  0.617  0.765  0.724  0.737  0.785 0.726
                              R0  0.415  0.767  0.639  0.734  0.671 0.645
                              M1  0.449  0.672  0.741  0.780  0.759 0.680
                           M2_s0  0.389  0.702  0.564  0.800  0.747 0.640
                           M2_s1  0.468  0.651  0.646  0.789  0.737 0.658
                           M2_s2  0.374  0.413  0.638  0.814  0.745 0.597
                           A3_s0  0.701  0.840  0.794  0.825  0.867 0.805
                           A3_s1  0.695  0.850  0.819  0.822  0.862 0.810
                           A3_s2  0.641  0.858  0.800  0.825  0.837 0.792
```
## Winner's curse: how well validation rank predicts test rank
Spearman correlation between validation and test metric across configurations (mean over folds):
```
family   metric
cnn      auroc     0.467
         sens1     0.067
tabular  auroc     0.628
         sens1     0.294
```
Mean over folds: best validation value vs the test value of that same configuration vs the average configuration vs the best test value of any configuration:
```
                best_val  test_of_best_val  mean_all_test  best_test_any
family  metric                                                          
cnn     auroc      0.898             0.793          0.783          0.889
        sens1      0.498             0.154          0.132          0.414
tabular auroc      0.927             0.767          0.708          0.920
        sens1      0.558             0.188          0.187          0.558
```
A big gap between "best_val" and "test_of_best_val" is the optimism of picking the best of thousands; "best_test_any" is what you would wrongly report if you picked on test.

## What this does NOT show
Nothing about early warning, lead time or ischemia: labels are ST episodes marked by an amplitude rule (circular), all 79 subjects were already used as test folds before, and no fresh data exists. The drift-absorption risk of a running baseline in a truly ischemic person is untested.

## Allowed poster wording
Only if the verdict line says adds value: "A search over about 1600 model variants, selected on validation patients only, reached sensitivity X at a 1 % false-alarm rate on unseen patients (Replayed, public EDB data; feasibility, not detection)." Otherwise: "A search over about 1600 model variants did not beat a simple personal-baseline ST rule on unseen patients (Replayed)."
