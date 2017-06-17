from sklearn.linear_model import LinearRegression, Lasso


class ModelRunner:

    def __init__(self, model_architecture, logger):
        """
        Initialize the runner given the model_architecture
        :param model_architecture: JSON object which defines the model architecture.
        """
        self.logger = logger
        self.model_architecture = model_architecture
        self.model = LinearRegression() if self.model_architecture.get('penalty') == 'l1' else Lasso()
        self.logger.info('{} is initialized!'.format(self))

    def __str__(self):
        return 'ModelRunner model: {}'.format(self.model)