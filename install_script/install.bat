@echo off
mkdir C:\ProgramData\NftGenerating
move .\NFTGen C:\ProgramData\NftGenerating

shrt\nircmd.exe shortcut C:\ProgramData\NftGenerating\NFTGen\main.exe "~$folder.desktop$" "Nft"
