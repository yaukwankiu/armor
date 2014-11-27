#localFeaturesSensitivityTest4.py

sigmoidWidths = {
                 'eigenvectors'             :   0.1,
                 'numberOfComponents'       :   0.05,
                 'skewness'                 :   0.3,
                 'angle'                    :   0.2,
                 'highIntensityRegionVolume':   1.,     # didn't test it this time
                 'volume'                   :  0.1, # taking log first
                 'centroid'                 : 0.1,
                 'eigenvalues'              : 10.,
                 'kurtosis'                 : 0.5,
                 ('HuMoments',0)            :  20,
                 ('HuMoments',1)            : 2000, # can't get accurate figures for these
                 ('HuMoments',2)            :0.02,
                 ('HuMoments',3)            : 0.01,
                 ('HuMoments',4)            : 0.01,
                 ('HuMoments',5)            : 0.05,
                 ('HuMoments',6)            : 0.05,
                 'rectangle'                : 4,
                }


