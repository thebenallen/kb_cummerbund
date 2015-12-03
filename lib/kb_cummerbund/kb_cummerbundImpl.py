#BEGIN_HEADER
from biokbase.workspace.client import Workspace as workspaceService
#END_HEADER


class kb_cummerbund:
    '''
    Module Name:
    kb_cummerbund

    Module Description:
    A KBase module: kb_cummerbund
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
	self.workspaceURL = config['workspace-url']
        #END_CONSTRUCTOR
        pass

    def generate_cummerbund_plots(self, ctx, cummerbundParams):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN generate_cummerbund_plots
        #END generate_cummerbund_plots

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method generate_cummerbund_plots return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]
