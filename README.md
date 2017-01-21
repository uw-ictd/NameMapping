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

Our approach relies on a mixture of available string matching algorithms. We use these algorithms and define a heuritstic to combine them and select best matches. We enrich these heurstics by defining patterns and features that allow a first classification and simplification of names to improve matching performace. These patterns may be data source specific.

### Traditional string matching algorithms

### Algorithms mixture

### Name patterns recognition
