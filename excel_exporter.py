"""
Módulo para exportar dados extraídos para Excel
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class ExcelExporter:
    """Classe para exportar dados de faturas para Excel"""
    
    def __init__(self, output_path: str = "faturas_coelba.xlsx"):
        """
        Inicializa o exportador
        
        Args:
            output_path: Caminho do arquivo Excel de saída
        """
        self.output_path = Path(output_path)
    
    def export_to_excel(self, data_list: List[Dict]) -> str:
        """
        Exporta uma lista de dados de faturas para Excel
        
        Args:
            data_list: Lista de dicionários com dados das faturas
            
        Returns:
            Caminho do arquivo criado
        """
        if not data_list:
            raise ValueError("Nenhum dado para exportar")
        
        # Criar DataFrame
        df = pd.DataFrame(data_list)
        
        # Ordenar colunas de forma lógica
        column_order = [
            'arquivo',
            'cliente',
            'uc',
            'mes_referencia',
            'vencimento',
            'valor_total',
            'consumo_kwh',
            'impostos'
        ]
        
        # Reordenar colunas se existirem
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        # Criar diretório de saída se não existir
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Salvar no Excel com formatação
        with pd.ExcelWriter(self.output_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Faturas')
            
            # Ajustar largura das colunas
            worksheet = writer.sheets['Faturas']
            for idx, col in enumerate(df.columns, 1):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(64 + idx)].width = min(max_length + 2, 50)
        
        return str(self.output_path)
    
    def append_to_excel(self, new_data: Dict) -> str:
        """
        Adiciona novos dados a um arquivo Excel existente
        
        Args:
            new_data: Dicionário com dados da nova fatura
            
        Returns:
            Caminho do arquivo atualizado
        """
        # Se o arquivo já existe, carregar dados existentes
        if self.output_path.exists():
            df_existing = pd.read_excel(self.output_path)
            df_new = pd.DataFrame([new_data])
            df = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df = pd.DataFrame([new_data])
        
        # Salvar
        with pd.ExcelWriter(self.output_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Faturas')
        
        return str(self.output_path)
