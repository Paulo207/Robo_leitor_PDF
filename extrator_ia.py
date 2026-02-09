"""
Módulo de extração usando IA (OpenAI) como fallback
Usado quando extração por regex falha
"""

import json
import logging
import os
from typing import Dict, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Tentar importar OpenAI
try:
    from openai import OpenAI
    OPENAI_DISPONIVEL = True
except ImportError:
    OPENAI_DISPONIVEL = False
    logger.warning("OpenAI não instalado. Extração com IA não disponível.")

load_dotenv()


class ExtratorIA:
    """Classe para extração de campos usando IA (OpenAI)"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.cliente = None
        
        if OPENAI_DISPONIVEL and self.api_key:
            self.cliente = OpenAI(api_key=self.api_key)
            logger.info("ExtratorIA inicializado com sucesso")
        else:
            logger.warning("ExtratorIA não disponível (API key não configurada ou OpenAI não instalado)")
    
    def extrair_campos(self, texto: str) -> Optional[Dict]:
        """
        Extrai campos usando IA
        
        Args:
            texto: Texto extraído do PDF
            
        Returns:
            Dicionário com campos extraídos ou None em caso de erro
        """
        if not self.cliente:
            logger.error("Cliente OpenAI não configurado")
            return None
        
        try:
            prompt = self._criar_prompt(texto)
            resposta = self._chamar_api(prompt)
            
            if resposta:
                campos = self._processar_resposta(resposta)
                logger.info("Campos extraídos com sucesso usando IA")
                return campos
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao extrair campos com IA: {str(e)}")
            return None
    
    def _criar_prompt(self, texto: str) -> str:
        """Cria prompt para a IA"""
        prompt = f"""
Você é um especialista em extração de dados de faturas de energia elétrica brasileiras.

Analise o seguinte texto de uma fatura da COELBA (concessionária de energia da Bahia) e extraia os seguintes campos:

1. Nome do Cliente
2. Número da UC (Unidade Consumidora) - geralmente 10-15 dígitos
3. Mês de Referência (formato MM/YYYY ou MMM/YYYY)
4. Data de Vencimento (formato DD/MM/YYYY)
5. Valor Total da Fatura (em reais)
6. Consumo em kWh
7. Impostos:
   - ICMS (valor em reais)
   - PIS (valor em reais)
   - COFINS (valor em reais)
   - CIP ou COSIP (valor em reais, se existir)

Retorne APENAS um objeto JSON válido com a seguinte estrutura, SEM texto adicional:

{{
  "cliente": "",
  "uc": "",
  "mes_referencia": "",
  "data_vencimento": "",
  "valor_total": "",
  "consumo_kwh": "",
  "impostos": {{
    "icms": "",
    "pis": "",
    "cofins": "",
    "cip": ""
  }}
}}

Se algum campo não for encontrado, deixe a string vazia "".

Texto da fatura:
---
{texto[:4000]}
---

JSON:
"""
        return prompt
    
    def _chamar_api(self, prompt: str) -> Optional[str]:
        """Chama API da OpenAI"""
        try:
            response = self.cliente.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em extração de dados estruturados de faturas brasileiras. Sempre retorne JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erro ao chamar API OpenAI: {str(e)}")
            return None
    
    def _processar_resposta(self, resposta: str) -> Optional[Dict]:
        """Processa resposta da IA e converte para dicionário"""
        try:
            # Tentar extrair JSON da resposta
            # A IA pode retornar texto antes/depois do JSON
            inicio_json = resposta.find('{')
            fim_json = resposta.rfind('}') + 1
            
            if inicio_json != -1 and fim_json > inicio_json:
                json_str = resposta[inicio_json:fim_json]
                campos = json.loads(json_str)
                return campos
            
            # Se não encontrar JSON, tentar parse direto
            return json.loads(resposta)
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON da IA: {str(e)}")
            logger.debug(f"Resposta recebida: {resposta}")
            return None
    
    def disponivel(self) -> bool:
        """Verifica se o extrator IA está disponível"""
        return self.cliente is not None
    
    def melhorar_extracao(self, campos_regex: Dict, texto: str) -> Dict:
        """
        Melhora extração existente preenchendo campos faltantes com IA
        
        Args:
            campos_regex: Campos já extraídos por regex
            texto: Texto original do PDF
            
        Returns:
            Campos melhorados
        """
        if not self.disponivel():
            return campos_regex
        
        # Identificar campos vazios
        campos_vazios = []
        for key, value in campos_regex.items():
            if key == 'impostos':
                for imp_key, imp_value in value.items():
                    if not imp_value:
                        campos_vazios.append(f"impostos.{imp_key}")
            elif not value:
                campos_vazios.append(key)
        
        if not campos_vazios:
            logger.info("Todos os campos já foram extraídos, IA não necessária")
            return campos_regex
        
        logger.info(f"Usando IA para preencher campos: {campos_vazios}")
        
        # Extrair com IA
        campos_ia = self.extrair_campos(texto)
        
        if not campos_ia:
            return campos_regex
        
        # Mesclar resultados
        resultado = campos_regex.copy()
        for campo in campos_vazios:
            if '.' in campo:
                # Campo de impostos
                _, imp_nome = campo.split('.')
                if campos_ia.get('impostos', {}).get(imp_nome):
                    resultado['impostos'][imp_nome] = campos_ia['impostos'][imp_nome]
            else:
                if campos_ia.get(campo):
                    resultado[campo] = campos_ia[campo]
        
        return resultado
