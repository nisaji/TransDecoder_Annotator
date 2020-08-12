use strict;
my $in_gff = @ARGV[0];

open (my $fh, '<', $in_gff);


my $ID = "None";
while(my $gff = <$fh>){
	chomp($gff);
	#print("$gff\n");
	my @gff = split('\t', $gff);
	my $feature = @gff[2];
	if($feature eq 'gene') {
		my $attribute = @gff[8];
		if ($attribute =~ /complete/){
			print("$gff\n");
		}
	}
	if($feature eq 'mRNA'){
		my $attribute = @gff[8];
		if ($attribute =~ /complete/){
			print("$gff\n");
			my @attributes = split(/;|=/, $attribute);
			my $Parent_ID = @attributes[1];
			$ID = $Parent_ID;
			#print("$ID\n");
		}
		
	}
	if($feature eq 'five_prime_UTR') {
		my $attribute = @gff[8];
		if ($attribute =~ /$ID/){
			print("$gff\n");
		}
	}
	if($feature eq 'exon') {
		my $attribute = @gff[8];
		if ($attribute =~ /$ID/){
			print("$gff\n");
		}
	}
	if($feature eq 'CDS') {
		my $attribute = @gff[8];
		if ($attribute =~ /$ID/){
			print("$gff\n");
		}
	}
	if($feature eq 'three_prime_UTR') {
		my $attribute = @gff[8];
		if ($attribute =~ /$ID/){
			print("$gff\n");
		}	
	}
}
