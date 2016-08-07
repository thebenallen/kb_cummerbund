

function kb_cummerbund(url, auth, auth_cb, timeout, async_job_check_time_ms, async_version) {
    var self = this;

    this.url = url;
    var _url = url;

    this.timeout = timeout;
    var _timeout = timeout;
    
    this.async_job_check_time_ms = async_job_check_time_ms;
    if (!this.async_job_check_time_ms)
        this.async_job_check_time_ms = 5000;
    this.async_version = async_version;

    var _auth = auth ? auth : { 'token' : '', 'user_id' : ''};
    var _auth_cb = auth_cb;


    this.generate_cummerbund_plots = function (cummerbundParams, _callback, _errorCallback, json_rpc_context) {
        if (self.async_version) {
            if (!json_rpc_context)
                json_rpc_context = {};
            json_rpc_context['service_ver'] = self.async_version;
        }
        self.generate_cummerbund_plots_async(cummerbundParams, function(job_id) {
            var _checkCallback = null;
            _checkCallback = function(job_state) {
                if (job_state.finished != 0) {
                    if (!job_state.hasOwnProperty('result'))
                        job_state.result = null;
                    _callback(job_state.result[0]);
                } else {
                    setTimeout(function () {
                        self.generate_cummerbund_plots_check(job_id, _checkCallback, _errorCallback);
                    }, self.async_job_check_time_ms);
                }
            };       
            _checkCallback({finished: 0});
        }, _errorCallback, json_rpc_context);
    };

    this.generate_cummerbund_plots_async = function (cummerbundParams, _callback, _errorCallback, json_rpc_context) {
        if (typeof cummerbundParams === 'function')
            throw 'Argument cummerbundParams can not be a function';
        if (_callback && typeof _callback !== 'function')
            throw 'Argument _callback must be a function if defined';
        if (_errorCallback && typeof _errorCallback !== 'function')
            throw 'Argument _errorCallback must be a function if defined';
        if (typeof arguments === 'function' && arguments.length > 1+2)
            throw 'Too many arguments ('+arguments.length+' instead of '+(1+2)+')';
        return json_call_ajax("kb_cummerbund.generate_cummerbund_plots_async", 
            [cummerbundParams], 1, _callback, _errorCallback, json_rpc_context);
    };
    
    this.generate_cummerbund_plots_check = function (job_id, _callback, _errorCallback) {
        if (typeof job_id === 'function')
            throw 'Argument job_id can not be a function';
        if (_callback && typeof _callback !== 'function')
            throw 'Argument _callback must be a function if defined';
        if (_errorCallback && typeof _errorCallback !== 'function')
            throw 'Argument _errorCallback must be a function if defined';
        if (typeof arguments === 'function' && arguments.length > 3)
            throw 'Too many arguments ('+arguments.length+' instead of 3)';
        return json_call_ajax("kb_cummerbund.generate_cummerbund_plots_check", 
            [job_id], 1, _callback, _errorCallback);
    };
 
    this.generate_cummerbund_plot2 = function (cummerbundstatParams, _callback, _errorCallback, json_rpc_context) {
        if (self.async_version) {
            if (!json_rpc_context)
                json_rpc_context = {};
            json_rpc_context['service_ver'] = self.async_version;
        }
        self.generate_cummerbund_plot2_async(cummerbundstatParams, function(job_id) {
            var _checkCallback = null;
            _checkCallback = function(job_state) {
                if (job_state.finished != 0) {
                    if (!job_state.hasOwnProperty('result'))
                        job_state.result = null;
                    _callback(job_state.result[0]);
                } else {
                    setTimeout(function () {
                        self.generate_cummerbund_plot2_check(job_id, _checkCallback, _errorCallback);
                    }, self.async_job_check_time_ms);
                }
            };       
            _checkCallback({finished: 0});
        }, _errorCallback, json_rpc_context);
    };

    this.generate_cummerbund_plot2_async = function (cummerbundstatParams, _callback, _errorCallback, json_rpc_context) {
        if (typeof cummerbundstatParams === 'function')
            throw 'Argument cummerbundstatParams can not be a function';
        if (_callback && typeof _callback !== 'function')
            throw 'Argument _callback must be a function if defined';
        if (_errorCallback && typeof _errorCallback !== 'function')
            throw 'Argument _errorCallback must be a function if defined';
        if (typeof arguments === 'function' && arguments.length > 1+2)
            throw 'Too many arguments ('+arguments.length+' instead of '+(1+2)+')';
        return json_call_ajax("kb_cummerbund.generate_cummerbund_plot2_async", 
            [cummerbundstatParams], 1, _callback, _errorCallback, json_rpc_context);
    };
    
    this.generate_cummerbund_plot2_check = function (job_id, _callback, _errorCallback) {
        if (typeof job_id === 'function')
            throw 'Argument job_id can not be a function';
        if (_callback && typeof _callback !== 'function')
            throw 'Argument _callback must be a function if defined';
        if (_errorCallback && typeof _errorCallback !== 'function')
            throw 'Argument _errorCallback must be a function if defined';
        if (typeof arguments === 'function' && arguments.length > 3)
            throw 'Too many arguments ('+arguments.length+' instead of 3)';
        return json_call_ajax("kb_cummerbund.generate_cummerbund_plot2_check", 
            [job_id], 1, _callback, _errorCallback);
    };
 
    this.create_expression_matrix = function (expressionMatrixParams, _callback, _errorCallback, json_rpc_context) {
        if (self.async_version) {
            if (!json_rpc_context)
                json_rpc_context = {};
            json_rpc_context['service_ver'] = self.async_version;
        }
        self.create_expression_matrix_async(expressionMatrixParams, function(job_id) {
            var _checkCallback = null;
            _checkCallback = function(job_state) {
                if (job_state.finished != 0) {
                    if (!job_state.hasOwnProperty('result'))
                        job_state.result = null;
                    _callback(job_state.result[0]);
                } else {
                    setTimeout(function () {
                        self.create_expression_matrix_check(job_id, _checkCallback, _errorCallback);
                    }, self.async_job_check_time_ms);
                }
            };       
            _checkCallback({finished: 0});
        }, _errorCallback, json_rpc_context);
    };

    this.create_expression_matrix_async = function (expressionMatrixParams, _callback, _errorCallback, json_rpc_context) {
        if (typeof expressionMatrixParams === 'function')
            throw 'Argument expressionMatrixParams can not be a function';
        if (_callback && typeof _callback !== 'function')
            throw 'Argument _callback must be a function if defined';
        if (_errorCallback && typeof _errorCallback !== 'function')
            throw 'Argument _errorCallback must be a function if defined';
        if (typeof arguments === 'function' && arguments.length > 1+2)
            throw 'Too many arguments ('+arguments.length+' instead of '+(1+2)+')';
        return json_call_ajax("kb_cummerbund.create_expression_matrix_async", 
            [expressionMatrixParams], 1, _callback, _errorCallback, json_rpc_context);
    };
    
    this.create_expression_matrix_check = function (job_id, _callback, _errorCallback) {
        if (typeof job_id === 'function')
            throw 'Argument job_id can not be a function';
        if (_callback && typeof _callback !== 'function')
            throw 'Argument _callback must be a function if defined';
        if (_errorCallback && typeof _errorCallback !== 'function')
            throw 'Argument _errorCallback must be a function if defined';
        if (typeof arguments === 'function' && arguments.length > 3)
            throw 'Too many arguments ('+arguments.length+' instead of 3)';
        return json_call_ajax("kb_cummerbund.create_expression_matrix_check", 
            [job_id], 1, _callback, _errorCallback);
    };
 
    this.create_interactive_heatmap_de_genes = function (interactiveHeatmapParams, _callback, _errorCallback, json_rpc_context) {
        if (self.async_version) {
            if (!json_rpc_context)
                json_rpc_context = {};
            json_rpc_context['service_ver'] = self.async_version;
        }
        self.create_interactive_heatmap_de_genes_async(interactiveHeatmapParams, function(job_id) {
            var _checkCallback = null;
            _checkCallback = function(job_state) {
                if (job_state.finished != 0) {
                    if (!job_state.hasOwnProperty('result'))
                        job_state.result = null;
                    _callback(job_state.result[0]);
                } else {
                    setTimeout(function () {
                        self.create_interactive_heatmap_de_genes_check(job_id, _checkCallback, _errorCallback);
                    }, self.async_job_check_time_ms);
                }
            };       
            _checkCallback({finished: 0});
        }, _errorCallback, json_rpc_context);
    };

    this.create_interactive_heatmap_de_genes_async = function (interactiveHeatmapParams, _callback, _errorCallback, json_rpc_context) {
        if (typeof interactiveHeatmapParams === 'function')
            throw 'Argument interactiveHeatmapParams can not be a function';
        if (_callback && typeof _callback !== 'function')
            throw 'Argument _callback must be a function if defined';
        if (_errorCallback && typeof _errorCallback !== 'function')
            throw 'Argument _errorCallback must be a function if defined';
        if (typeof arguments === 'function' && arguments.length > 1+2)
            throw 'Too many arguments ('+arguments.length+' instead of '+(1+2)+')';
        return json_call_ajax("kb_cummerbund.create_interactive_heatmap_de_genes_async", 
            [interactiveHeatmapParams], 1, _callback, _errorCallback, json_rpc_context);
    };
    
    this.create_interactive_heatmap_de_genes_check = function (job_id, _callback, _errorCallback) {
        if (typeof job_id === 'function')
            throw 'Argument job_id can not be a function';
        if (_callback && typeof _callback !== 'function')
            throw 'Argument _callback must be a function if defined';
        if (_errorCallback && typeof _errorCallback !== 'function')
            throw 'Argument _errorCallback must be a function if defined';
        if (typeof arguments === 'function' && arguments.length > 3)
            throw 'Too many arguments ('+arguments.length+' instead of 3)';
        return json_call_ajax("kb_cummerbund.create_interactive_heatmap_de_genes_check", 
            [job_id], 1, _callback, _errorCallback);
    };
  

    /*
     * JSON call using jQuery method.
     */
    function json_call_ajax(method, params, numRets, callback, errorCallback, json_rpc_context) {
        var deferred = $.Deferred();

        if (typeof callback === 'function') {
           deferred.done(callback);
        }

        if (typeof errorCallback === 'function') {
           deferred.fail(errorCallback);
        }

        var rpc = {
            params : params,
            method : method,
            version: "1.1",
            id: String(Math.random()).slice(2),
        };
        if (json_rpc_context)
            rpc['context'] = json_rpc_context;

        var beforeSend = null;
        var token = (_auth_cb && typeof _auth_cb === 'function') ? _auth_cb()
            : (_auth.token ? _auth.token : null);
        if (token != null) {
            beforeSend = function (xhr) {
                xhr.setRequestHeader("Authorization", token);
            }
        }

        var xhr = jQuery.ajax({
            url: _url,
            dataType: "text",
            type: 'POST',
            processData: false,
            data: JSON.stringify(rpc),
            beforeSend: beforeSend,
            timeout: _timeout,
            success: function (data, status, xhr) {
                var result;
                try {
                    var resp = JSON.parse(data);
                    result = (numRets === 1 ? resp.result[0] : resp.result);
                } catch (err) {
                    deferred.reject({
                        status: 503,
                        error: err,
                        url: _url,
                        resp: data
                    });
                    return;
                }
                deferred.resolve(result);
            },
            error: function (xhr, textStatus, errorThrown) {
                var error;
                if (xhr.responseText) {
                    try {
                        var resp = JSON.parse(xhr.responseText);
                        error = resp.error;
                    } catch (err) { // Not JSON
                        error = "Unknown error - " + xhr.responseText;
                    }
                } else {
                    error = "Unknown Error";
                }
                deferred.reject({
                    status: 500,
                    error: error
                });
            }
        });

        var promise = deferred.promise();
        promise.xhr = xhr;
        return promise;
    }
}


