
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
 * <p>Original spec-file type: cummerbundstatParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace",
    "ws_cuffdiff_id",
    "ws_cummerbund_output",
    "ws_diffstat_output"
})
public class CummerbundstatParams {

    @JsonProperty("workspace")
    private String workspace;
    @JsonProperty("ws_cuffdiff_id")
    private String wsCuffdiffId;
    @JsonProperty("ws_cummerbund_output")
    private String wsCummerbundOutput;
    @JsonProperty("ws_diffstat_output")
    private String wsDiffstatOutput;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace")
    public String getWorkspace() {
        return workspace;
    }

    @JsonProperty("workspace")
    public void setWorkspace(String workspace) {
        this.workspace = workspace;
    }

    public CummerbundstatParams withWorkspace(String workspace) {
        this.workspace = workspace;
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

    public CummerbundstatParams withWsCuffdiffId(String wsCuffdiffId) {
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

    public CummerbundstatParams withWsCummerbundOutput(String wsCummerbundOutput) {
        this.wsCummerbundOutput = wsCummerbundOutput;
        return this;
    }

    @JsonProperty("ws_diffstat_output")
    public String getWsDiffstatOutput() {
        return wsDiffstatOutput;
    }

    @JsonProperty("ws_diffstat_output")
    public void setWsDiffstatOutput(String wsDiffstatOutput) {
        this.wsDiffstatOutput = wsDiffstatOutput;
    }

    public CummerbundstatParams withWsDiffstatOutput(String wsDiffstatOutput) {
        this.wsDiffstatOutput = wsDiffstatOutput;
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
        return ((((((((((("CummerbundstatParams"+" [workspace=")+ workspace)+", wsCuffdiffId=")+ wsCuffdiffId)+", wsCummerbundOutput=")+ wsCummerbundOutput)+", wsDiffstatOutput=")+ wsDiffstatOutput)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
