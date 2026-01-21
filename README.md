# Projeto-de-Seguranca-de-Redes-II-Autenticidade-e-Integridade-na-Comunicacao-Cliente-Servidor
Implementação de Mecanismos de Autenticidade e Não-Repudiação em Comunicação Cliente-Servidor 

# Sistema de Comunicação Cliente-Servidor Seguro

Projeto desenvolvido para a disciplina de **Redes de Computadores II**, com foco na implementação prática de mecanismos de **autenticidade**, **integridade** e **não-repudiação** em comunicações de rede, bem como na análise de ataques reais em ambientes inseguros.

---

## Objetivo do Projeto

Implementar um sistema cliente-servidor capaz de:
- Garantir a **autenticidade** das mensagens trocadas
- Assegurar a **integridade** dos dados
- Impedir o **repúdio** do emissor
- Detectar ataques do tipo:
  - Atacante passivo
  - Atacante ativo (modificação de dados)
  - Ataque de replay

O projeto simula um ambiente de rede inseguro, no qual atacantes possuem capacidades limitadas, condizentes com cenários reais.

---

## Conceitos de Segurança Aplicados

- Criptografia assimétrica (RSA)
- Assinaturas digitais (RSA-PSS)
- Funções hash criptográficas (SHA-256)
- Proteção contra ataques de replay (timestamp e nonce)
- Framing de mensagens sobre TCP

---

##  Arquitetura do Sistema

```text
Cliente Legítimo
      |
      |  (mensagem assinada)
      v
Rede Insegura
      |
      +--> Atacante Passivo
      +--> Atacante Ativo
      +--> Atacante de Replay
      |
      v
Servidor Seguro

