![bin](https://raw.githubusercontent.com/biocore/oecophylla/master/doc/images/bin.jpeg "bin")

Binning attempts to bin together contigs into estimated genomes.  

The information binning programs use to make these calls is typically the abundance profile of contigs in an assembly across different individual samples. 

Practically speaking, that means that contigs assembled from one sample (sample A) must be compared to reads from many samples (samples A, B, C, D, and E) to generate an abundance profile. Assuming you want to bin contigs from assemblies of each of *n* samples using information from each other sample, that means you must do *n* x *n* comparisons. 
