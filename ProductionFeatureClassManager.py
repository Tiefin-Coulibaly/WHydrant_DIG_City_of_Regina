import Constants
import arcpy
from arcpy import env
from ProductionFeatureClass import ProductionFeatureClass
from DomainManager import DomainManager

env.workspace = Constants.PRODUCTION_SDE_CONNECTION_FILE
env.overwriteOutput = True


class ProductionFeatureClassManager(ProductionFeatureClass, DomainManager):
    def __init__(self, *args, **kwargs):
        super().__init__(
            Constants.DOMAINS_TO_CREATE_IN_GDB,
            Constants.PRODUCTION_SDE_CONNECTION_FILE,
            *args,
            **kwargs,
        )

    def add_fields_from_schema(self):
        """
        Adds fields defined in the FEATURE_SCHEMA to the specified feature class.

        :param feature_class: The path to the feature class where fields will be added.
        """
        try:
            arcpy.AddMessage("Adding fields from schema...")
            for field_name, properties in Constants.FEATURE_SCHEMA.items():
                arcpy.management.AddField(
                    in_table=self.production_feature_class_path,
                    field_name=field_name,
                    field_type=properties.get("type"),
                    field_alias=properties.get("alias", ""),
                )
                arcpy.AddMessage(f"Added field: {field_name}")
            arcpy.AddMessage("All fields added successfully.")
        except Exception as e:
            arcpy.AddError(f"Failed to add fields from schema: {e}")

    def assign_default_values(self):
        """
        Assigns default values to fields in the feature class based on the schema.

        :param feature_class: The path to the feature class where default values will be assigned.
        """
        try:
            arcpy.AddMessage("Assigning default values to fields...")
            for field_name, properties in Constants.FEATURE_SCHEMA.items():
                default_value = properties.get("default")
                if default_value is not None:
                    arcpy.management.AssignDefaultToField(
                        in_table=self.production_feature_class_path,
                        field_name=field_name,
                        default_value=default_value,
                    )
                    arcpy.AddMessage(f"Assigned default value for field: {field_name}")
            arcpy.AddMessage("Default values assigned successfully.")
        except Exception as e:
            arcpy.AddError(f"Failed to assign default values: {e}")

    def edit_field_alias(self, field_name, new_alias):
        """
        Edits the alias of a specified field in the feature class.

        :param field_name: The name of the field whose alias is to be changed.
        :param new_alias: The new alias to assign to the field.
        """
        try:
            arcpy.AddMessage(f"Changing alias for field {field_name} to {new_alias}...")
            arcpy.management.AlterField(
                in_table=self.production_feature_class_path,
                field=field_name,
                new_field_alias=new_alias,
            )
            arcpy.AddMessage(f"Alias for field {field_name} changed successfully.")
        except Exception as e:
            arcpy.AddError(f"Failed to change alias for field {field_name}: {e}")

    def add_globalid_field(self):
        """
        Adds a GlobalID field to the feature class if it does not already exist.
        """
        try:
            arcpy.AddMessage("Adding GlobalID field...")
            arcpy.management.AddGlobalIDs(self.production_feature_class_path)
            arcpy.AddMessage("GlobalID field added successfully.")
        except Exception as e:
            arcpy.AddError(f"Failed to add GlobalID field: {e}")

    def create_production_feature_class(self):
        """
        Creates a new feature class in the geodatabase based on the defined schema.
        """
        try:
            arcpy.AddMessage("Creating new feature class...")
            self.production_feature_class_path = arcpy.management.CreateFeatureclass(
                out_path=rf"{Constants.PRODUCTION_SDE_CONNECTION_FILE}\{Constants.FEATURE_DATASET_NAME}",
                out_name=self.production_feature_class_name,
                geometry_type="POINT",
                spatial_reference=arcpy.SpatialReference(26913),  # UTM Zone 13N
            ).getOutput(0)
            self.add_fields_from_schema()
            self.assign_default_values()
            self.add_globalid_field()
            self.edit_field_alias("OBJECTID", "Object ID")

            arcpy.AddMessage(
                f"Feature class {self.production_feature_class_name} created successfully at {self.production_feature_class_path}."
            )
        except Exception as e:
            arcpy.AddError(f"Failed to create feature class: {e}")

    def production_run_all(self):
        self.create_production_feature_class()
        self.create_domains()
        self.assign_domains_to_fields(self.production_feature_class_path)


if __name__ == "__main__":
    manager = ProductionFeatureClassManager()
    manager.production_run_all()
