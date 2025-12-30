
class ProductionFeatureClass():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__production_feature_class_path = ""
        self.__production_feature_class_name = "SRC_WN_W_Hydrant"

    @property
    def production_feature_class_path(self):
        return self.__production_feature_class_path
    
    @production_feature_class_path.setter
    def production_feature_class_path(self, new_production_feature_class):
        self.__production_feature_class_path = new_production_feature_class
    
    @property
    def production_feature_class_name(self):
        return self.__production_feature_class_name


    