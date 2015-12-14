
package us.kbase.kbcummerbund;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: expressionMatrixParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "ws_cuffdiff_id",
    "ws_expression_matrix_id",
    "include_replicates"
})
public class ExpressionMatrixParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("ws_cuffdiff_id")
    private String wsCuffdiffId;
    @JsonProperty("ws_expression_matrix_id")
    private String wsExpressionMatrixId;
    @JsonProperty("include_replicates")
    private Long includeReplicates;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ExpressionMatrixParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("ws_cuffdiff_id")
    public String getWsCuffdiffId() {
        return wsCuffdiffId;
    }

    @JsonProperty("ws_cuffdiff_id")
    public void setWsCuffdiffId(String wsCuffdiffId) {
        this.wsCuffdiffId = wsCuffdiffId;
    }

    public ExpressionMatrixParams withWsCuffdiffId(String wsCuffdiffId) {
        this.wsCuffdiffId = wsCuffdiffId;
        return this;
    }

    @JsonProperty("ws_expression_matrix_id")
    public String getWsExpressionMatrixId() {
        return wsExpressionMatrixId;
    }

    @JsonProperty("ws_expression_matrix_id")
    public void setWsExpressionMatrixId(String wsExpressionMatrixId) {
        this.wsExpressionMatrixId = wsExpressionMatrixId;
    }

    public ExpressionMatrixParams withWsExpressionMatrixId(String wsExpressionMatrixId) {
        this.wsExpressionMatrixId = wsExpressionMatrixId;
        return this;
    }

    @JsonProperty("include_replicates")
    public Long getIncludeReplicates() {
        return includeReplicates;
    }

    @JsonProperty("include_replicates")
    public void setIncludeReplicates(Long includeReplicates) {
        this.includeReplicates = includeReplicates;
    }

    public ExpressionMatrixParams withIncludeReplicates(Long includeReplicates) {
        this.includeReplicates = includeReplicates;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((("ExpressionMatrixParams"+" [workspaceName=")+ workspaceName)+", wsCuffdiffId=")+ wsCuffdiffId)+", wsExpressionMatrixId=")+ wsExpressionMatrixId)+", includeReplicates=")+ includeReplicates)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
