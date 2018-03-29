class StepDecider:
    """
    Determines at the step level if a test should be run.
    """

    def __init__(self, context):
        """
        Behave context of currently running step.
        :param context: 
        """
        self.context = context

    def __skip_context(self):
        return self.context.vendor_skip

    def should_run_test(self):
        return self.__skip_context()


class ResourceDecider:
    """
    Determines if a resource should be validated based on Argonaut Value Sets.
    """
    argo_vital_codes = ["8716-3",
                        "9279-1",
                        "8867-4",
                        "59408-5",
                        "8310-5",
                        "8302-2",
                        "8306-3",
                        "8287-5",
                        "29463-7",
                        "39156-5",
                        "55284-4",
                        "8480-6",
                        "8462-4"]

    def __init__(self, resource):
        self.resource = resource

    def __needs_argo_validation(self):

        validate = False
        found_validation_toggle = False

        try:
            for category_coding in self.resource["category"]["coding"]:
                if category_coding["code"] == "vital-signs":
                    found_validation_toggle = True
                    for code in self.resource['code']['coding']:
                        if code["code"] in self.argo_vital_codes:
                            validate = True
        except KeyError:
            validate = False
        except TypeError:
            validate = False

        if not found_validation_toggle:
            validate = True

        return validate

    def should_validate(self):
        return self.__needs_argo_validation()