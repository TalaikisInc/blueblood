FILE=$1
solc --abi -o output $FILE.sol
solc --bin -o output $FILE.sol
solc --bin-runtime -o output $FILE.sol
abi = Get-Content .\output\$FILE.abi
bin = Get-Content .\output\$FILE.bin
binRuntime = Get-Content .\output\$FILE.bin-runtime
porosity --code $code --abi $abi --list --verbose 0
orosity --abi $abi --code $code --decompile --verbose 0
