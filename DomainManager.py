import Constants
import arcpy


class DomainManager:
    def __init__(self, domains_to_create_in_gdb, production_gdb_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domains_to_create_in_gdb = domains_to_create_in_gdb
        self.production_gdb_path = production_gdb_path
        self.existing_gdb_domains = arcpy.da.ListDomains(self.production_gdb_path)
        self.existing_gdb_domains_names = [
            domain.name
            for domain in self.existing_gdb_domains
            if domain.owner == "GSSRC"
        ]

    def AddCodedValueToDomain(self, domain_name, code, code_description):
        """
        Adds a coded value to an existing domain in the geodatabase.

        :param domain_name: The name of the domain to which the coded value will be added.
        :param code: The code to be added to the domain.
        :param code_description: The description of the code.
        :return: None
        """
        try:
            arcpy.AddMessage(
                f"Adding coded value {code}: {code_description} to domain {domain_name}..."
            )
            arcpy.management.AddCodedValueToDomain(
                in_workspace=self.production_gdb_path,
                domain_name=domain_name,
                code=code,
                code_description=code_description,
            )
            arcpy.AddMessage(
                f"Coded value {code} added to domain {domain_name} successfully."
            )
        except Exception as e:
            arcpy.AddError(
                f"Failed to add coded value {code} to domain {domain_name}: {e}"
            )

    def create_domains(self):
        """
        Creates domains in the geodatabase based on the provided domain definitions.

        :return: None
        """

        try:
            arcpy.AddMessage("Creating domains...")
            with arcpy.EnvManager(
                overwriteOutput=True, workspace=self.production_gdb_path
            ):
                for domain_name, properties in self.domains_to_create_in_gdb.items():
                    if domain_name.casefold() not in (
                        name.casefold() for name in self.existing_gdb_domains_names
                    ):
                        arcpy.AddMessage(f"Creating domain: {domain_name}")

                        arcpy.management.CreateDomain(
                            in_workspace=self.production_gdb_path,
                            domain_name=domain_name,
                            domain_description=domain_name,
                            field_type=properties.get("field_type"),
                            domain_type=properties.get("domain_type"),
                            split_policy=properties.get("split_policy", "DEFAULT"),
                            merge_policy=properties.get("merge_policy", "DEFAULT"),
                        )

                        arcpy.AddMessage(f"Created domain: {domain_name}")

                        # Add coded values if present
                        coded_values = properties.get("coded_values", {})
                        if coded_values:
                            for code, description in coded_values.items():
                                self.AddCodedValueToDomain(
                                    domain_name, code, description
                                )

                arcpy.AddMessage("All domains created successfully.")
        except Exception as e:
            arcpy.AddError(f"Failed to create domains: {e}")

    @staticmethod
    def assign_domains_to_fields(production_feature_class_path):
        try:
            for field_name, properties in Constants.FEATURE_SCHEMA.items():
                domain_name = properties.get("domain")
                if domain_name:
                    arcpy.AddMessage(
                        f"Assigning domain {domain_name} to field {field_name}..."
                    )
                    arcpy.management.AssignDomainToField(
                        in_table=production_feature_class_path,
                        field_name=field_name,
                        domain_name=domain_name,
                    )
                    arcpy.AddMessage(
                        f"Domain {domain_name} assigned to field {field_name} successfully."
                    )

        except Exception as e:
            arcpy.AddError(
                f"Failed to assign domains to fields in {production_feature_class_path}: {e}"
            )


if __name__ == "__main__":
    domain_manager = DomainManager(
        domains_to_create_in_gdb=Constants.DOMAINS_TO_CREATE_IN_GDB,
        production_gdb_path=Constants.PRODUCTION_SDE_CONNECTION_FILE,
    )
    domain_manager.create_domains()
    # domain_manager.assign_domains_to_fields()
