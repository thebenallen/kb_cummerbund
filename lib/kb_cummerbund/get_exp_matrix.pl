
use strict;
use JSON;
my ($infile, $outfile) = @ARGV;
open (FILE, $infile) or die ("cannot open file $ARGV[0]");
my %hash = ();
my @data = <FILE>;
my $first_row = shift @data;
$first_row=~s/\"//g;
chomp ($first_row);
my ($tmp, @samples) = split ("\t", $first_row);

my @matrix=();
my @features;

my @matrix = ();
my $i=0;
foreach (@data){
  $_=~s/\"//g;
  chomp ($_);
  my ($id, @temp) = split (" ", $_);
  my @exp_values;  
  foreach my $value (@temp){
    $value = $value *1.0;
    push @exp_values,  $value;
  }
  push (@features, $id);
  push (@matrix, \@exp_values);
$i++;
}
close (FILE);

if ($i==0){
  my @exp_values = ();
  push (@matrix, @exp_values);
}

$hash{'col_ids'}=\@samples;
$hash{'row_ids'}=\@features;
$hash{'values'}=\@matrix;

my %hx = ();
$hx{'type'}='log-level';
$hx{'scale'}="1.0";
$hx{'data'} = \%hash;
open (FILE2, ">$outfile") or die ("could not open file");
print FILE2  to_json(\%hx);
close (FILE2);
