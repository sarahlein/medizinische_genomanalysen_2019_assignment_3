#! /usr/bin/env python3

import vcf
import httplib2
import os
import subprocess

__author__ = "Sarah Meitz"


##
##
## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
##
## 4) View the VCF in a browser
##

class Assignment3:
    
    def __init__(self):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)

        ## Call annotate_vcf_file here
        self.vcf_path = os.path.join(os.getcwd(), "chr16.vcf")  # TODO

        if not os.path.isfile(self.vcf_path):
            subprocess.call(["wget", "http://hmd.ait.ac.at/medgen2019/chr16.vcf"])

        self.annotations_dict = self.annotate_vcf_file()
    def annotate_vcf_file(self):
        '''
        - Annotate the VCF file using the following example code (for 1 variant)
        - Iterate of the variants (use first 900)
        - Store the result in a data structure
        :return:
        '''    

        ##
        ## Example loop
        ##



        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
                
        params_pos = []  # List of variant positions
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))
                
                if counter >= 899:
                    break
        
        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'
        
        ## Perform annotation
        #res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        #annotation_result = con.decode('utf-8')


        import myvariant
        mv = myvariant.MyVariantInfo()
        ann = mv.getvariants(params)

        annotation_dict = []
        count = 0
        for x in ann:
            try:
                if x['notfound']:
                    pass
            except:
                annotation_dict.append(x)
                count += 1
        #print(count) # 24 gefunden


        
        ## TODO now do something with the 'annotation_result'


        ##
        ## End example code
        ##
        
        return annotation_dict  ## return the data structure here
    
    
    def get_list_of_genes(self):
        '''
        Print the name of genes in the annotation data set
        :return:
        '''

        genes = []

        for hit in self.annotations_dict:
            try:
                if hit['cadd']['gene']:
                    # print(hit['cadd']['gene']['genename'])
                    genes.append(hit['cadd']['gene']['genename'])
            except:
                pass
        print("Genes in annotation data set:\t ", genes)

    
    def get_num_variants_modifier(self):
        '''
        Print the number of variants with putative_impact "MODIFIER"
        :return:
        '''
        count = 0
        for hit in self.annotations_dict:
            if 'snpeff' in hit:
                key, value = "putative_impact", "MODIFIER"
                if key in hit['snpeff']['ann'] and value == hit['snpeff']['ann']['putative_impact']:
                    count += 1

        print("Number of variants with putative_impact 'MODIFIER':\t ", count)
        
    
    def get_num_variants_with_mutationtaster_annotation(self):
        '''
        Print the number of variants with a 'mutationtaster' annotation
        :return:
        '''
        count = 0
        for hit in self.annotations_dict:
            try:
                if hit['dbnsfp']['mutationtaster']:
                    count += 1
            except:
                pass
        print("Number of variants with a 'mutationtaster' annotation:\t ", count)
    
    def get_num_variants_non_synonymous(self):
        '''
        Print the number of variants with 'consequence' 'NON_SYNONYMOUS'
        :return:
        '''
        count = 0
        for hit in self.annotations_dict:
            try:
                if 'cadd' in hit:
                    key, value = "consequence", "NON_SYNONYMOUS"
                    if key in hit['cadd'] and value == hit['cadd']['consequence']:
                        count += 1
            except:
                pass

        print("Number of variants with 'consequence' 'NON_SYNONYMOUS':\t ", count)
        
    
    def view_vcf_in_browser(self):
        '''
        - Open a browser and go to https://vcf.iobio.io/
        - Upload the VCF file and investigate the details
        :return:
        '''
   
        ## Document the final URL here
        print("View vcf in browser: https://vcf.iobio.io/?species=Human&build=GRCh38")
            
    
    def print_summary(self):
        self.get_list_of_genes()
        self.get_num_variants_modifier()
        self.get_num_variants_with_mutationtaster_annotation()
        self.get_num_variants_non_synonymous()
        self.view_vcf_in_browser()
    
    
def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print("Done with assignment 3")
        
        
if __name__ == '__main__':
    main()
   
    



