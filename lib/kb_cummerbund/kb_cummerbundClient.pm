package kb_cummerbund::kb_cummerbundClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
use Time::HiRes;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

kb_cummerbund::kb_cummerbundClient

=head1 DESCRIPTION


A KBase module: kb_cummerbund


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => kb_cummerbund::kb_cummerbundClient::RpcClient->new,
	url => $url,
	headers => [],
    };
    my %arg_hash = @args;
    my $async_job_check_time = 5.0;
    if (exists $arg_hash{"async_job_check_time_ms"}) {
        $async_job_check_time = $arg_hash{"async_job_check_time_ms"} / 1000.0;
    }
    $self->{async_job_check_time} = $async_job_check_time;

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my $token = Bio::KBase::AuthToken->new(@args);
	
	if (!$token->error_message)
	{
	    $self->{token} = $token->token;
	    $self->{client}->{token} = $token->token;
	}
        else
        {
	    #
	    # All methods in this module require authentication. In this case, if we
	    # don't have a token, we can't continue.
	    #
	    die "Authentication failed: " . $token->error_message;
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 generate_cummerbund_plots

  $return = $obj->generate_cummerbund_plots($cummerbundParams)

=over 4

=item Parameter and return types

=begin html

<pre>
$cummerbundParams is a kb_cummerbund.cummerbundParams
$return is a kb_cummerbund.ws_cummerbund_output
cummerbundParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_cummerbund.workspace_name
	ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
	ws_cummerbund_output has a value which is a kb_cummerbund.ws_cummerbund_output
workspace_name is a string
ws_cuffdiff_id is a string
ws_cummerbund_output is a string

</pre>

=end html

=begin text

$cummerbundParams is a kb_cummerbund.cummerbundParams
$return is a kb_cummerbund.ws_cummerbund_output
cummerbundParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_cummerbund.workspace_name
	ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
	ws_cummerbund_output has a value which is a kb_cummerbund.ws_cummerbund_output
workspace_name is a string
ws_cuffdiff_id is a string
ws_cummerbund_output is a string


=end text

=item Description



=back

=cut

sub generate_cummerbund_plots
{
    my($self, @args) = @_;
    my $job_id = $self->generate_cummerbund_plots_async(@args);
    while (1) {
        Time::HiRes::sleep($self->{async_job_check_time});
        my $job_state_ref = $self->generate_cummerbund_plots_check($job_id);
        if ($job_state_ref->{"finished"} != 0) {
            if (!exists $job_state_ref->{"result"}) {
                $job_state_ref->{"result"} = [];
            }
            return wantarray ? @{$job_state_ref->{"result"}} : $job_state_ref->{"result"}->[0];
        }
    }
}

sub generate_cummerbund_plots_async {
    my($self, @args) = @_;
# Authentication: required
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function generate_cummerbund_plots_async (received $n, expecting 1)");
    }
    {
        my($cummerbundParams) = @args;
        my @_bad_arguments;
        (ref($cummerbundParams) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"cummerbundParams\" (value was \"$cummerbundParams\")");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to generate_cummerbund_plots_async:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => 'generate_cummerbund_plots_async');
        }
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cummerbund.generate_cummerbund_plots_async",
        params => \@args});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'generate_cummerbund_plots_async',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
            );
        } else {
            return $result->result->[0];  # job_id
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method generate_cummerbund_plots_async",
                        status_line => $self->{client}->status_line,
                        method_name => 'generate_cummerbund_plots_async');
    }
}

sub generate_cummerbund_plots_check {
    my($self, @args) = @_;
# Authentication: required
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function generate_cummerbund_plots_check (received $n, expecting 1)");
    }
    {
        my($job_id) = @args;
        my @_bad_arguments;
        (!ref($job_id)) or push(@_bad_arguments, "Invalid type for argument 0 \"job_id\" (it should be a string)");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to generate_cummerbund_plots_check:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => 'generate_cummerbund_plots_check');
        }
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cummerbund.generate_cummerbund_plots_check",
        params => \@args});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'generate_cummerbund_plots_check',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method generate_cummerbund_plots_check",
                        status_line => $self->{client}->status_line,
                        method_name => 'generate_cummerbund_plots_check');
    }
}
  


=head2 create_expression_matrix

  $return = $obj->create_expression_matrix($expressionMatrixParams)

=over 4

=item Parameter and return types

=begin html

<pre>
$expressionMatrixParams is a kb_cummerbund.expressionMatrixParams
$return is a kb_cummerbund.ws_expression_matrix_id
expressionMatrixParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_cummerbund.workspace_name
	ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
	ws_expression_matrix_id has a value which is a kb_cummerbund.ws_expression_matrix_id
	include_replicates has a value which is a kb_cummerbund.bool
workspace_name is a string
ws_cuffdiff_id is a string
ws_expression_matrix_id is a string
bool is an int

</pre>

=end html

=begin text

$expressionMatrixParams is a kb_cummerbund.expressionMatrixParams
$return is a kb_cummerbund.ws_expression_matrix_id
expressionMatrixParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_cummerbund.workspace_name
	ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
	ws_expression_matrix_id has a value which is a kb_cummerbund.ws_expression_matrix_id
	include_replicates has a value which is a kb_cummerbund.bool
workspace_name is a string
ws_cuffdiff_id is a string
ws_expression_matrix_id is a string
bool is an int


=end text

=item Description



=back

=cut

sub create_expression_matrix
{
    my($self, @args) = @_;
    my $job_id = $self->create_expression_matrix_async(@args);
    while (1) {
        Time::HiRes::sleep($self->{async_job_check_time});
        my $job_state_ref = $self->create_expression_matrix_check($job_id);
        if ($job_state_ref->{"finished"} != 0) {
            if (!exists $job_state_ref->{"result"}) {
                $job_state_ref->{"result"} = [];
            }
            return wantarray ? @{$job_state_ref->{"result"}} : $job_state_ref->{"result"}->[0];
        }
    }
}

sub create_expression_matrix_async {
    my($self, @args) = @_;
# Authentication: required
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function create_expression_matrix_async (received $n, expecting 1)");
    }
    {
        my($expressionMatrixParams) = @args;
        my @_bad_arguments;
        (ref($expressionMatrixParams) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"expressionMatrixParams\" (value was \"$expressionMatrixParams\")");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to create_expression_matrix_async:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => 'create_expression_matrix_async');
        }
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cummerbund.create_expression_matrix_async",
        params => \@args});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'create_expression_matrix_async',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
            );
        } else {
            return $result->result->[0];  # job_id
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method create_expression_matrix_async",
                        status_line => $self->{client}->status_line,
                        method_name => 'create_expression_matrix_async');
    }
}

sub create_expression_matrix_check {
    my($self, @args) = @_;
# Authentication: required
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function create_expression_matrix_check (received $n, expecting 1)");
    }
    {
        my($job_id) = @args;
        my @_bad_arguments;
        (!ref($job_id)) or push(@_bad_arguments, "Invalid type for argument 0 \"job_id\" (it should be a string)");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to create_expression_matrix_check:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => 'create_expression_matrix_check');
        }
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cummerbund.create_expression_matrix_check",
        params => \@args});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'create_expression_matrix_check',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method create_expression_matrix_check",
                        status_line => $self->{client}->status_line,
                        method_name => 'create_expression_matrix_check');
    }
}
  


=head2 create_interactive_heatmap_de_genes

  $return = $obj->create_interactive_heatmap_de_genes($interactiveHeatmapParams)

=over 4

=item Parameter and return types

=begin html

<pre>
$interactiveHeatmapParams is a kb_cummerbund.interactiveHeatmapParams
$return is a kb_cummerbund.ws_expression_matrix_id
interactiveHeatmapParams is a reference to a hash where the following keys are defined:
	sample1 has a value which is a string
	sample2 has a value which is a string
	q_value_cutoff has a value which is a float
	log2_fold_change_cutoff has a value which is a float
	num_genes has a value which is an int
	ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
	ws_expression_matrix_id has a value which is a kb_cummerbund.ws_expression_matrix_id
ws_cuffdiff_id is a string
ws_expression_matrix_id is a string

</pre>

=end html

=begin text

$interactiveHeatmapParams is a kb_cummerbund.interactiveHeatmapParams
$return is a kb_cummerbund.ws_expression_matrix_id
interactiveHeatmapParams is a reference to a hash where the following keys are defined:
	sample1 has a value which is a string
	sample2 has a value which is a string
	q_value_cutoff has a value which is a float
	log2_fold_change_cutoff has a value which is a float
	num_genes has a value which is an int
	ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
	ws_expression_matrix_id has a value which is a kb_cummerbund.ws_expression_matrix_id
ws_cuffdiff_id is a string
ws_expression_matrix_id is a string


=end text

=item Description



=back

=cut

sub create_interactive_heatmap_de_genes
{
    my($self, @args) = @_;
    my $job_id = $self->create_interactive_heatmap_de_genes_async(@args);
    while (1) {
        Time::HiRes::sleep($self->{async_job_check_time});
        my $job_state_ref = $self->create_interactive_heatmap_de_genes_check($job_id);
        if ($job_state_ref->{"finished"} != 0) {
            if (!exists $job_state_ref->{"result"}) {
                $job_state_ref->{"result"} = [];
            }
            return wantarray ? @{$job_state_ref->{"result"}} : $job_state_ref->{"result"}->[0];
        }
    }
}

sub create_interactive_heatmap_de_genes_async {
    my($self, @args) = @_;
# Authentication: required
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function create_interactive_heatmap_de_genes_async (received $n, expecting 1)");
    }
    {
        my($interactiveHeatmapParams) = @args;
        my @_bad_arguments;
        (ref($interactiveHeatmapParams) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"interactiveHeatmapParams\" (value was \"$interactiveHeatmapParams\")");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to create_interactive_heatmap_de_genes_async:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => 'create_interactive_heatmap_de_genes_async');
        }
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cummerbund.create_interactive_heatmap_de_genes_async",
        params => \@args});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'create_interactive_heatmap_de_genes_async',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
            );
        } else {
            return $result->result->[0];  # job_id
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method create_interactive_heatmap_de_genes_async",
                        status_line => $self->{client}->status_line,
                        method_name => 'create_interactive_heatmap_de_genes_async');
    }
}

sub create_interactive_heatmap_de_genes_check {
    my($self, @args) = @_;
# Authentication: required
    if ((my $n = @args) != 1) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function create_interactive_heatmap_de_genes_check (received $n, expecting 1)");
    }
    {
        my($job_id) = @args;
        my @_bad_arguments;
        (!ref($job_id)) or push(@_bad_arguments, "Invalid type for argument 0 \"job_id\" (it should be a string)");
        if (@_bad_arguments) {
            my $msg = "Invalid arguments passed to create_interactive_heatmap_de_genes_check:\n" . join("", map { "\t$_\n" } @_bad_arguments);
            Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
                                   method_name => 'create_interactive_heatmap_de_genes_check');
        }
    }
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cummerbund.create_interactive_heatmap_de_genes_check",
        params => \@args});
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'create_interactive_heatmap_de_genes_check',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method create_interactive_heatmap_de_genes_check",
                        status_line => $self->{client}->status_line,
                        method_name => 'create_interactive_heatmap_de_genes_check');
    }
}
  
  

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_cummerbund.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'create_interactive_heatmap_de_genes',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method create_interactive_heatmap_de_genes",
            status_line => $self->{client}->status_line,
            method_name => 'create_interactive_heatmap_de_genes',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for kb_cummerbund::kb_cummerbundClient\n";
    }
    if ($sMajor == 0) {
        warn "kb_cummerbund::kb_cummerbundClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 bool

=over 4



=item Description

indicates true or false values, false <= 0, true >=1


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 workspace_name

=over 4



=item Description

workspace name of the object


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 ws_cuffdiff_id

=over 4



=item Description

@id ws KBaseRNASeq.RNASeqCuffdiffdifferentialExpression


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 ws_cummerbund_output

=over 4



=item Description

@id ws KBaseRNASeq.cummerbund_output


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 ws_expression_matrix_id

=over 4



=item Description

@id ws KBaseFeatureValues.ExpressionMatrix


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 cummerbundParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_cummerbund.workspace_name
ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
ws_cummerbund_output has a value which is a kb_cummerbund.ws_cummerbund_output

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_cummerbund.workspace_name
ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
ws_cummerbund_output has a value which is a kb_cummerbund.ws_cummerbund_output


=end text

=back



=head2 expressionMatrixParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_cummerbund.workspace_name
ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
ws_expression_matrix_id has a value which is a kb_cummerbund.ws_expression_matrix_id
include_replicates has a value which is a kb_cummerbund.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_cummerbund.workspace_name
ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
ws_expression_matrix_id has a value which is a kb_cummerbund.ws_expression_matrix_id
include_replicates has a value which is a kb_cummerbund.bool


=end text

=back



=head2 heatmapParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
sample1 has a value which is a string
sample2 has a value which is a string
q_value_cutoff has a value which is a float
log2_fold_change_cutoff has a value which is a float
num_genes has a value which is an int
ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
ws_expression_matrix_id1 has a value which is a kb_cummerbund.ws_expression_matrix_id
ws_expression_matrix_id2 has a value which is a kb_cummerbund.ws_expression_matrix_id
ws_cummerbund_output has a value which is a kb_cummerbund.ws_cummerbund_output

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
sample1 has a value which is a string
sample2 has a value which is a string
q_value_cutoff has a value which is a float
log2_fold_change_cutoff has a value which is a float
num_genes has a value which is an int
ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
ws_expression_matrix_id1 has a value which is a kb_cummerbund.ws_expression_matrix_id
ws_expression_matrix_id2 has a value which is a kb_cummerbund.ws_expression_matrix_id
ws_cummerbund_output has a value which is a kb_cummerbund.ws_cummerbund_output


=end text

=back



=head2 interactiveHeatmapParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
sample1 has a value which is a string
sample2 has a value which is a string
q_value_cutoff has a value which is a float
log2_fold_change_cutoff has a value which is a float
num_genes has a value which is an int
ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
ws_expression_matrix_id has a value which is a kb_cummerbund.ws_expression_matrix_id

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
sample1 has a value which is a string
sample2 has a value which is a string
q_value_cutoff has a value which is a float
log2_fold_change_cutoff has a value which is a float
num_genes has a value which is an int
ws_cuffdiff_id has a value which is a kb_cummerbund.ws_cuffdiff_id
ws_expression_matrix_id has a value which is a kb_cummerbund.ws_expression_matrix_id


=end text

=back



=cut

package kb_cummerbund::kb_cummerbundClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
