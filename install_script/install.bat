@echo off

::set DEVICE_PATH=ip://192.168.0.104:2020
::if NOT "%COUNTRY_CODE%"=="" (
::set extra=%extra% --es countryCode %COUNTRY_CODE%
::)

::echo ON
::adb shell am broadcast -n "com.siriusxm.aaos.coreapp/com.siriusxm.aaos.coreapp.SettingsReceiver" -a "com.siriusxm.aaos.coreapp.SettingsReceiver.ACTION_SXM_SETTINGS" %extra% --receiver-include-background --user "all"
mkdir C:\ProgramData\NftGenerating
xcopy . C:\ProgramData\NftGenerating /H /Y /C /R /S

shrt\nircmd.exe shortcut C:\ProgramData\NftGenerating\main.exe "~$folder.desktop$" "Nft" "-p Nft"
