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


  	 async funcdef generate_cummerbund_plots (cummerbundParams) returns (ws_cummerbund_output) authentication required;

     async funcdef create_expression_matrix (expressionMatrixParams) returns (ws_expression_matrix_id) authentication required;
};
