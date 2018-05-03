# NameMapping
Matching transliterated names for data merging

## Background

In the developing world, Usage of multiple geolocated data sources can be complicated because of weak standardization of a lot of locality names. The fact that these names are often transliterated from vernacular languages that may have no written forms or written forms using non-latin alphabets with no fixed transliteration rule can be a cause for this weak standardization. Complicated local political histories with multiple layers of topological naming can be another source.

Meanwhile, in situations with often low data density, being able to link data sources and to co analyze data sets is essential to generating locally relevant as well as nationnally representative statistics, or to plan actions and interventions based on the best evidence generated along the years. Defining a tool that would allow users to easily match location names between data sources is thus of great interest for a large variety of actors.

## Goal

Provide a generic software package with validated methods an heurtistics for matching locality names written differently between different data sources.

The success of our approach is defined by the largest amount of matches allowed with a zero false positive matches.

## Data

The initial project is run on multiple data sets from Niger. Two lists of localities from the national censues from 2001 and 2012 are obtained throuhgh the RENALOC and RENACOM sets, available on the Institut National de la Statistique (INS) website. A third list of localities in Niger is obtained from the voters registry available on the Comission Electorale Nationale Indépendante (CENI) website.

A validation set is produced by both manually matching locality names and by validating manually matches obtained from earlier versions of our method.

## Methods

Our approach relies on a mixture of available string matching algorithms. We use these algorithms and define heuritstics to combine them and select best matches. We enrich these heurstics by defining patterns and features that allow a first simplification of names to improve matching performace. These patterns may be data source specific.

### Pre Processing
When given two datasets, our first step will be to preprocess the data to spot locally-specific patterns to take care of. These can involve :
1. Common prefixes and suffixes
2. Different transliteration patterns (eg _w_ vs _ou_ for the same sound)

These patterns can be spotted by the application presented for validation to the user, or the user should be able to specify them.

### Cleaning
In a second step, we define string cleaning heuristics, to remove irregularities or differences in conventions that may affect the ability to match the different data sources. These heuristics involve (among other):
1. Unifying numerals in diverse forms (i. ii. iii. , I II III ...)
2. Removing brackets
3. Splitting and recombining N-Grams of the different strings we want to match

### Unsupervised Algorithm
We also define different metrics of proximity between the data sets we want to match. Currently used metrics are :
[Jaro-Winkler proximity](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) and [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance), [Double Metaphone transliteration](https://en.wikipedia.org/wiki/Metaphone).

For each commune, all possible name pairs between the tow sources are compared, and all possible metrics are measured, for raw or cleaned data. A first match is then made based on pre-specified thresholds.

### Unsupervised iterative trimming
In a latter stage, we will iteratively go through the measured pairs, and we will test different heuristics to check systematic variations that can be filtered before matching. These heuristics can include combinations of simple operations such as :

1. N-Gram splitting and recombining
2. Strings cleaning as describe above
3. Prefix / suffix trimming or translitation variation

The iterative trimming will be made through a process of elimination that will validate easy matches and will later on narrow down on remaining names to converge towards the most complete matching possible.

### Supervised algorithms
Finally, we will devise a method for user validation of the matched pairs, which will lead to fitting supervised learning algorithms for remaining data.

The cost-benefit of implementing such user interaction and computation will be compared to simple unsupervised approaches.
