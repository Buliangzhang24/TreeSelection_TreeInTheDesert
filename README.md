# TreeSelection_TreeInTheDesert
## Pre-Selected Tree Species

| **Early Stage**  | Tamarix spp.                              |
| ---------------- | ----------------------------------------- |
|                  | Vachellia tortilis                        |
|                  | Halocnemum strobilaceum                   |
|                  | Plocama pendula                           |
|                  | Atriplex nummularia                       |
|                  | Salvadora persica                         |
|                  | Prosopis cineraria                        |
| **Forest Stage** | Phoenix dactylifera / Phoenix canariensis |
|                  | Citrus aurantium                          |
|                  | Jatropha curcas                           |
|                  | Olea cerasiformis                         |
|                  | Acacia ampliceps                          |
|                  | Acacia nilotica                           |
|                  | Conocarpus lancifolius                    |
## 1.  Key Factors and Data Sources


| **Factor**                                             | **Data Source & Processing Method**                   | **Situation**              |
| ------------------------------------------------------ | ----------------------------------------------------- | -------------------------- |
| **Salinity (NDSI)**                                    | Sentinel-2 SWIR bands → NDSI = (B11-B8A)/(B11+B8A) \| | ![[/images/NDSI_Plot.png]]         |
| **Drought (AI)**                                       | CHIRPS rainfall + MODIS PET → AI = P/PET              | ![[/images/Moisture_Analysis.png]] |
| **Wind erosion**                                       | ERA5 wind speed → % of days with strong wind (>5 m/s) | No                         |
| **Soil texture**                                       | SoilGrids 250m (sand/clay ratio)                      | Low Resolution             |
| **Economic/ecological needs/invasion risk assessment** | Literature (e.g., FAO crop database)                  | In table                   |

## 2.  Weight Assignment (needs further validation)

Method: Prioritize based on Tarfaya’s conditions
Be Like salinity 40%, drought 30%, wind 20%, economy 10%

## 3.  Formulas & Algorithms

**Steps**

1.     Standardize Environmental Factors: Standardize factors to 0-1 scale.

2.     Assign weights

Salinity weight = (plot NDSI / max regional NDSI) × 40%

Drought weight = (plot AI / min regional AI) × 30%

Wind erosion weight = (plot wind speed / max regional wind speed) × 20%

Economic/ecological weight = fixed 10% (manually set priority).

3.     Score species tolerance (1-5) from literature: Assign species tolerance scores (1-5, 5=best) for salinity, drought, and wind resistance based on literature.


| Species                 | Salt_Tolerance | Drought_Tolerance | Wind_Resistance |
| ----------------------- | -------------- | ----------------- | --------------- |
| Tamarix spp.            | 5              | 5                 | 4               |
| Vachellia tortilis      | 4              | 5                 | 4               |
| Halocnemum strobilaceum | 5              | 5                 | 3               |
| Plocama pendula         | 4              | 4                 | 3               |
| Atriplex nummularia     | 5              | 5                 | 3               |
| Salvadora persica       | 4              | 5                 | 4               |
| Prosopis cineraria      | 4              | 5                 | 4               |
| Phoenix dactylifera     | 4              | 4                 | 4               |
| Citrus aurantium        | 2              | 3                 | 3               |
| Jatropha curcas         | 3              | 4                 | 3               |
| Olea cerasiformis       | 3              | 4                 | 3               |
| Acacia ampliceps        | 5              | 4                 | 3               |
| Acacia nilotica         | 4              | 4                 | 3               |
| Conocarpus lancifolius  | 4              | 4                 | 5               |

4.     Total score = (Salt tolerance × dynamic salinity weight) + (Drought tolerance × dynamic drought weight) + (Wind resistance × dynamic wind weight) + (Economic value × fixed weight)
![[/images/Scores.png]]
