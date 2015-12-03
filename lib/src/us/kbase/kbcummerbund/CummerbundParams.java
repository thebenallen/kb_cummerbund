
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
 * <p>Original spec-file type: cummerbundParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "ws_cuffdiff_id",
    "ws_cummerbund_output"
})
public class CummerbundParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("ws_cuffdiff_id")
    private String wsCuffdiffId;
    @JsonProperty("ws_cummerbund_output")
    private String wsCummerbundOutput;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public CummerbundParams withWorkspaceName(String workspaceName) {
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

    public CummerbundParams withWsCuffdiffId(String wsCuffdiffId) {
        this.wsCuffdiffId = wsCuffdiffId;
        return this;
    }

    @JsonProperty("ws_cummerbund_output")
    public String getWsCummerbundOutput() {
        return wsCummerbundOutput;
    }

    @JsonProperty("ws_cummerbund_output")
    public void setWsCummerbundOutput(String wsCummerbundOutput) {
        this.wsCummerbundOutput = wsCummerbundOutput;
    }

    public CummerbundParams withWsCummerbundOutput(String wsCummerbundOutput) {
        this.wsCummerbundOutput = wsCummerbundOutput;
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
        return ((((((((("CummerbundParams"+" [workspaceName=")+ workspaceName)+", wsCuffdiffId=")+ wsCuffdiffId)+", wsCummerbundOutput=")+ wsCummerbundOutput)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
