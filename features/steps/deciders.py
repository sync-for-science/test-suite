class StepDecider:
    """
    Determines at the step level if a test should be run.
    """

    def __init__(self, context):
        """
        Behave context of currently running step.
        :param context: A Behave framework context
        """
        self.context = context

    def __skip_context(self):
        return self.context.vendor_skip

    def should_run_test(self):
        return not self.__skip_context()


class ResourceDecider(object):
    """
    Determines if a resource should be validated based on Argonaut Value Sets.
    """
    def __init__(self, resource):
        self.resource = resource

    def _needs_argo_validation(self):
        pass

    def should_validate(self):
        return self._needs_argo_validation()


class ArgonautObservationDecider(ResourceDecider):

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

    def _needs_argo_validation(self):

        if self.resource["resourceType"] != "Observation":
            return True

        category_codes = [category.get('code', None)
                          for category in self.resource.get("category", {}).get("coding", {})]

        if 'vital-signs' not in category_codes:
            return True

        codings = [code.get("code", None)
                   for code in self.resource.get('code', {}).get('coding', {})]

        if any(code in self.argo_vital_codes for code in codings):
            return True
