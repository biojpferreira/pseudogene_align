import streamlit as st
import logging
import re
from Bio import SeqIO, pairwise2
from Bio.pairwise2 import format_alignment


# ----------------------- Configuracao de logging ---------------------------

#Loggin configuração coloca o arquivo dentro da pasta log do projeto
log_format='[%(asctime)s] [%(name)s]\t%(levelname)s:%(message)s'
date_format='%Y-%m-%d %H:%M:%S'

logging.basicConfig(datefmt=date_format, format=log_format, level=logging.INFO)

#----------------------------------------------------------------------------
class GeneAlign:
    def __init__(self):
        try:
            self.fasta_reference = "./FLNC_ALIGN.fas"
            ## page basic config
            st.set_page_config(
                page_title="GeneAlign",
                layout="wide",
                initial_sidebar_state="auto",
                menu_items={
                        'About': """# Saturn ecosystem\nPlataforma de alinhamento de pseudogene."""})
            
            self.main()
        except Exception as err:
            logging.getLogger("INIT_APP").error(err)
    
    def check_pattern(self, input_sequence):
        try:
            pattern = r'^[ATCG]+$'
            return bool(re.match(pattern, input_sequence))
            
        except Exception as err:
            logging.getLogger("VALIDATE_SEQUENCE").error(err)
    
    def align_sequence_with_fasta(self,input_seq):
        # Ler a sequência de referência do arquivo FASTA
        reference_seq = None
        for record in SeqIO.parse(self.fasta_reference, "fasta"):
            reference_seq = str(record.seq)
            sequence_id = record.id  # Nome (ID) da sequência
        
             # Realizar o alinhamento local, com parâmetros para correspondência exata
            alignments = pairwise2.align.localms(
                input_seq, reference_seq,
                1,     # Pontuação para match exato
                -100,  # Penalidade para mismatch
                -100,  # Penalidade para abertura de gap
                -100   # Penalidade para extensão de gap
            )
            
            # Exibe os resultados do alinhamento
            if alignments:
                st.success(f"Alinhamento encontrado com a sequência: {sequence_id}")
                
                for alignment in alignments:
                    aligned_score = alignment[2]
                    
                    percent_identity = (aligned_score/len(input_seq)) * 100
                    
                    text = f"Match com {round(percent_identity,2)}% de correspondencia"
                    
                    if percent_identity >= 98: st.success(text)
                    elif percent_identity <= 97 and  percent_identity >= 50: st.warning(text)
                    else: st.error(text)
                    
                    st.code(format_alignment(*alignment))
            else:
                st.error(f"Nenhum alinhamento encontrado para a sequência: {sequence_id}")
                    
    def main(self):
        try:
            st.title("Alinhador de sequencias com pseudogene FLNC")
            user_sequence = st.text_input(label="Insira uma sequencia",value="", 
                                               placeholder="ACGCTAGCTAGCATGCATC")
            if self.check_pattern(user_sequence):
                st.success("Sequencia válida")
                st.divider()
                self.align_sequence_with_fasta(user_sequence)
            else:
                st.error("Sequencia inválida")
            
        except Exception as err:
            logging.getLogger("MAIN_APP").error(err)
    

if __name__ =="__main__":
    GeneAlign()
    
        