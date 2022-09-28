# Agrivoltaics Supply Side Management

Optimizes Supply Side Management with Agrivoltaics (Solar sharing between 
Photovoltaics and Agriculture) by Artificial Intelligence. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 
agrivoltaics-supply-side-management.

#### Case 1
When using by cloning this GIT repository:
```bash
pip install -e [ABSOLUTE PATH TO THIS PROJECT]
```

#### Case 2
When using a package available in PyPI:
```bash
pip install agrivoltaics-supply-side-management
```

#### Solvers
We use Python library for mathematical optimization, called Pyomo. 
As in any mathematical optimization tool, it requires a solver. 

For Linear Programming, glpk is used as a solver by default following Pyomo 
tutorial. 

In Macintosh, install it through Homebrew:
```bash
brew install glpk
```

For other platforms, see https://www.gnu.org/software/glpk/

## Usage

[To be added]




## References

[1] P. E. Campana, B. Stridh, S. Amaducci, and M. Colauzzi,
    “Optimisation of vertically mounted agrivoltaic systems,”
    Journal of Cleaner Production, vol. 325, p. 129091, Nov. 2021,
    doi: 10.1016/j.jclepro.2021.129091.
[2] C. B. Honsberg, R. Sampson, R. Kostuk, G. Barron-Gafford, 
    S. Bowden, and S. Goodnick, “Agrivoltaic Modules Co-Designed 
    for Electrical and Crop Productivity,” 
    in 2021 IEEE 48th Photovoltaic Specialists Conference (PVSC), 
    Jun. 2021, pp. 2163–2166. doi: 10.1109/PVSC43889.2021.9519011.
[3] B. Willockx, B. Uytterhaegen, B. Ronsijn, B. Herteleer, and J. Cappelle, 
    “A standardized classification and performance indicators of agrivoltaic 
    systems.,” Oct. 2020. doi: 10.4229/EUPVSEC20202020-6CV.2.47.
[4] H-W, Heldt, ”Plant Biochemistry,” Elsevier Academic Press, 
    Burlington, MA, USA, 2005.
[5] R. W. Langhans and T. W. Tibbits, “Plant Growth Chamber Handbook 
    - Chapter 1 Radiation,” in Plant Growth Chamber Handbook, 
    Iowa State University, 1997.
[6] O. A. Martin, R. Kumar, and J. Lao, "Bayesian Modeling and Computation 
    in Python," Boca Ratón, 2021. 
    [Online]. Available: https://bayesiancomputationbook.com
[7] R. Retkute, S. E. Smith-Unna, R. W. Smith, A. J. Burgess, O. E. Jensen, 
    G. N. Johnson, S. P. Preston, E. H. Murchie, ”Exploiting heterogeneous 
    environments: does photosynthetic acclimation optimize carbon gain in 
    fluctuating light?,” Journal of Experimental Botany, May 2015, vol. 66, 
    no. 9, pp. 2437–2447, doi: 10.1093/jxb/erv055.
