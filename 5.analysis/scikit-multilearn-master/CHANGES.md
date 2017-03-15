scikit-multilearn Changelog
===========================

0.0.5 (released 2017-02-25)
---------------------------

- a general matrix-based label space clusterer has been added which can cluster the output space using any scikit-learn compatible clusterer (incl. k-means)
- support for more single-class and multi-class classifiers you can now use problem transformation approaches with your favourite neural networks/deep learning libraries: theano, tensorflow, keras, scikit-neuralnetworks
- support for label powerset based stratified kfold added
- graph-tool clusterer supports weighted graphs again and includes stochastic blockmodel calibration
- bugs were fixed in: classifier chains and hierarchical neuro fuzzy clasifiers

0.0.4 (released 2017-02-04)
---------------------------

-  *kNN classifiers support sparse matrices properly
- support for the new model_selection API from scikit-learn
- extended graph-based label space clusteres to allow taking probability of a label occuring alone into consideration
- compatible with newest graphtool
- support the case when meka decides that an observation doesn't have any labels assigned
- HARAM classifier provided by Fernando Benitez from University of Konstanz
- predict_proba added to problem transformation classifiers
- ported to python 3 

0.0.3 (released 2016-06-03)
---------------------------

- support for new multi-label classification methods:
    - classsifier chains (CC)
    - multi-label kNN methods: BRkNN and MLkNN
    - all classifiers use sparse matrices internally
    - a general network for clustering label space with a flat classifier
    - the classifiers work with scikit pipelines / CVs

- interface to meka 1.9, meka can work as a scikit-ml classifier
- loading arff files to sparse matrices by default

0.0.2 (removed due to bug in PyPi)
---------------------------

- support for new multi-label classification methods:
    - classsifier chains (CC)
    - multi-label kNN methods: BRkNN and MLkNN
    - all classifiers use sparse matrices internally
    - a general network for clustering label space with a flat classifier
    - the classifiers work with scikit pipelines / CVs



0.0.1 (released 2014-12-01)
---------------------------

- initial release
- support for initial set of multi-label classification methods:
    - binary relevance, label powerset
    - RAkEL both distinct and overlapping
    - label cooccurence based distinct partitioning classifiers
- interface to meka 1.7
- ARFF to numpy.array convertion classes and data set manipulation

