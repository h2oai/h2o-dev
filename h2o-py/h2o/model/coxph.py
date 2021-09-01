# -*- encoding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .model_base import ModelBase


class H2OCoxPHModel(ModelBase):

    def formula(self):
        """Survival formula."""
        return self._model_json["output"]["formula"] 
        
    def concordance(self):
        """Concordance"""
        return self._model_json["output"]["concordance"]

    def coefficients_table(self):
        """Coefficients table."""
        return self._model_json["output"]["coefficients_table"]

    def show_summary(self):
        print(self._summary())


    def _summary(self):
        """Prints summary information about this model."""
        output = self._model_json["output"]
        return """Call:
{formula}
{coefs}
Likelihood ratio test={lrt:f}
Concordance={concordance:f}
n={n:d}, number of events={tot_events:d}
""".format(formula=self.formula(),
           coefs=self.coefficients_table(),
           lrt=output["loglik_test"],
           concordance=self.concordance(),
           n=output['n'],
           tot_events=output["total_event"])


class H2OCoxPHMojoModel(ModelBase):
    pass
