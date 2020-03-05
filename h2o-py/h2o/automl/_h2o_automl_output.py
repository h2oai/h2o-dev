import h2o
from h2o.automl._base import H2OAutoMLBaseMixin
from h2o.base import Keyed


class H2OAutoMLOutput(H2OAutoMLBaseMixin, Keyed):
    """
    AutoML Output object containing the results of AutoML
    """
    
    def __init__(self, state):
        self._project_name = state['project_name']
        self._leader = state['leader']
        self._leaderboard = state['leaderboard']
        self._event_log = el = state['event_log']
        self._training_info = {r[0]: r[1]
                               for r in el[el['name'] != '', ['name', 'value']]
                                   .as_data_frame(use_pandas=False, header=False)
                               }
        
    def __getitem__(self, item):
        if (
            hasattr(self, item) and
            # do not enable user to get anything else than properties through the dictionary interface
            hasattr(self.__class__, item) and 
            isinstance(getattr(self.__class__, item), property)
        ):
            return getattr(self, item)
        raise KeyError(item)

    @property
    def project_name(self):
        """
        Retrieve a string indicating the project_name of the automl instance to retrieve.
        :return: a string containing the project_name
        """
        return self._project_name

    @property
    def leader(self):
        """
        Retrieve the top model from an H2OAutoML object

        :return: an H2O model
        """
        return self._leader

    @property
    def leaderboard(self):
        """
        Retrieve the leaderboard from an H2OAutoML object

        :return: an H2OFrame with model ids in the first column and evaluation metric in the second column sorted
                 by the evaluation metric
        """
        return self._leaderboard

    @property
    def training_info(self):
        """
        Expose the name/value columns of `event_log` as a simple dictionary, for example `start_epoch`, `stop_epoch`, ...
        See :func:`event_log` to obtain a description of those key/value pairs.

        :return: a dictionary with event_log['name'] column as keys and event_log['value'] column as values.
        """
        return self._training_info

    @property
    def event_log(self):
        """
        Retrieve the backend event log from an H2OAutoML object

        :return: an H2OFrame with detailed events occurred during the AutoML training.
        """
        return self._event_log

    #-------------------------------------------------------------------------------------------------------------------
    # Overrides
    #-------------------------------------------------------------------------------------------------------------------
    @property
    def key(self):
        return self.project_name
    
    def detach(self):
        self._project_name = None
        h2o.remove(self.leaderboard)
        h2o.remove(self.event_log)
