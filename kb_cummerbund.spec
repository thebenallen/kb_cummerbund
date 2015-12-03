/*
A KBase module: kb_cummerbund
*/




module kb_cummerbund {

        /* workspace name of the object */

	typedef string workspace_name;

	/* object of type: KBaseRNASeq.RNASeqCuffdiffdifferentialExpression */

	typedef string ws_cuffdiff_id;

	/* object of type: KBaseRNASeq.cummerbund_output */

	typedef string ws_cummerbund_output;



	typedef structure {
		workspace_name workspace_name;
		ws_cuffdiff_id ws_cuffdiff_id;
		ws_cummerbund_output ws_cummerbund_output;
	} cummerbundParams;


	async funcdef generate_cummerbund_plots (cummerbundParams) returns (ws_cummerbund_output) authentication required;

};
