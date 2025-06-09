#ifndef PRINCIPAL_H
#define PRINCIPAL_H

void IniciarSistema();
void ExibirMenuPrincipal();
void AutenticarUsuario();
void AlocarVaga();
void LiberarVaga();
void GerenciaFila(const char* usuario);
void AtualizarEstado();
void ExibirResumo();
void EncerrarSistema();
void TratarErros(int codigo);

#endif
