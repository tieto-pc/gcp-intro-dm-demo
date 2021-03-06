import common
import vpc
import vm


def GenerateConfig(context):
    """Creates the infra resources. Calls infra modules."""
    if common.MY_DEBUG:
        print 'ENTER deployment.GenerateConfig'
    resources = []
    resources += vpc.getResource(context)
    resources += vm.getResource(context)
    if common.MY_DEBUG:
        print 'EXIT deployment.GenerateConfig, resources: ' + str(resources)
    return {'resources': resources}

