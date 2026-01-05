# commit_diario.ps1
# Script para commit e push diário

$Data = Get-Date -Format "yyyy-MM-dd"

git add .

# Verifica se há algo para commitar
$Status = git status --porcelain

if ($Status) {
    git commit -m "Progresso do dia $Data"
    git push
    Write-Host "Commit realizado com sucesso ($Data)"
}
else {
    Write-Host "Nada para commitar hoje."
}
