/*
A KBase module: kb_cummerbund
*/

module kb_cummerbund {
	/*
	Insert your typespec information here.
	*/
	typedef string workspace_name;

	/*
	A string representing input ws object  cuffdiff_results_id.
	*/

	typedef string cuffdiff_results_id;

	/*
	A string representing output  cummerbund_results_id.

	*/
	typedef string cummerbund_results_id;

	/*
	Generate plots
	store data for plots in cummerbund_results_id
	*/
	async funcdef generate_plots(workspace_name, cuffdiff_results_id) returns (cummerbund_results_id) authentication required;

};
