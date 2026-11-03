param(
    [ValidateSet('bios','uefi')][string]$Firmware='bios',
    [string]$Iso=(Join-Path $PSScriptRoot '..\out\aikaos-mini-11.1-cd-x86_64.iso'),
    [ValidateRange(1024,8192)][int]$Memory=4096,
    [ValidateRange(1,8)][int]$CpuCount=2,
    [switch]$Audio
)
$ErrorActionPreference='Stop'
$project=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$testRoot=Join-Path $project "tests\$Firmware"
New-Item -ItemType Directory -Path $testRoot -Force | Out-Null
$isoPath=(Resolve-Path -LiteralPath $Iso).Path.Replace('\','/')
$serialPort=if($Firmware -eq 'bios'){4446}else{4447}
$qmpPort=if($Firmware -eq 'bios'){4456}else{4457}
$qemuArgs=@('-name',"AikaOS-Mini-$Firmware",'-machine','q35','-accel','tcg,thread=multi','-cpu','max','-smp',"$CpuCount",'-m',"$Memory",
    '-device','virtio-vga,xres=1280,yres=800','-device','virtio-rng-pci',
    '-device','qemu-xhci,id=usb','-device','usb-tablet,bus=usb.0','-display','none',
    '-drive',('file="'+$isoPath+'",media=cdrom,if=ide,index=0,readonly=on'),
    '-boot','order=d,menu=on',
    '-netdev','user,id=testnet','-device','virtio-net-pci,netdev=testnet',
    '-serial',"tcp:127.0.0.1:$serialPort,server=on,wait=off",'-qmp',"tcp:127.0.0.1:$qmpPort,server=on,wait=off")
if($Audio){$qemuArgs+=@('-audiodev','none,id=snd0','-device','ich9-intel-hda','-device','hda-duplex,audiodev=snd0')}
if($Firmware -eq 'uefi'){
    $vars=Join-Path $testRoot 'uefi-vars.fd'
    if(-not(Test-Path -LiteralPath $vars)){Copy-Item -LiteralPath 'C:\Program Files\qemu\share\edk2-i386-vars.fd' -Destination $vars}
    $qemuArgs+=@('-drive','if=pflash,format=raw,readonly=on,file="C:/Program Files/qemu/share/edk2-x86_64-code.fd"',
        '-drive','if=pflash,format=raw,file=uefi-vars.fd')
}
$process=Start-Process 'C:\Program Files\qemu\qemu-system-x86_64.exe' -WindowStyle Hidden -WorkingDirectory $testRoot -ArgumentList $qemuArgs -RedirectStandardError (Join-Path $testRoot 'qemu-stderr.log') -PassThru
$result=[pscustomobject]@{pid=$process.Id;firmware=$Firmware;memory_mib=$Memory;iso=$isoPath;sha256=(Get-FileHash -LiteralPath $isoPath -Algorithm SHA256).Hash.ToLower();serial_port=$serialPort;qmp_port=$qmpPort}
$result | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $testRoot 'vm.json')
$result | ConvertTo-Json
