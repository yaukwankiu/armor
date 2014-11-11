"""   
goal:   to test the change in the features under perturbation
1.  Test subject:  a random sum of gaussians
2.  Perturbations:  stretching, addition of noise, etc

2014-11-11
PLAN:   
        1. finish/fix/rewrite armor/tests/localFeaturesDistributionTest.py
            make sure we have information of the full angle, not just the cosine of the angle
        2. plot/analyse/compare the distributions between physically related and physically unrelated datasets
        3. add the normalised third moment in the two canonical directions (skewness) as feature

"""
#   1.  local features +1:  normalised third moment / normalised fourth moment
#   1a. fix the angle feature with the third moment
#   2.  plot the physically related and physically unrelated comparisons
#   3.  

