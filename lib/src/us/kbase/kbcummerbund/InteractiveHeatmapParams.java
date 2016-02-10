
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
 * <p>Original spec-file type: interactiveHeatmapParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "sample1",
    "sample2",
    "q_value_cutoff",
    "log2_fold_change_cutoff",
    "num_genes",
    "ws_cuffdiff_id",
    "ws_expression_matrix_id"
})
public class InteractiveHeatmapParams {

    @JsonProperty("sample1")
    private String sample1;
    @JsonProperty("sample2")
    private String sample2;
    @JsonProperty("q_value_cutoff")
    private Double qValueCutoff;
    @JsonProperty("log2_fold_change_cutoff")
    private Double log2FoldChangeCutoff;
    @JsonProperty("num_genes")
    private Long numGenes;
    @JsonProperty("ws_cuffdiff_id")
    private String wsCuffdiffId;
    @JsonProperty("ws_expression_matrix_id")
    private String wsExpressionMatrixId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("sample1")
    public String getSample1() {
        return sample1;
    }

    @JsonProperty("sample1")
    public void setSample1(String sample1) {
        this.sample1 = sample1;
    }

    public InteractiveHeatmapParams withSample1(String sample1) {
        this.sample1 = sample1;
        return this;
    }

    @JsonProperty("sample2")
    public String getSample2() {
        return sample2;
    }

    @JsonProperty("sample2")
    public void setSample2(String sample2) {
        this.sample2 = sample2;
    }

    public InteractiveHeatmapParams withSample2(String sample2) {
        this.sample2 = sample2;
        return this;
    }

    @JsonProperty("q_value_cutoff")
    public Double getQValueCutoff() {
        return qValueCutoff;
    }

    @JsonProperty("q_value_cutoff")
    public void setQValueCutoff(Double qValueCutoff) {
        this.qValueCutoff = qValueCutoff;
    }

    public InteractiveHeatmapParams withQValueCutoff(Double qValueCutoff) {
        this.qValueCutoff = qValueCutoff;
        return this;
    }

    @JsonProperty("log2_fold_change_cutoff")
    public Double getLog2FoldChangeCutoff() {
        return log2FoldChangeCutoff;
    }

    @JsonProperty("log2_fold_change_cutoff")
    public void setLog2FoldChangeCutoff(Double log2FoldChangeCutoff) {
        this.log2FoldChangeCutoff = log2FoldChangeCutoff;
    }

    public InteractiveHeatmapParams withLog2FoldChangeCutoff(Double log2FoldChangeCutoff) {
        this.log2FoldChangeCutoff = log2FoldChangeCutoff;
        return this;
    }

    @JsonProperty("num_genes")
    public Long getNumGenes() {
        return numGenes;
    }

    @JsonProperty("num_genes")
    public void setNumGenes(Long numGenes) {
        this.numGenes = numGenes;
    }

    public InteractiveHeatmapParams withNumGenes(Long numGenes) {
        this.numGenes = numGenes;
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

    public InteractiveHeatmapParams withWsCuffdiffId(String wsCuffdiffId) {
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

    public InteractiveHeatmapParams withWsExpressionMatrixId(String wsExpressionMatrixId) {
        this.wsExpressionMatrixId = wsExpressionMatrixId;
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
        return ((((((((((((((((("InteractiveHeatmapParams"+" [sample1=")+ sample1)+", sample2=")+ sample2)+", qValueCutoff=")+ qValueCutoff)+", log2FoldChangeCutoff=")+ log2FoldChangeCutoff)+", numGenes=")+ numGenes)+", wsCuffdiffId=")+ wsCuffdiffId)+", wsExpressionMatrixId=")+ wsExpressionMatrixId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
