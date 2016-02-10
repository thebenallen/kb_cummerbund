/*
   A KBase module: kb_cummerbund
 */

module kb_cummerbund {

	/* indicates true or false values, false <= 0, true >=1 */
	typedef int bool;

	/* workspace name of the object */
	typedef string workspace_name;

	/* @id ws KBaseRNASeq.RNASeqCuffdiffdifferentialExpression */
	typedef string ws_cuffdiff_id;

	/* @id ws KBaseRNASeq.cummerbund_output */
	typedef string ws_cummerbund_output;

	/* @id ws KBaseFeatureValues.ExpressionMatrix */
	typedef string ws_expression_matrix_id;


	typedef structure {
		workspace_name workspace_name;
		ws_cuffdiff_id ws_cuffdiff_id;
		ws_cummerbund_output ws_cummerbund_output;
	} cummerbundParams;

	typedef structure {
		workspace_name workspace_name;
		ws_cuffdiff_id ws_cuffdiff_id;
		ws_expression_matrix_id ws_expression_matrix_id;
		bool include_replicates;
	} expressionMatrixParams;

	typedef structure {
		string sample1;
		string sample2;
		float q_value_cutoff;
		float log2_fold_change_cutoff ;
		int num_genes;
		ws_cuffdiff_id ws_cuffdiff_id;
		ws_expression_matrix_id ws_expression_matrix_id1;
		ws_expression_matrix_id ws_expression_matrix_id2;
		ws_cummerbund_output ws_cummerbund_output;
	} heatmapParams;
	
	typedef structure {
		string sample1;
		string sample2;
		float q_value_cutoff;
		float log2_fold_change_cutoff ;
		int num_genes;
		ws_cuffdiff_id ws_cuffdiff_id;
		ws_expression_matrix_id ws_expression_matrix_id;
	} interactiveHeatmapParams;
	

	async funcdef generate_cummerbund_plots (cummerbundParams) returns (ws_cummerbund_output) authentication required;

	async funcdef create_expression_matrix (expressionMatrixParams) returns (ws_expression_matrix_id) authentication required;
	
	async funcdef create_heatmap_de_genes (heatmapParams) returns (ws_cummerbund_output) authentication required;

	async funcdef create_interactive_heatmap_de_genes (interactiveHeatmapParams) returns (ws_expression_matrix_id) authentication required;

	/*
	#async funcdef create_volcano_plot(volcanoplotParams) returns (ws_cummerbund_output) authentication required;
*/
};
