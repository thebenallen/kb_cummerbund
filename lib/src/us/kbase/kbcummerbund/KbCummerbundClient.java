package us.kbase.kbcummerbund;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JobState;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: kb_cummerbund</p>
 * <pre>
 * A KBase module: kb_cummerbund
 * </pre>
 */
public class KbCummerbundClient {
    private JsonClientCaller caller;
    private long asyncJobCheckTimeMs = 100;
    private int asyncJobCheckTimeScalePercent = 150;
    private long asyncJobCheckMaxTimeMs = 300000;  // 5 minutes
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public KbCummerbundClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public KbCummerbundClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public KbCummerbundClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public KbCummerbundClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public long getAsyncJobCheckTimeMs() {
        return this.asyncJobCheckTimeMs;
    }

    public void setAsyncJobCheckTimeMs(long newValue) {
        this.asyncJobCheckTimeMs = newValue;
    }

    public int getAsyncJobCheckTimeScalePercent() {
        return this.asyncJobCheckTimeScalePercent;
    }

    public void setAsyncJobCheckTimeScalePercent(int newValue) {
        this.asyncJobCheckTimeScalePercent = newValue;
    }

    public long getAsyncJobCheckMaxTimeMs() {
        return this.asyncJobCheckMaxTimeMs;
    }

    public void setAsyncJobCheckMaxTimeMs(long newValue) {
        this.asyncJobCheckMaxTimeMs = newValue;
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    protected <T> JobState<T> _checkJob(String jobId, TypeReference<List<JobState<T>>> retType) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(jobId);
        List<JobState<T>> res = caller.jsonrpcCall("kb_cummerbund._check_job", args, retType, true, true);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: generate_cummerbund_plots</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.CummerbundParams CummerbundParams} (original type "cummerbundParams")
     * @return   instance of original type "ws_cummerbund_output" (@id ws KBaseRNASeq.cummerbund_output)
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    protected String _generateCummerbundPlotsSubmit(CummerbundParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("kb_cummerbund._generate_cummerbund_plots_submit", args, retType, true, true, jsonRpcContext);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: generate_cummerbund_plots</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.CummerbundParams CummerbundParams} (original type "cummerbundParams")
     * @return   instance of original type "ws_cummerbund_output" (@id ws KBaseRNASeq.cummerbund_output)
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public String generateCummerbundPlots(CummerbundParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        String jobId = _generateCummerbundPlotsSubmit(arg1, jsonRpcContext);
        TypeReference<List<JobState<List<String>>>> retType = new TypeReference<List<JobState<List<String>>>>() {};
        long asyncJobCheckTimeMs = this.asyncJobCheckTimeMs;
        while (true) {
            if (Thread.currentThread().isInterrupted())
                throw new JsonClientException("Thread was interrupted");
            try { 
                Thread.sleep(asyncJobCheckTimeMs);
            } catch(Exception ex) {
                throw new JsonClientException("Thread was interrupted", ex);
            }
            asyncJobCheckTimeMs = Math.min(asyncJobCheckTimeMs * this.asyncJobCheckTimeScalePercent / 100, this.asyncJobCheckMaxTimeMs);
            JobState<List<String>> res = _checkJob(jobId, retType);
            if (res.getFinished() != 0L)
                return res.getResult().get(0);
        }
    }

    /**
     * <p>Original spec-file function name: generate_cummerbund_plot2</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.CummerbundstatParams CummerbundstatParams} (original type "cummerbundstatParams")
     * @return   instance of original type "ws_cummerbund_output" (@id ws KBaseRNASeq.cummerbund_output)
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    protected String _generateCummerbundPlot2Submit(CummerbundstatParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("kb_cummerbund._generate_cummerbund_plot2_submit", args, retType, true, true, jsonRpcContext);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: generate_cummerbund_plot2</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.CummerbundstatParams CummerbundstatParams} (original type "cummerbundstatParams")
     * @return   instance of original type "ws_cummerbund_output" (@id ws KBaseRNASeq.cummerbund_output)
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public String generateCummerbundPlot2(CummerbundstatParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        String jobId = _generateCummerbundPlot2Submit(arg1, jsonRpcContext);
        TypeReference<List<JobState<List<String>>>> retType = new TypeReference<List<JobState<List<String>>>>() {};
        long asyncJobCheckTimeMs = this.asyncJobCheckTimeMs;
        while (true) {
            if (Thread.currentThread().isInterrupted())
                throw new JsonClientException("Thread was interrupted");
            try { 
                Thread.sleep(asyncJobCheckTimeMs);
            } catch(Exception ex) {
                throw new JsonClientException("Thread was interrupted", ex);
            }
            asyncJobCheckTimeMs = Math.min(asyncJobCheckTimeMs * this.asyncJobCheckTimeScalePercent / 100, this.asyncJobCheckMaxTimeMs);
            JobState<List<String>> res = _checkJob(jobId, retType);
            if (res.getFinished() != 0L)
                return res.getResult().get(0);
        }
    }

    /**
     * <p>Original spec-file function name: create_expression_matrix</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.ExpressionMatrixParams ExpressionMatrixParams} (original type "expressionMatrixParams")
     * @return   instance of original type "ws_expression_matrix_id" (@id ws KBaseFeatureValues.ExpressionMatrix)
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    protected String _createExpressionMatrixSubmit(ExpressionMatrixParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("kb_cummerbund._create_expression_matrix_submit", args, retType, true, true, jsonRpcContext);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: create_expression_matrix</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.ExpressionMatrixParams ExpressionMatrixParams} (original type "expressionMatrixParams")
     * @return   instance of original type "ws_expression_matrix_id" (@id ws KBaseFeatureValues.ExpressionMatrix)
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public String createExpressionMatrix(ExpressionMatrixParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        String jobId = _createExpressionMatrixSubmit(arg1, jsonRpcContext);
        TypeReference<List<JobState<List<String>>>> retType = new TypeReference<List<JobState<List<String>>>>() {};
        long asyncJobCheckTimeMs = this.asyncJobCheckTimeMs;
        while (true) {
            if (Thread.currentThread().isInterrupted())
                throw new JsonClientException("Thread was interrupted");
            try { 
                Thread.sleep(asyncJobCheckTimeMs);
            } catch(Exception ex) {
                throw new JsonClientException("Thread was interrupted", ex);
            }
            asyncJobCheckTimeMs = Math.min(asyncJobCheckTimeMs * this.asyncJobCheckTimeScalePercent / 100, this.asyncJobCheckMaxTimeMs);
            JobState<List<String>> res = _checkJob(jobId, retType);
            if (res.getFinished() != 0L)
                return res.getResult().get(0);
        }
    }

    /**
     * <p>Original spec-file function name: create_interactive_heatmap_de_genes</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.InteractiveHeatmapParams InteractiveHeatmapParams} (original type "interactiveHeatmapParams")
     * @return   instance of type {@link us.kbase.kbcummerbund.ResultsToReport ResultsToReport}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    protected String _createInteractiveHeatmapDeGenesSubmit(InteractiveHeatmapParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("kb_cummerbund._create_interactive_heatmap_de_genes_submit", args, retType, true, true, jsonRpcContext);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: create_interactive_heatmap_de_genes</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.InteractiveHeatmapParams InteractiveHeatmapParams} (original type "interactiveHeatmapParams")
     * @return   instance of type {@link us.kbase.kbcummerbund.ResultsToReport ResultsToReport}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ResultsToReport createInteractiveHeatmapDeGenes(InteractiveHeatmapParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        String jobId = _createInteractiveHeatmapDeGenesSubmit(arg1, jsonRpcContext);
        TypeReference<List<JobState<List<ResultsToReport>>>> retType = new TypeReference<List<JobState<List<ResultsToReport>>>>() {};
        long asyncJobCheckTimeMs = this.asyncJobCheckTimeMs;
        while (true) {
            if (Thread.currentThread().isInterrupted())
                throw new JsonClientException("Thread was interrupted");
            try { 
                Thread.sleep(asyncJobCheckTimeMs);
            } catch(Exception ex) {
                throw new JsonClientException("Thread was interrupted", ex);
            }
            asyncJobCheckTimeMs = Math.min(asyncJobCheckTimeMs * this.asyncJobCheckTimeScalePercent / 100, this.asyncJobCheckMaxTimeMs);
            JobState<List<ResultsToReport>> res = _checkJob(jobId, retType);
            if (res.getFinished() != 0L)
                return res.getResult().get(0);
        }
    }

    /**
     * <p>Original spec-file function name: create_interactive_heatmap_de_genes_old</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.HeatmapParams HeatmapParams} (original type "heatmapParams")
     * @return   instance of type {@link us.kbase.kbcummerbund.ResultsToReport ResultsToReport}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    protected String _createInteractiveHeatmapDeGenesOldSubmit(HeatmapParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("kb_cummerbund._create_interactive_heatmap_de_genes_old_submit", args, retType, true, true, jsonRpcContext);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: create_interactive_heatmap_de_genes_old</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.kbcummerbund.HeatmapParams HeatmapParams} (original type "heatmapParams")
     * @return   instance of type {@link us.kbase.kbcummerbund.ResultsToReport ResultsToReport}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ResultsToReport createInteractiveHeatmapDeGenesOld(HeatmapParams arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        String jobId = _createInteractiveHeatmapDeGenesOldSubmit(arg1, jsonRpcContext);
        TypeReference<List<JobState<List<ResultsToReport>>>> retType = new TypeReference<List<JobState<List<ResultsToReport>>>>() {};
        long asyncJobCheckTimeMs = this.asyncJobCheckTimeMs;
        while (true) {
            if (Thread.currentThread().isInterrupted())
                throw new JsonClientException("Thread was interrupted");
            try { 
                Thread.sleep(asyncJobCheckTimeMs);
            } catch(Exception ex) {
                throw new JsonClientException("Thread was interrupted", ex);
            }
            asyncJobCheckTimeMs = Math.min(asyncJobCheckTimeMs * this.asyncJobCheckTimeScalePercent / 100, this.asyncJobCheckMaxTimeMs);
            JobState<List<ResultsToReport>> res = _checkJob(jobId, retType);
            if (res.getFinished() != 0L)
                return res.getResult().get(0);
        }
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("kb_cummerbund.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
